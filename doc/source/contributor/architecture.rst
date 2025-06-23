===================
System Architecture
===================

Aetos is a reverse-proxy, which should be used together with Prometheus.
It implements a subset of Prometheus API to support observabilityclient's and
Watcher's access to Prometheus. Using Aetos provides OpenStack authentication
and multi-tenancy support to Prometheus.

On most endpoints Aetos recognizes 2 types of access:
        - privileged
        - nonprivileged

Privileged access is by default automatically allowed for admin and service
users and it allows sending requests without any restrictions. Privileged
users can retrieve any metric from any project at any time. These users can
also retrieve metrics coming from other sources than ceilometer, which
typically lack openstack project labels.

Nonprivileged access is allowed for users with the reader or member role.
These users cat retrieve metrics from their current project only. Aetos
will automatically modify each request to prevent access to metrics from
other projects.

Privileged and unprivileged access can be configured for each endpoint
separately by modifying policies.
