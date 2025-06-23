======================
Aetos service overview
======================
The aetos service provides a multi-tenancy layer and openstack authentication
for Prometheus.

The aetos service consists of the following components:

``aetos``
  A reverse-proxy, which runs on a central management server, preferably on
  the same one which runs Prometheus. It provides a subset of Prometheus
  API. For each request an authentication token is checked before forwarding
  it to Prometheus. Two privilege levels are recognized. When accessing
  with lower privilege, which typically means access by a non-admin user,
  the request is restricted to metrics from the current project only.
