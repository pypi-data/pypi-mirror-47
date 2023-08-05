# Copyright 2017 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from horizon import tabs

from openstack_dashboard.dashboards.admin.instances import tables
from openstack_dashboard.dashboards.project.instances import tabs \
    as project_tabs


class AuditTab(project_tabs.AuditTab):
    table_classes = (tables.AdminAuditTable,)


class AdminInstanceDetailTabs(tabs.DetailTabsGroup):
    slug = "instance_details"
    tabs = (project_tabs.OverviewTab, project_tabs.LogTab,
            project_tabs.ConsoleTab, AuditTab)
    sticky = True
