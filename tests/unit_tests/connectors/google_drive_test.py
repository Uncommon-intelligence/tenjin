from tenjin.connectors.google_drive import list_files, list_files_in_folder

def create_mock_service_class(mock_execute_result):
    class MockService:
        def files(self):
            return self

        def list(self, *args, **kwargs):
            return self

        def execute(self):
            return mock_execute_result

    return MockService


def create_mock_service(mock_execute_result, service_account_file, user_email):
    MockService = create_mock_service_class(mock_execute_result)
    return MockService()


def test_list_files(capfd):
    service_account_file = "./not/a/real/file.json"
    user_email = "user@example.org"
    mock_execute_result = {"files": [{"id": "1", "name": "Test File"}]}

    service = create_mock_service(mock_execute_result, service_account_file, user_email)
    files = list_files(service)

    assert files == [{"id": "1", "name": "Test File"}]


def test_list_files_in_folder(capfd):
    service_account_file = "./not/a/real/file.json"
    user_email = "user@example.org"
    mock_execute_result = {"files": [{"id": "1", "name": "Test File", "mimeType": "application/pdf", "parents": ["0"]}]}

    service = create_mock_service(mock_execute_result, service_account_file, user_email)
    files = list_files_in_folder(service, "0")

    assert files == [{"id": "1", "name": "Test File", "mimeType": "application/pdf", "parents": ["0"]}]
