#
# Copyright 2025 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from aetos.controllers.api.v1.admin import root as admin_root
from aetos.controllers.api.v1 import label
from aetos.controllers.api.v1 import labels
from aetos.controllers.api.v1 import query
from aetos.controllers.api.v1 import series
from aetos.controllers.api.v1 import status
from aetos.controllers.api.v1 import targets


class V1Controller:
    """Version 1 API controller root."""

    query = query.QueryController()
    series = series.SeriesController()
    labels = labels.LabelsController()
    label = label.LabelController()
    targets = targets.TargetsController()
    status = status.StatusController()
    admin = admin_root.AdminController()
