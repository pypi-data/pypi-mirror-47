========================
python-bsn-neutronclient
========================

Python bindings for Big Switch Networks Neutron API

* Free software: Apache license

Features
--------

- Network Templates
- Reachability Tests - BCF test path extension
- Tenant Policies
- Manually force BCF to sync network configuration

CLI Usage
---------
Currently only force-bcf-sync should be accessed via CLI, other features
should be accessed via Horizon GUI

OpenStack CLI:

- openstack force-bcf-sync
    - Force BCF to sync network configuration
    - No parameter

Neutron CLI (Deprecated):

- neutron force-bcf-sync 1
    - Force BCF to sync network configuration
    - Number 1 is required as parameter