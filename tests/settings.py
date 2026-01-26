# The database schema name.

# Used to switch the default schema within the test cases from `public`
# (PostgreSQL) to `doc` (CrateDB). It could make sense to contribute
# this switch to upstream [tap-postgres] in one way or another.
#
# https://github.com/crate/meltano-tap-cratedb/issues/6
#
# [tap-postgres]: https://github.com/MeltanoLabs/tap-postgres

# PostgreSQL default.
# DB_SCHEMA_NAME = "public"  # noqa: ERA001

# CrateDB default.
DB_SCHEMA_NAME = "doc"
