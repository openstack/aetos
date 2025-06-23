=========
Aetos API
=========

Aetos API is currently a minimal subset of `Prometheus API
<https://prometheus.io/docs/prometheus/latest/querying/api/>`_
as required by the observabilityclient and Watcher.

Regular API
===========

.. rest-controller:: aetos.controllers.api.v1.label:LabelController
   :webprefix: /api/v1/label/<name>/values

.. rest-controller:: aetos.controllers.api.v1.labels:LabelsController
   :webprefix: /api/v1/labels

.. rest-controller:: aetos.controllers.api.v1.query:QueryController
   :webprefix: /api/v1/query

.. rest-controller:: aetos.controllers.api.v1.series:SeriesController
   :webprefix: /api/v1/series

.. rest-controller:: aetos.controllers.api.v1.status:StatusController
   :webprefix: /api/v1/status

.. rest-controller:: aetos.controllers.api.v1.targets:TargetsController
   :webprefix: /api/v1/targets

Admin API
=========

.. rest-controller:: aetos.controllers.api.v1.admin.tsdb.clean_tombstones:CleanTombstonesController
   :webprefix: /api/v1/admin/tsdb/clean_tombstones

.. rest-controller:: aetos.controllers.api.v1.admin.tsdb.delete_series:DeleteSeriesController
   :webprefix: /api/v1/admin/tsdb/delete_series

.. rest-controller:: aetos.controllers.api.v1.admin.tsdb.snapshot:SnapshotController
   :webprefix: /api/v1/admin/tsdb/snapshot
