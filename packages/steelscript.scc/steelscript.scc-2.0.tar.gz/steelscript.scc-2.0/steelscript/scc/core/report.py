# Copyright (c) 2019 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

import logging

from steelscript.netprofiler.core.filters import TimeFilter # [mzetea] - shouldn't netprofiler be added as a dependency?
from steelscript.common.timeutils import datetime_to_seconds

# Below are mappings from resource to report class
scc_stats_reports = {
    'bw_usage': 'BWUsageStatsReport',
    'bw_timeseries': 'BWTimeSeriesStatsReport',
    'bw_per_appliance': 'BWPerApplStatsReport',
    'throughput': 'ThroughputStatsReport',
    'throughput_per_appliance': 'ThroughputPerApplStatsReport',
    'connection_history': 'ConnectionHistoryStatsReport',
    'connection_pooling': 'ConnectionPoolingStatsReport',
    'connection_forwarding': 'ConnectionForwardingStatsReport',
    'http': 'HTTPStatsReport',
    'nfs': 'NFSStatsReport',
    'ssl': 'SSLStatsReport',
    'disk_load': 'DiskLoadStatsReport',
    'dns_usage': 'DNSUsageStatsReport',
    'dns_cache_hits': 'DNSCacheHitsStatsReport',
    'sdr_adaptive': 'SDRAdaptiveStatsReport',
    'memory_paging': 'MemoryPagingStatsReport',
    'cpu_utilization': 'CpuUtilizationStatsReport',
    'pfs': 'PFSStatsReport',
    'srdf': 'SRDFStatsReport',
    'tcp_memory_pressure': 'TCPMemoryPressureReport',
    'qos': 'QoSStatsReport',
    'snap_mirror': 'SnapMirrorStatsReport',
    'granite_lun_io': 'SteelFusionLUNIOReport',
    'granite_initiator_io': 'SteelFusionInitiatorIOReport',
    'granite_network_io': 'SteelFusionNetworkIOReport',
    'blockstore': 'SteelFusionBlockstoreReport'}

scc_appl_reports = {'appliances': 'AppliancesReport'}

# Remove prefix 'cmc' from the actual service name
# 'cmc.stats' or 'cmc.appliance_inventory' for easy
# reference of scc service attributes

scc_reports = {'stats': scc_stats_reports,
               'appliance_inventory': scc_appl_reports}

logger = logging.getLogger(__name__)


def get_scc_report_class(service, resource):
    """Return report class based on service name and resource name."""
    return eval(scc_reports[service][resource])


class SCCException(Exception):
    pass


class BaseSCCReport(object):
    """Base class for SCC reports, not directly used for
    creating report objects.

    :param service: string, attr name of the service obj
    :param resource: string, name of the resource
    :param link: string, name of the link to retrieve data
    :param data_key: string, key mapping to the data in response
        if None, then the entire reponse is desired
    :param required_fields: list of fields required by the sub-report,
        excluding start_time and end_time.
    :param non_required_fields: list of fields available to use but not
        required by the sub-report
    """
    service = None
    resource = None
    link = None
    data_key = None
    required_fields = []
    non_required_fields = []

    def __init__(self, scc):
        self.scc = scc
        self.datarep = None
        self.response = None
        self.data = None
        self.criteria = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if any([type, value, traceback]):
            logger.exception("Exception in running %s" %
                             self.__class__.__name__)

    def _fill_criteria(self, **kwargs):
        # Ensure all passed-in params are valid params
        valid_fields = set(self.required_fields + self.non_required_fields)

        for field in kwargs:
            if field not in valid_fields:
                raise SCCException("Criteria '%s' is not a valid field for %s"
                                   % (field, self.__class__.__name__))

        for field in self.required_fields:
            if field not in kwargs or not kwargs[field]:
                raise SCCException("Field '%s' is required to run %s" %
                                   (field, self.__class__.__name__))

        temp = {}
        for field in valid_fields:
            if field in kwargs and kwargs[field]:
                temp[field] = kwargs[field]
        self.criteria = temp if temp else None

    def run(self, **kwargs):
        """Run report to fetch data from the SCC device"""
        self._fill_criteria(**kwargs)
        svc_obj = getattr(self.scc, self.service)
        self.datarep = svc_obj.bind(self.resource)
        self.response = self.datarep.execute(self.link, self.criteria)
        if (self.data_key and isinstance(self.response.data, dict) and
                self.data_key in self.response.data):
            self.data = self.response.data[self.data_key]
        elif not self.data_key:
            self.data = self.response.data
        else:
            raise SCCException('data_key %s is invalid for %s'
                               % (self.data_key, self.__class__.__name__))


class BaseStatsReport(BaseSCCReport):
    """Base class for reports generated by scc.stats api, not directly
    used for creating reports objects. All report instances are derived based
    on sub-classes inheriting from this class.
    """

    service = 'stats'

    def _fill_criteria(self, **kwargs):

        if ('timefilter' in kwargs and
                not all(['start_time' in kwargs, 'end_time' in kwargs])):

            # when timefilter is passed in, need to convert to start/end time
            timefilter = TimeFilter.parse_range(kwargs['timefilter'])

            kwargs['start_time'] = timefilter.start
            kwargs['end_time'] = timefilter.end
            del kwargs['timefilter']

        for name in ['start_time', 'end_time']:
            if name in kwargs:
                kwargs[name] = datetime_to_seconds(kwargs[name])

        if 'devices' in kwargs and kwargs['devices']:
            kwargs['devices'] = kwargs['devices'].split(',')

        if 'port' in kwargs and kwargs['port']:
            kwargs['port'] = int(kwargs['port'])

        super(BaseStatsReport, self)._fill_criteria(**kwargs)

#
# Bandwidth Reports
#


class BWUsageStatsReport(BaseStatsReport):
    """Report class to return bandwidth usage"""
    resource = 'bw_usage'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['start_time', 'end_time']
    non_required_fields = ['traffic_type', 'port', 'devices']


class BWTimeSeriesStatsReport(BaseStatsReport):
    """Report class to return bandwidth timeseries"""
    resource = 'bw_timeseries'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['start_time', 'end_time']
    non_required_fields = ['traffic_type', 'port', 'devices']


class BWPerApplStatsReport(BaseStatsReport):
    """Report class to return the bandwidth per appliance data"""
    resource = 'bw_per_appliance'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['devices', 'start_time', 'end_time']
    non_required_fields = ['traffic_type']

#
# Throughput Reports
#


class ThroughputStatsReport(BaseStatsReport):
    """Report class to return the peak/p95 throughput timeseries"""
    resource = 'throughput'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type', 'port']


class ThroughputPerApplStatsReport(BaseStatsReport):
    """Report class to return the throughput per appliance data"""
    resource = 'throughput_per_appliance'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['devices', 'start_time', 'end_time']
    non_required_fields = ['traffic_type']

#
# Timeseries Reports for Single Device
#


class ConnectionHistoryStatsReport(BaseStatsReport):
    """Report class to return the max/avg connection history timeseries"""
    resource = 'connection_history'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type']


class SRDFStatsReport(BaseStatsReport):
    """Report class to return the regular/peak srdf timeseries"""
    resource = 'srdf'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type']


class TCPMemoryPressureReport(BaseStatsReport):
    """Report class to return regular/peak tcp memory pressure timesries"""
    resource = 'tcp_memory_pressure'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type']

#
# Multiple Devices Reports
#


class MultiDevStatsReport(BaseStatsReport):
    required_fields = ['start_time', 'end_time']
    non_required_fields = ['devices']


class ConnectionPoolingStatsReport(MultiDevStatsReport):
    """Report class to return the connection pooling timeseries"""
    resource = 'connection_pooling'
    link = 'report'
    data_key = 'response_data'


class ConnectionForwardingStatsReport(MultiDevStatsReport):
    """Report class to return the connection forwrding timeseries"""
    resource = 'connection_forwarding'
    link = 'report'
    data_key = 'response_data'


class DNSUsageStatsReport(MultiDevStatsReport):
    """Report class to return the dns usage timeseries"""
    resource = 'dns_usage'
    link = 'report'
    data_key = 'response_data'


class DNSCacheHitsStatsReport(MultiDevStatsReport):
    """Report class to return the dns cache hits timeseries"""
    resource = 'dns_cache_hits'
    link = 'report'
    data_key = 'response_data'


class HTTPStatsReport(MultiDevStatsReport):
    """Report class to return the http timeseries"""
    resource = 'http'
    link = 'report'
    data_key = 'response_data'


class NFSStatsReport(MultiDevStatsReport):
    """Report class to return the nfs timeseries"""
    resource = 'nfs'
    link = 'report'
    data_key = 'response_data'


class SSLStatsReport(MultiDevStatsReport):
    """Report class to return the ssl timeseries"""
    resource = 'ssl'
    link = 'report'
    data_key = 'response_data'


class DiskLoadStatsReport(MultiDevStatsReport):
    """Report class to return disk load timeseries"""
    resource = 'disk_load'
    link = 'report'
    data_key = 'response_data'

#
# Single Device Reports
#


class SingleDevStatsReport(BaseStatsReport):
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = []


class SDRAdaptiveStatsReport(SingleDevStatsReport):
    """Report class to return the SDR Adaptive timeseries"""
    resource = 'sdr_adaptive'
    link = 'report'
    data_key = 'response_data'


class MemoryPagingStatsReport(SingleDevStatsReport):
    """Report class to return the memory paging timeseries"""
    resource = 'memory_paging'
    link = 'report'
    data_key = 'response_data'


class CpuUtilizationStatsReport(SingleDevStatsReport):
    """Report class to return the cpu utilization timeseries"""
    resource = 'cpu_utilization'
    link = 'report'
    data_key = 'response_data'


class PFSStatsReport(SingleDevStatsReport):
    """Report class to return the pfs timeseries"""
    resource = 'pfs'
    link = 'report'
    data_key = 'response_data'


#
# Qos Reports
#


class QoSStatsReport(BaseStatsReport):
    """Report class to return the outbound/inbound qos timeseries"""
    resource = 'qos'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['qos_class_id', 'traffic_type']

#
# Snapmirror Reports
#


class SnapMirrorStatsReport(BaseStatsReport):
    """Report class to return regular/peak snapmirror timeseries"""
    resource = 'snapmirror'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['filer_id', 'traffic_type']


#
# SteelFusion Reports
#


class SteelFusionLUNIOReport(BaseStatsReport):
    """Report class to return the SteelFusion lun io timeseries"""
    resource = 'granite_lun_io'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type', 'lun_subclass_id']


class SteelFusionInitiatorIOReport(BaseStatsReport):
    """Report class to return the SteelFusion initiator io timeseries"""
    resource = 'granite_initiator_io'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type', 'initiator_subclass_id']


class SteelFusionNetworkIOReport(BaseStatsReport):
    """Report class to return the SteelFusion network IO timeseries"""
    resource = 'granite_network_io'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['start_time', 'end_time', 'device']
    non_required_fields = ['traffic_type']


class SteelFusionBlockstoreReport(BaseStatsReport):
    """Report class to return the SteelFusion blockstore timeseries"""
    resource = 'granite_blockstore'
    link = 'report'
    data_key = 'response_data'
    required_fields = ['device', 'start_time', 'end_time']
    non_required_fields = ['traffic_type', 'lun_subclass_id']


#
# cmc.appliance_inventory service reports
#


class BaseApplInvtReport(BaseSCCReport):
    """Base class for reports generated by appliance_inventory api, not
    directly used for creating reports objects. All report instances are
    derived based on sub-classes inheriting from this class.
    """
    service = 'appliance_inventory'


class AppliancesReport(BaseApplInvtReport):
    """Report class to return brief info of appliances"""
    resource = 'appliances'
    link = 'get'
    data_key = None
    required_fields = []
    non_required_fields = []
