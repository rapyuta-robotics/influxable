import pytest
from influxable import InfluxDBApi, exceptions
from influxable.connection import Connection


class TestConnection:
    def check_if_connection_reached(self, connection):
        query = 'SHOW DATABASES'
        InfluxDBApi.execute_query(connection.request, query)

    def test_create_instance_with_no_args_success(self):
        connection = Connection()
        self.check_if_connection_reached(connection)
        assert connection is not None

    def test_create_instance_with_args_success(self):
        connection = Connection(
            user='admin',
            password='changeme'
        )
        self.check_if_connection_reached(connection)
        assert connection is not None

