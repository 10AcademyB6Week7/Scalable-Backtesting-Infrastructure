from urllib import response
import sys, json
sys.path.insert(0,'./backend/')
from backtest_api import app

client = app.test_client()

def test_backtest_results():
    client_response = client.get('/backtest_results')
    assert b'success' in client_response.data
    assert 200 == client_response.status_code

def test_get_backtest_scene():
    payload = json.dumps({
            "start_data": "test",
            "end_data": "test",
            "indicator":"test",
            "parameter_range":"test"
        })
    client_response = client.post('/get_backtest_scene', headers={"Content-Type": "application/json"}, data=payload)
    assert b'success' in client_response.data
    assert 200 == client_response.status_code

