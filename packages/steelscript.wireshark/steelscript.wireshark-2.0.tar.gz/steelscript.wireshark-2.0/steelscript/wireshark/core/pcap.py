# Copyright (c) 2019 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

import os
import re
import sys
import pickle
import logging
import subprocess
import datetime
import tempfile
import pytz
import tzlocal

from dateutil.parser import parse as dateutil_parse

from steelscript.common.timeutils import parse_timedelta
from steelscript.wireshark.core.exceptions import InvalidField

HAVE_PCAP = False

# hack around the fact that ModuleNotFoundError is not present below 3.6
v_i = sys.version_info
if v_i.major == 3 and v_i.minor <= 5:
    ModuleNotFoundError = Exception
try:
    from steelscript.packets.core.pcap import pcap_info
    from steelscript.packets.query.pcap_query import PcapQuery
    HAVE_PCAP = True
except (ImportError, ModuleNotFoundError):
    pass


logger = logging.getLogger(__name__)

local_tz = tzlocal.get_localzone()

# include path for capinfos and tshark
popen_env = os.environ
popen_env["PATH"] = "/usr/local/bin/:" + popen_env["PATH"]


class PcapFile(object):

    OCCURRENCE_FIRST = 'f'
    OCCURRENCE_LAST = 'l'
    OCCURRENCE_ALL = 'a'

    def __init__(self, filename):
        self.filename = filename

        self._info = None
        self.starttime = None
        self.endtime = None
        self.numpackets = None

    def info(self):
        """Returns info on pcap file, uses ``capinfos -A -m -T`` or
        steelscript's pcap library internally depending on environment."""
        if self._info is None:
            if HAVE_PCAP:
                logger.debug(
                    "PcapFile.info() run using steelscript pcap library.")
                with open(self.filename, 'rb') as pfile:
                    pfile_info = pcap_info(pfile)

                self._info = {'Start time': pfile_info['first_timestamp'],
                              'End time': pfile_info['last_timestamp'],
                              'Number of packets': pfile_info[
                                  'total_packets']
                              }
                self.starttime = (datetime.datetime
                                  .utcfromtimestamp(self._info['Start time'])
                                  .replace(tzinfo=pytz.utc)
                                  .astimezone(local_tz))
                self.endtime = (datetime.datetime
                                .utcfromtimestamp(self._info['End time'])
                                .replace(tzinfo=pytz.utc)
                                .astimezone(local_tz))
                self.numpackets = self._info['Number of packets']

            else:
                logger.debug(
                    "PcapFile.info() run using Wireshark capinfos subprocess "
                    "call.")
                cmd = ['capinfos', '-A', '-m', '-T', self.filename]
                logger.info('subprocess: %s' % ' '.join(cmd))
                capinfos = subprocess.check_output(cmd,
                                                   env=popen_env,
                                                   universal_newlines=True)
                capinfos = capinfos.decode('utf8')
                hdrs, vals = (capinfos.split('\n')[:2])
                self._info = dict(zip(hdrs.split(','), vals.split(',')))

                self.starttime = (dateutil_parse(self._info['Start time'])
                                  .replace(tzinfo=local_tz))
                self.endtime = (dateutil_parse(self._info['End time'])
                                .replace(tzinfo=local_tz))

                self.numpackets = int(self._info['Number of packets'])

        return self._info

    def export(self, filename,
               starttime=None, endtime=None, duration=None):
        """Returns a PCAP file, potentially including your specified starttime,
        endtime or duration. Internally uses editcap

        :param str filename: the name of the new PCAP file to be
            created/exported from the existing PCAP file
        :param str starttime: defines a start time filter
        :param str endtime: defines an end time filter
        :param str duration: defines a duration filter

        """

        cmd = ['editcap']

        if starttime is not None:
            if isinstance(starttime, str):
                starttime = dateutil_parse(starttime)

        if endtime is not None:
            if isinstance(endtime, str):
                endtime = dateutil_parse(endtime)

        if duration is not None:
            if isinstance(duration, str):
                duration = parse_timedelta(duration)

            if starttime:
                endtime = starttime + duration
            elif endtime:
                starttime = endtime - duration
            else:
                raise ValueError("Must specify either starttime or "
                                 "endtime with duration")

        if starttime is not None:
            cmd.extend(['-A', (starttime
                               .strftime('%Y-%m-%d %H:%M:%S'))])

        if endtime is not None:
            cmd.extend(['-B', (endtime
                               .strftime('%Y-%m-%d %H:%M:%S'))])

        cmd.append(self.filename)
        cmd.append(filename)

        logger.info('subprocess: %s' % ' '.join(cmd))
        subprocess.check_output(cmd, env=popen_env, universal_newlines=True)

        return PcapFile(filename)

    def delete(self):
        """Removes the filename from PcapFile object and deletes the file"""
        if os.path.exists(self.filename):
            os.unlink(self.filename)

        self.filename = None

    def query(self, fieldnames, filterexpr=None,
              starttime=None, endtime=None, duration=None,
              use_tshark_fields=True,
              occurrence=OCCURRENCE_ALL,
              aggregator=',',
              as_dataframe=False,
              use_ss_packets=True):
        """Parses the PCAP file, returning the data in a tabular format.
        NOTE: When using OCCURRENCE_ALL you can generate an exception if there
        are multiple fields that have multiple values.

        :param list fieldnames: a list of field names for the desired values.
            Use the aggregator string for seperating columns
        :param str filterexpr: the filter expression used by tshark for
            refining your data
        :param str starttime: defines a start time filter for the query
        :param str endtime: defines an end time filter for the query
        :param str duration: defines a duration filter for the query
        :param bool use_tshark_fields: use the internal class TSharkField for
            more flexibility during data manipulation. Defaults to True.
        :param str occurrence: defines if you want the first, last, or all
            occurrences. Values:

                - 'f' (PcapFile.OCCURRENCE_FIRST) - First
                - 'l' (PcapFile.OCCURRENCE_LAST) - Last
                - 'a' (PcapFile.OCCURRENCE_ALL) - All

        :param str aggregator: delimiter string for seperating columns (aka
            tshark fields)
        :param bool as_dataframe: if true, returns a Pandas dataframe object
            with the results of the query. If false returns a list. Defaults
            to false.
        :param bool use_ss_packets: if allows the use of steelscript.packets
            pcap_query. Forces use of tshark if false.
        """
        if not self.filename:
            raise ValueError('No filename')

        """
        Test if we can use the pcap lib query. This is true if we only have
        supported fields and, optionally, a start and end time. All other
        arguments must be default and we can't have a filterexpr.
        """
        pq = None
        use_pcap = False
        if use_ss_packets and HAVE_PCAP:
            use_pcap = HAVE_PCAP
        if use_pcap:
            pq = PcapQuery()
            if pq.fields_supported(fieldnames and
                    filterexpr in [None, ''] and duration is None and
                    occurrence == self.OCCURRENCE_ALL and
                    aggregator == ','):
                stime = 0.0
                etime = 0.0
                rdf = 1 if as_dataframe else 0
                if starttime is not None:
                    if isinstance(starttime, str):
                        stime = dateutil_parse(starttime)
                if endtime is not None:
                    if isinstance(endtime, str):
                        etime = dateutil_parse(endtime)

                logger.debug(
                    "PcapFile.query() run using PcapQuery.pcap_query().")
                with open(self.filename, 'rb') as f:
                    return pq.pcap_query(f, fieldnames, stime, etime, rdf=rdf)

        # Continue with native tshark query instead
        cmd = ['tshark', '-r', self.filename,
               '-T', 'fields',
               '-E', 'occurrence=%s' % occurrence]

        if occurrence == self.OCCURRENCE_ALL:
            cmd.extend(['-E', 'aggregator=%s' % aggregator])

        if starttime or endtime:
            logger.info("Creating temp pcap file for timerange: %s-%s" %
                        (starttime, endtime))
            (fd, filename) = tempfile.mkstemp(suffix='.pcap')
            os.close(fd)
            p = self.export(filename,
                            starttime=starttime,
                            endtime=endtime,
                            duration=duration)
            logger.info("Issuing query on temp pcap file")
            res = p.query(fieldnames, filterexpr=filterexpr,
                          use_tshark_fields=use_tshark_fields,
                          occurrence=occurrence,
                          as_dataframe=as_dataframe)
            p.delete()
            return res

        if filterexpr not in [None, '']:
            # use new '-Y' option since '-R' is deprecated
            cmd.extend(['-Y', filterexpr])

        fields = []
        for n in fieldnames:
            if use_tshark_fields:
                tf = TSharkFields.instance()
                if n in tf.protocols:
                    # Allow protocols as a field, but convert to a string
                    # rather than attempt to parse it
                    fields.append(TSharkField(n, '', 'FT_STRING', n))

                elif n in tf.fields:
                    fields.append(tf.fields[n])

                else:
                    raise InvalidField(n)

            cmd.extend(['-e', n])

        logger.info('subprocess: %s' % ' '.join(cmd))
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                env=popen_env,
                                universal_newlines=True)

        data = []
        errors = 0

        line = proc.stdout.readline().rstrip()

        while proc.poll() is None or line:
            cols = line.split('\t')
            if len(cols) < len(fieldnames):
                cols.extend([None]*(len(fieldnames) - len(cols)))
                logger.debug("Line incomplete: '%s'" % line)
            elif len(cols) > len(fieldnames):
                logger.error("Could not parse line: '%s'" % line)
                errors = errors + 1
                if errors > 20:
                    return
                continue

            if occurrence == PcapFile.OCCURRENCE_ALL:
                newcols = []
                needs_dup = []
                n = 0
                multi_occur = False
                for i, col in enumerate(cols):
                    if col and ',' in col:
                        if n:
                            logger.warning('One packet has at least '
                                           'two columns with multiple '
                                           'occurrences, skip it. '
                                           'cmd: %s' % ' '.join(cmd))
                            multi_occur = True
                            break
                        # Split col data into an array
                        newcol = col.split(',')
                        newcols.append(newcol)
                        n = len(newcol)
                    else:
                        # Single valued column, keep track of
                        # the col index, as we need to dup it
                        # below
                        newcols.append(col)
                        needs_dup.append(i)

                if multi_occur:
                    # The above for loop exited due to multiple occurrences of
                    # at least two columns in the current packet. Skip this
                    # packet and keep processing the rest of the pcap file
                    continue

                if n:
                    for i in needs_dup:
                        newcols[i] = ([newcols[i]] * n)
                    rows = (list(map(list, zip(*newcols))))
                else:
                    rows = [newcols]
            else:
                rows = [cols]

            if use_tshark_fields:
                newrows = []
                for row in rows:
                    newcols = []
                    for i, col in enumerate(row):
                        t = fields[i].datatype
                        if col == '' or col is None:
                            col = None
                        elif t == datetime.datetime:
                            col = (dateutil_parse(col)
                                   .replace(tzinfo=local_tz))
                        elif fields[i].name == 'frame.time_epoch':
                            col = (datetime.datetime.utcfromtimestamp(float(col))
                                   .replace(tzinfo=pytz.utc)
                                   .astimezone(local_tz))
                        elif t in [int, int]:
                            col = t(col, base=0)
                        else:
                            col = t(col)
                        newcols.append(col)
                    newrows.append(newcols)
                rows = newrows

            data.extend(rows)

            # grab next line
            line = proc.stdout.readline().rstrip()

        if as_dataframe:
            if len(data) > 0:
                import pandas
                df = pandas.DataFrame(data, columns=fieldnames)
                return df
            else:
                return None
        else:
            return data


class TSharkField(object):

    __slots__ = ['name', 'desc', 'datatype', 'datatype_str', 'protocol']

    def __init__(self, name, desc, datatype, protocol):
        self.name = name
        self.desc = desc
        self.protocol = protocol
        self.datatype_str = datatype

        if re.match('FT_U?INT64.*', datatype):
            self.datatype = int
        elif re.match('FT_(U?INT.*|FRAMENUM)', datatype):
            self.datatype = int
        elif re.match('FT_(FLOAT|DOUBLE|RELATIVE_TIME)', datatype):
            self.datatype = float
        elif re.match('FT_ABSOLUTE_TIME', datatype):
            self.datatype = datetime.datetime
        else:
            self.datatype = str

    def __str__(self):
        return '<TSharkField %s, %s>' % (self.name, self.datatype_str)

    def __repr__(self):
        return str(self)

    def __getstate__(self):
        return [self.name, self.desc, self.datatype_str,
                self.datatype, self.protocol]

    def __setstate__(self, state):
        (self.name, self.desc, self.datatype_str,
         self.datatype, self.protocol) = state


class TSharkFields(object):

    CACHEFILE = os.path.join(os.path.expanduser('~'), '.steelscript',
                             'tshark_fields')
    CACHEFILE_VERSION = 1

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = TSharkFields()
        return cls._instance

    def __init__(self):
        self.protocols = None
        self.fields = None
        self.load()

    def load(self, force=False, ignore_cache=False, protocols=None):
        """Load"""
        if self.protocols and not force:
            return

        if not ignore_cache and os.path.exists(self.CACHEFILE):
            with open(self.CACHEFILE, 'rb') as f:
                version = pickle.load(f)
                if version == self.CACHEFILE_VERSION:
                    protos, fields = pickle.load(f)
                    if protos.keys() and fields.keys():
                        self.protocols, self.fields = protos, fields
                        return
                else:
                    logger.info("Cache file version mistmatch")

        cmd = ['tshark', '-G', 'fields']

        logger.info('subprocess: %s' % ' '.join(cmd))
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                env=popen_env,
                                universal_newlines=True)

        self.protocols = {}
        self.fields = {}
        while proc.poll() is None:
            line = proc.stdout.readline().rstrip()
            if not line:
                continue
            fields = line.split('\t')
            if fields[0] == 'P':
                (t, desc, name) = fields[:3]
                if protocols is not None and name not in protocols:
                    continue
                self.protocols[name] = desc
            elif fields[0] == 'F':
                (t, desc, name, datatype, protocol) = fields[:5]
                if protocols is not None and protocol not in protocols:
                    continue
                self.fields[name] = TSharkField(name, desc, datatype, protocol)

        with open(self.CACHEFILE, 'wb', 2) as f:
            pickle.dump(self.CACHEFILE_VERSION, f)
            pickle.dump([self.protocols, self.fields], f)

    def find(self, name=None, name_re=None,
             desc=None, desc_re=None,
             protocol=None, protocol_re=None):
        fields = []
        for field in self.fields.values():
            if ( (name is not None and name != field.name) or
                 (name_re is not None and not re.search(name_re, field.name)) or
                 (desc is not None and desc != field.desc) or
                 (desc_re is not None and not re.search(desc_re, field.desc)) or
                 (protocol is not None and protocol != field.protocol) or
                 (protocol_re is not None and
                  not re.search(protocol_re, field.protocol))):
                continue
            fields.append(field)
        return fields
