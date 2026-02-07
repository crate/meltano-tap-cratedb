"""A Singer tap for CrateDB, built with the Meltano SDK, based on the PostgreSQL tap."""

from importlib.metadata import PackageNotFoundError, version

from tap_cratedb.patch import patch_sqlalchemy_dialect

__appname__ = "meltano-tap-cratedb"

try:
    __version__ = version(__appname__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

patch_sqlalchemy_dialect()
