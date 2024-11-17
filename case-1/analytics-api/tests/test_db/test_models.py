from app.db.models import LocationData, Base
from sqlalchemy import inspect

def test_location_data_table_exists():
    table_name = LocationData.__tablename__

    tables = Base.metadata.tables
    assert table_name in tables, f"Table '{table_name}' does not exist in metadata."

def test_location_data_columns():
    mapper = inspect(LocationData)
    table = mapper.local_table

    expected_columns = {
        'id': 'INTEGER',
        'device_id': 'VARCHAR',
        'latitude': 'FLOAT',
        'longitude': 'FLOAT',
        'speed': 'FLOAT',
        'timestamp': 'DATETIME'
    }

    for column in table.columns:
        assert column.name in expected_columns, f"Unexpected column '{column.name}' found."

    for column_name in expected_columns.keys():
        assert column_name in table.columns, f"Expected column '{column_name}' not found."