import io
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload


# File paths for the client secret and token files
SERVICE_ACCOUNT_FILE = './keys/google_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

def create_drive_service(service_account_file, user_email):
    """
    Create a Google Drive service using the specified service_account_file and impersonating the user_email.

    :param service_account_file: Path to the service account JSON key file.
    :param user_email: The email address of the user to impersonate.
    :param scopes: A list of scopes for the API. Defaults to None.
    :return: A Google Drive service instance or None if an error occurred.
    """

    try:
        creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        delegated_creds = creds.with_subject(user_email)
        service = build('drive', 'v3', credentials=delegated_creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def list_files(service, number_of_files=10):
    """
    List the specified number of files from the authenticated user's Google Drive.

    :param service: A Google Drive service instance.
    :param number_of_files: The number of files to list. Defaults to 10.
    :return: A list of dictionaries containing the file id and name/path of the file.
    """
    # Query the Google Drive API to get the list of files
    results = service.files().list(
        pageSize=number_of_files, fields="nextPageToken, files(id, name)").execute()

    items = results.get('files', [])

    # Create an empty list to store the file information
    file_list = []

    # Add a dictionary with file id and name/path for each file
    for item in items:
        file_list.append({"id": item["id"], "name": item["name"]})

    return file_list

def list_folders(service):
    """
    List all folders in the authenticated user's Google Drive.

    :param service: A Google Drive service instance.
    """
    query = "mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    folders = []

    for item in items:
        folders.append({"id": item["id"], "name": item["name"]})

    return folders

def list_files_in_folder(service, folder_id, include_subfolders=True):
    """
    List all files in the specified folder and its subfolders.

    :param service: A Google Drive service instance.
    :param folder_id: The ID of the folder to list files from.
    :param include_subfolders: If True, include files in subfolders. Defaults to True.
    """
    files = []
    query = f"'{folder_id}' in parents"

    def recursive_list_files(service, query):
        nonlocal files
        results = service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
        items = results.get('files', [])

        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder' and include_subfolders:
                recursive_list_files(service, f"'{item['id']}' in parents")
            else:
                files.append(item)

    recursive_list_files(service, query)
    return files


def download_and_read_file(service, file_id):
    """
    Download and read the contents of the specified file.

    :param service: A Google Drive service instance.
    :param file_id: The ID of the file to download and read.
    :return: The contents of the file as a string.
    """
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download progress: {int(status.progress() * 100)}%")

    file.seek(0)
    content = file.read().decode('utf-8')
    return content
