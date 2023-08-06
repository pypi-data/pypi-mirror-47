# Copyright (c) 2019 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from steelscript.scc.core.app import SCCApp
from steelscript.scc.core import report as report_module

import pprint


class SteelFusionNetworkIOReportApp(SCCApp):

    def add_options(self, parser):
        super(SteelFusionNetworkIOReportApp, self).add_options(parser)

        parser.add_option(
            '--timefilter', dest='timefilter', default='last 1 hour',
            help='Time range to analyze (defaults to "last 1 hour") '
            'other valid formats are: "4/21/13 4:00 to 4/21/13 5:00" '
            'or "16:00:00 to 21:00:04.546"')

        parser.add_option(
            '--traffic_type', dest='traffic_type', default='throughput',
            help='Type of traffic to query, either for throughput or prefetch')

        parser.add_option('--device', dest='device', default=None,
                          help='Device ID')

    def validate_args(self):
        super(SteelFusionNetworkIOReportApp, self).validate_args()

        if not self.options.device:
            self.parser.error("Device (serial ID) is required")

    def main(self):
        with report_module.SteelFusionNetworkIOReport(self.scc) as report:
            report.run(timefilter=self.options.timefilter,
                       traffic_type=self.options.traffic_type,
                       device=self.options.device)
            pprint.pprint(report.data)

if __name__ == '__main__':
    SteelFusionNetworkIOReportApp().run()
