"""Test Configuration."""
import logging

# Increase logging for components we are working on.
logging.getLogger("sqlconnector").setLevel(logging.DEBUG)
logging.getLogger("tap-cratedb").setLevel(logging.DEBUG)
logging.getLogger("tap-postgres").setLevel(logging.DEBUG)

# Decrease logging for components not of immediate interest.
logging.getLogger("faker").setLevel(logging.INFO)
logging.getLogger("crate.client.http").setLevel(logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
