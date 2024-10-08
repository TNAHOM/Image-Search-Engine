import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")


async def upload_to_google_drive(file_path: str) -> str:
    # Use service account credentials from the JSON file
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    # Folder name where the files should be uploaded
    folder_name = "Hackaton image list"
    folder_id = None

    # Search for the folder in Google Drive
    response = (
        service.files()
        .list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces="drive",
            fields="files(id, name)",
        )
        .execute()
    )

    # If folder exists, get its ID; otherwise, create it
    if response.get("files"):
        folder_id = response["files"][0]["id"]
    else:
        # Create a new folder
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        folder = service.files().create(body=file_metadata, fields="id").execute()
        folder_id = folder.get("id")

    # Upload the file to the specific folder
    file_metadata = {
        "name": os.path.basename(file_path),
        "parents": [folder_id],  # Specify the folder ID to upload into
    }
    media = MediaFileUpload(file_path, resumable=True)

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_id = file.get("id")

    # Make the file accessible to the specified user email
    service.permissions().create(
        fileId=file_id,
        body={"role": "writer", "type": "user", "emailAddress": "nahomt2419@gmail.com"},
    ).execute()

    return f"https://drive.google.com/uc?id={file_id}"
