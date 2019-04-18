We building four types of containers
====================================

* `registry.getnoc.com/noc/noc/code:$version` -- contains noc. Ready to be launched as standalone image.

* `registry.getnoc.com/noc/noc/static:$version` -- only contains static files and nginx. Intended to be used as container for frontend static for nomad or k8s

* `registry.getnoc.com/noc/noc/build:$version` -- does not contains noc source only deps. should be used as container for tests

* `registry.getnoc.com/noc/noc/dev:$version` -- based on code container. but contains some additional debug tools
