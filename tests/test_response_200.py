import requests

# Test for 200 response
def test_response_status_code():
    try:
        res = requests.get("http://127.0.0.1:5000")
    except ConnectionRefusedError as e:
        raise ConnectionRefusedError
    assert res.status_code == 200
