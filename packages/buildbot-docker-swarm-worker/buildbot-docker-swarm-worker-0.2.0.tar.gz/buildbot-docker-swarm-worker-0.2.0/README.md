[![PyPI](https://img.shields.io/pypi/v/buildbot-docker-swarm-worker.svg?style=flat-square)](https://pypi.org/project/buildbot-docker-swarm-worker/)
[![Build Status](https://img.shields.io/travis/com/cjolowicz/buildbot-docker-swarm-worker.svg?style=flat-square)](https://travis-ci.com/cjolowicz/buildbot-docker-swarm-worker)
[![Coverage Status](https://img.shields.io/coveralls/cjolowicz/buildbot-docker-swarm-worker.svg?style=flat-square)](https://coveralls.io/github/cjolowicz/buildbot-docker-swarm-worker?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)

# buildbot-docker-swarm-worker

This package provides a [buildbot](https://buildbot.net) plugin to
deploy buildbot workers on demand as services on a
[Docker Swarm](https://docs.docker.com/engine/swarm/) cluster.

## Installation

Install this package from
[PyPI](https://pypi.org/project/buildbot-docker-swarm-worker/):

```sh
pip install buildbot-docker-swarm-worker
```

## Usage

```python
from buildbot.plugins import worker
swarm_worker = worker.DockerSwarmLatentWorker(
    "docker-swarm-worker",
    "buildbot/buildbot-worker:latest",
)
```

## Related projects

- https://github.com/cjolowicz/docker-buildbot
- https://github.com/cjolowicz/docker-buildbot-worker
