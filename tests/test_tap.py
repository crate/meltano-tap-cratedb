import io
import json
from contextlib import redirect_stdout
from unittest import mock

from singer_sdk.singerlib import Catalog
from singer_sdk.testing import sync_end_to_end

from tap_cratedb.tap import TapCrateDB

cratedb_builtin_streams = [
    "information_schema-administrable_role_authorizations",
    "information_schema-applicable_roles",
    "information_schema-character_sets",
    "information_schema-columns",
    "information_schema-enabled_roles",
    "information_schema-foreign_server_options",
    "information_schema-foreign_servers",
    "information_schema-foreign_table_options",
    "information_schema-foreign_tables",
    "information_schema-key_column_usage",
    "information_schema-referential_constraints",
    "information_schema-role_table_grants",
    "information_schema-routines",
    "information_schema-schemata",
    "information_schema-sql_features",
    "information_schema-table_constraints",
    "information_schema-table_partitions",
    "information_schema-tables",
    "information_schema-user_mapping_options",
    "information_schema-user_mappings",
    "information_schema-view_column_usage",
    "information_schema-views",
    "pg_catalog-pg_am",
    "pg_catalog-pg_attrdef",
    "pg_catalog-pg_attribute",
    "pg_catalog-pg_auth_members",
    "pg_catalog-pg_class",
    "pg_catalog-pg_constraint",
    "pg_catalog-pg_cursors",
    "pg_catalog-pg_database",
    "pg_catalog-pg_depend",
    "pg_catalog-pg_description",
    "pg_catalog-pg_enum",
    "pg_catalog-pg_event_trigger",
    "pg_catalog-pg_index",
    "pg_catalog-pg_indexes",
    "pg_catalog-pg_locks",
    "pg_catalog-pg_matviews",
    "pg_catalog-pg_namespace",
    "pg_catalog-pg_proc",
    "pg_catalog-pg_publication",
    "pg_catalog-pg_publication_tables",
    "pg_catalog-pg_range",
    "pg_catalog-pg_roles",
    "pg_catalog-pg_settings",
    "pg_catalog-pg_shdescription",
    "pg_catalog-pg_stats",
    "pg_catalog-pg_subscription",
    "pg_catalog-pg_subscription_rel",
    "pg_catalog-pg_tables",
    "pg_catalog-pg_tablespace",
    "pg_catalog-pg_type",
    "pg_catalog-pg_views",
    "sys-allocations",
    "sys-checks",
    "sys-cluster",
    "sys-cluster_health",
    "sys-health",
    "sys-jobs",
    "sys-jobs_log",
    "sys-jobs_metrics",
    "sys-node_checks",
    "sys-nodes",
    "sys-operations",
    "sys-operations_log",
    "sys-privileges",
    "sys-repositories",
    "sys-roles",
    "sys-segments",
    "sys-sessions",
    "sys-shards",
    "sys-snapshot_restore",
    "sys-snapshots",
    "sys-summits",
    "sys-users",
]

cratedb_summits_cardinality = 1605

singer_config = {"sqlalchemy_url": "crate://"}


def test_tap_discover_streams():
    """
    Verify discovery of available streams.
    """
    tap = TapCrateDB(config=singer_config)
    streams = tap.discover_streams()
    curated_names = []
    for stream in streams:
        if (
            stream.name.startswith("information_schema-")
            or stream.name.startswith("pg_catalog-")
            or stream.name.startswith("sys-")
        ):
            curated_names.append(stream.name)
    assert curated_names == cratedb_builtin_streams


def test_tap_sync_all():
    """
    Verify end-to-end sync from the tap to the target.
    """

    class DummyTarget(mock.Mock):
        name = "dummy"

    tap = TapCrateDB(config=singer_config)
    target = DummyTarget()
    sync_end_to_end(tap, target)
    target.assert_has_calls([mock.call.listen(mock.ANY)])


def test_tap_sync_summits():
    """
    Verify contents of a single table sync.
    """
    with open("tests/resources/cratedb-summits.json") as f:
        catalog = Catalog.from_dict(json.load(f))

    tap = TapCrateDB(config=singer_config, catalog=catalog)
    stream = tap.streams.get("sys-summits")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        stream.sync()
    buffer.seek(0)
    payload = buffer.getvalue()

    # Verify cardinality.
    # Singer output includes a SCHEMA line and a STATE line in addition to RECORD lines.
    record_lines = [line for line in payload.splitlines() if '"type":"RECORD"' in line]
    length = len(record_lines)
    assert (
        length == cratedb_summits_cardinality
    ), f"In table 'sys.summits', expected {cratedb_summits_cardinality} records, got {length}"

    # Verify content per single sample.
    assert '"region":"Bergamo Alps"' in payload
