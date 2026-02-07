# Singer tap / Meltano extractor for CrateDB

[![Tests](https://github.com/crate/meltano-tap-cratedb/actions/workflows/main.yml/badge.svg)](https://github.com/crate/meltano-tap-cratedb/actions/workflows/main.yml)
[![Test coverage](https://img.shields.io/codecov/c/gh/crate/meltano-tap-cratedb.svg)](https://codecov.io/gh/crate/meltano-tap-cratedb/)
[![Python versions](https://img.shields.io/pypi/pyversions/meltano-tap-cratedb.svg)](https://pypi.org/project/meltano-tap-cratedb/)

[![License](https://img.shields.io/github/license/crate/meltano-tap-cratedb.svg)](https://github.com/crate/meltano-tap-cratedb/blob/main/LICENSE)
[![Status](https://img.shields.io/pypi/status/meltano-tap-cratedb.svg)](https://pypi.org/project/meltano-tap-cratedb/)
[![PyPI](https://img.shields.io/pypi/v/meltano-tap-cratedb.svg)](https://pypi.org/project/meltano-tap-cratedb/)
[![Downloads](https://pepy.tech/badge/meltano-tap-cratedb/month)](https://pepy.tech/project/meltano-tap-cratedb/)


## About

A [Singer] tap for [CrateDB], built with the [Meltano SDK] for custom extractors
and loaders, and based on the [Meltano PostgreSQL tap].

In Singer ELT jargon, a "tap" conceptually wraps a data source, where you
"extract" data from.

In order to learn more about Singer, Meltano, and friends, please
navigate to the [Singer Intro].

## Install

Usually, you will not install this package directly, but rather on behalf
of a Meltano project. A corresponding snippet is outlined in the next section.

After adding it to your `meltano.yml` project definition file, you can install
all defined components and their dependencies with a single command.

```shell
meltano install
```

## Usage

You can run the CrateDB Singer tap `tap-cratedb` by itself, or
in a pipeline using Meltano.

### Meltano

Using the `meltano add` subcommand, you can add the plugin to your
Meltano project.
```shell
meltano add extractor tap-cratedb
```
NB: It will only work like this when released and registered on Meltano Hub.
    In the meanwhile, please add the configuration snippet manually.


#### CrateDB Cloud

In order to connect to [CrateDB Cloud], configure the `sqlalchemy_url` setting
within your `meltano.yml` configuration file like this.
```yaml
- name: tap-cratedb
  namespace: cratedb
  variant: cratedb
  pip_url: meltano-tap-cratedb
  config:
    sqlalchemy_url: "crate://admin:password@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true"
```


#### On localhost
In order to connect to a standalone or on-premise instance of CrateDB, configure
the `sqlalchemy_url` setting within your `meltano.yml` configuration file like this.
```yaml
- name: tap-cratedb
  namespace: cratedb
  variant: cratedb
  pip_url: meltano-tap-cratedb
  config:
    sqlalchemy_url: crate://crate@localhost/
```

Then, invoke the pipeline by using `meltano run`, similar like this.
```shell
meltano run tap-cratedb target-csv
```

### Standalone

You can also invoke the adapter standalone by using the `tap-cratedb` program.
This example demonstrates how to export data from the database into a file.

Define the database connection string including credentials in SQLAlchemy format.
```shell
export TAP_CRATEDB_SQLALCHEMY_URL='crate://admin:K4IgMXNvQBJM3CiElOiPHuSp6CiXPCiQYhB4I9dLccVHGvvvitPSYr1vTpt4@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true'
```

Discover all available database streams.
```shell
tap-cratedb --config ENV --discover
```

Export CrateDB's `sys.summits` table.
```shell
tap-cratedb --config ENV --catalog tests/resources/cratedb-summits.json
```

## Development

In order to work on this adapter dialect on behalf of a real pipeline definition,
link your sandbox to a development installation of [meltano-tap-cratedb], and
configure the `pip_url` of the component to point to a different location than the
[vanilla package on PyPI].

Use this URL to directly point to a specific Git repository reference.
```yaml
pip_url: git+https://github.com/crate/meltano-tap-cratedb.git@main
```

Use a `pip`-like notation to link the CrateDB Singer tap in development mode,
so you can work on it at the same time while running the pipeline, and iterating
on its definition.
```yaml
pip_url: --editable=/path/to/sources/meltano-tap-cratedb
```


[CrateDB]: https://cratedb.com/product
[CrateDB Cloud]: https://console.cratedb.cloud/
[Meltano SDK]: https://github.com/meltano/sdk
[Meltano PostgreSQL tap]: https://github.com/MeltanoLabs/tap-postgres
[meltano-tap-cratedb]: https://github.com/crate/meltano-tap-cratedb
[Singer]: https://www.singer.io/
[vanilla package on PyPI]: https://pypi.org/project/meltano-tap-cratedb/
