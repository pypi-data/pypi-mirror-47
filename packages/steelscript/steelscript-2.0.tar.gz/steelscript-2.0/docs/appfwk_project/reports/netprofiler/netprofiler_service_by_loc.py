# Copyright (c) 2015 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

import steelscript.appfwk.apps.report.modules.tables as tables
from steelscript.appfwk.apps.report.models import Report

from steelscript.netprofiler.appfwk.datasources.netprofiler import \
    NetProfilerServiceByLocTable

#
# NetProfiler report
#

report = Report.create("NetProfiler Services", position=10)

report.add_section()

# Define a Overall TimeSeries showing Avg Bytes/s
p = NetProfilerServiceByLocTable.create('services-by-loc')

report.add_widget(tables.TableWidget, p, "Services by location", width=6)
