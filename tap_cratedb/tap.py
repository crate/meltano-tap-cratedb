"""CrateDB tap implementation, based on the PostgreSQL tap."""
from __future__ import annotations

from functools import cached_property

import tap_postgres
from sqlalchemy.engine import make_url
from tap_postgres.client import (
    PostgresStream,
)
from tap_postgres.tap import TapPostgres

from tap_cratedb.client import CrateDBConnector


class TapCrateDB(TapPostgres):
    name = "tap-cratedb"
    default_stream_class = PostgresStream

    @cached_property
    def connector(self) -> CrateDBConnector:
        """
        Get a configured connector for this Tap.

        Connector is a singleton (one instance is used by the Tap and Streams).
        """
        # We mutate this url to use the ssh tunnel if enabled
        url = make_url(self.config.get("sqlalchemy_url", "crate://"))
        ssh_config = self.config.get("ssh_tunnel", {})

        if ssh_config.get("enable", False):  # pragma: no cover
            # Return a new URL with SSH tunnel parameters
            if hasattr(tap_postgres, "connection_parameters"):
                from tap_postgres.connection_parameters import ConnectionParameters

                url = self.ssh_tunnel_connect(
                    ssh_config=ssh_config, connection_parameters=ConnectionParameters.from_tap_config(self.config)
                )
            else:
                url = self.ssh_tunnel_connect(ssh_config=ssh_config, url=url)

        return CrateDBConnector(
            config=dict(self.config),
            sqlalchemy_url=url.render_as_string(hide_password=False),
        )
