from uuid import uuid4
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_returns_ok():
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_auth_register_login_and_me_flow():
    email = f"test_{uuid4().hex[:10]}@example.com"
    password = 'TestPass123!'

    register_response = client.post(
        '/auth/register',
        json={
            'email': email,
            'password': password,
            'name': 'Smoke Test User',
        },
    )

    assert register_response.status_code == 200
    register_payload = register_response.json()
    assert register_payload['token']
    assert register_payload['user']['email'] == email
    assert register_payload['user']['user_id']
    assert register_payload['user']['employee_id']

    login_response = client.post(
        '/auth/login',
        json={
            'email': email,
            'password': password,
        },
    )

    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload['token']
    assert login_payload['user']['email'] == email

    me_response = client.get(
        '/auth/me',
        headers={'Authorization': f"Bearer {login_payload['token']}"},
    )

    assert me_response.status_code == 200
    me_payload = me_response.json()
    assert me_payload['email'] == email
    assert me_payload['user_id'] == login_payload['user']['user_id']
    assert me_payload['employee_id'] == login_payload['user']['employee_id']


def test_full_ml_api_flow_upload_train_bias_explain_report():
    sample_csv = Path(__file__).resolve().parents[1] / 'data' / 'sample_dataset.csv'
    assert sample_csv.exists(), f'Missing sample dataset: {sample_csv}'

    with sample_csv.open('rb') as csv_file:
        upload_response = client.post(
            '/upload',
            files={'file': ('sample_dataset.csv', csv_file, 'text/csv')},
            data={'target_column': 'hired'},
        )

    assert upload_response.status_code == 200
    upload_payload = upload_response.json()
    assert upload_payload['dataset_id']
    assert upload_payload['rows'] > 0
    assert 'hired' in upload_payload['columns']

    train_response = client.post(
        '/train',
        json={
            'dataset_id': upload_payload['dataset_id'],
            'target_column': 'hired',
            'model_type': 'logistic_regression',
            'test_size': 0.2,
            'random_state': 42,
            'async_job': False,
        },
    )

    assert train_response.status_code == 200
    train_payload = train_response.json()
    assert train_payload['status'] == 'completed'
    run_id = train_payload['result']['run_id']
    assert run_id

    bias_response = client.get('/bias', params={'run_id': run_id, 'sensitive_column': 'gender'})
    assert bias_response.status_code == 200
    bias_payload = bias_response.json()
    assert bias_payload['run_id'] == run_id
    assert 'fairness_index' in bias_payload

    explain_response = client.get('/explain', params={'run_id': run_id, 'sample_size': 20, 'async_job': False})
    assert explain_response.status_code == 200
    explain_payload = explain_response.json()
    assert explain_payload['status'] == 'completed'
    assert explain_payload['result']['run_id'] == run_id

    report_response = client.get('/report', params={'run_id': run_id, 'sensitive_column': 'gender', 'sample_size': 20})
    assert report_response.status_code == 200
    report_payload = report_response.json()
    assert report_payload['run_id'] == run_id
    assert report_payload['train']['run_id'] == run_id
    assert report_payload['bias']['run_id'] == run_id
    assert report_payload['explain']['run_id'] == run_id
