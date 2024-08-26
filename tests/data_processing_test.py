# test_data_processing.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_pipeline.data_processing import process_data, prepare_dataframe_for_insert
from datetime import datetime

@patch('data_pipeline.data_processing.pq.write_table')
@patch('data_pipeline.data_processing.datetime')
def test_process_data_success(mock_datetime, mock_write_table):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)
    data = {'col1': [1, 2], 'col2': [3, 4]}
    filename = process_data(data)
    expected_filename = "raw_data_20230101000000.parquet"
    assert filename == expected_filename
    mock_write_table.assert_called_once()

@patch('data_pipeline.data_processing.pq.write_table')
@patch('data_pipeline.data_processing.datetime')
def test_process_data_error(mock_datetime, mock_write_table):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)
    mock_write_table.side_effect = Exception("Mock error")
    data = {'col1': [1, 2], 'col2': [3, 4]}
    with pytest.raises(Exception):
        process_data(data)

def test_prepare_dataframe_for_insert_success():
    data = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(data)
    result_df = prepare_dataframe_for_insert(df)
    assert 'data_ingestao' in result_df.columns
    assert 'dado_linha' in result_df.columns
    assert 'tag' in result_df.columns
    assert result_df['tag'].iloc[0] == 'Personagem'