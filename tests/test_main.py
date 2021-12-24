def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_request_end_point(client):
    r = client.get("/request")
    assert r.json() == {'response': "Someday"}
    assert r.status_code == 200