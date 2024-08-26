import pytest
from unittest import mock
import pandas as pd
from data_pipeline.clickhouse_client import execute_sql_script, get_client, insert_dataframe
import os

# Teste para get_client
@mock.patch('clickhouse_connect.get_client')
def test_get_client(mock_get_client):
    mock_get_client.return_value = mock.Mock()
    client = get_client()
    
    mock_get_client.assert_called_once_with(
        host=os.getenv('CLICKHOUSE_HOST'),
        port=os.getenv('CLICKHOUSE_PORT'),
        user=os.getenv('CLICKHOUSE_USER'),
        password=os.getenv('CLICKHOUSE_PASS')
    )
    assert client is not None

# Teste para execute_sql_script
@mock.patch('clickhouse_connect.get_client')
def test_execute_sql_script(mock_get_client):
    mock_client = mock.Mock()
    mock_get_client.return_value = mock_client

    with mock.patch("builtins.open", mock.mock_open(read_data="CREATE TABLE test_table (id Int32)")):
        client = execute_sql_script("dummy_path.sql")
    
    mock_client.command.assert_called_once_with("CREATE TABLE test_table (id Int32)")
    assert client == mock_client

# Teste para insert_dataframe
@mock.patch('clickhouse_connect.get_client')
def test_insert_dataframe(mock_get_client):
    mock_client = mock.Mock()
    mock_get_client.return_value = mock_client

    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Rick', 'Morty', 'Summer']})
    insert_dataframe(mock_client, "test_table", df)
    
    mock_client.insert_df.assert_called_once_with("test_table", df)

# Teste para erro em get_client
@mock.patch('clickhouse_connect.get_client')
def test_get_client_error(mock_get_client):
    mock_get_client.side_effect = Exception("Failed to connect")
    
    with pytest.raises(Exception) as exc_info:
        get_client()
    
    assert str(exc_info.value) == "Failed to connect"

# Teste para erro em execute_sql_script
@mock.patch('clickhouse_connect.get_client')
def test_execute_sql_script_error(mock_get_client):
    mock_client = mock.Mock()
    mock_client.command.side_effect = Exception("Failed to execute script")
    mock_get_client.return_value = mock_client

    with mock.patch("builtins.open", mock.mock_open(read_data="CREATE TABLE test_table (id Int32)")):
        with pytest.raises(Exception) as exc_info:
            execute_sql_script("dummy_path.sql")
    
    assert str(exc_info.value) == "Failed to execute script"

# Teste para erro em insert_dataframe
@mock.patch('clickhouse_connect.get_client')
def test_insert_dataframe_error(mock_get_client):
    mock_client = mock.Mock()
    mock_client.insert_df.side_effect = Exception("Failed to insert data")
    mock_get_client.return_value = mock_client

    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Rick', 'Morty', 'Summer']})
    
    with pytest.raises(Exception) as exc_info:
        insert_dataframe(mock_client, "test_table", df)
    
    assert str(exc_info.value) == "Failed to insert data"
