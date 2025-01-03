from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import boto3
from botocore.exceptions import ClientError
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

class CloudTransfer:
    # Google Drive API scope
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        """
        Initialize the CloudTransfer with Google Drive and Amazon Photos credentials
        """
        # Google Drive setup
        self.creds = self._get_google_credentials(credentials_path, token_path)
        self.service = build('drive', 'v3', credentials=self.creds)

        # Amazon Photos setup
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def _get_google_credentials(self, credentials_path, token_path):
        """
        Get or refresh Google Drive credentials
        """
        creds = None
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def create_drive_folder(self, folder_name, parent_folder_id=None):
        """Creates a folder in Google Drive."""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        
        file = self.service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def upload_to_drive(self, local_file_path, drive_folder_id):
        """Uploads a file to Google Drive."""
        file_metadata = {
            'name': os.path.basename(local_file_path),
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(local_file_path, mimetype='*/*')
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')

    def download_from_amazon(self, bucket_name, key, local_file_path):
        """Downloads a file from Amazon Photos."""
        try:
            self.s3.download_file(bucket_name, key, local_file_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"File '{key}' not found in Amazon Photos.")
            else:
                print(f"Error downloading file: {str(e)}")
            return False

    def transfer_photos(self, bucket_name, temp_dir='/tmp'):
        """
        Transfer all photos from Amazon Photos to Google Drive
        """
        # Create root folder in Google Drive
        root_folder_id = self.create_drive_folder('Amazon Photos Transfer')

        # List all objects in the Amazon Photos bucket
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' not in response:
                print(f"No objects found in bucket {bucket_name}")
                return

            for obj in response['Contents']:
                key = obj['Key']
                file_name = os.path.basename(key)
                local_path = os.path.join(temp_dir, file_name)

                print(f"Processing {file_name}...")

                # Download from Amazon Photos
                if self.download_from_amazon(bucket_name, key, local_path):
                    # Upload to Google Drive
                    try:
                        file_id = self.upload_to_drive(local_path, root_folder_id)
                        print(f"Successfully transferred {file_name}")
                    except Exception as e:
                        print(f"Error uploading {file_name} to Google Drive: {str(e)}")
                    finally:
                        # Clean up temporary file
                        if os.path.exists(local_path):
                            os.remove(local_path)

        except Exception as e:
            print(f"Error during transfer: {str(e)}")

def main():
    # Create a .env file with these variables
    # AWS_ACCESS_KEY_ID=your_access_key
    # AWS_SECRET_ACCESS_KEY=your_secret_key
    # AWS_REGION=your_region

    transfer = CloudTransfer(
        credentials_path='credentials.json',
        token_path='token.json'
    )
    
    # Replace with your actual bucket name
    transfer.transfer_photos('your-amazon-photos-bucket')

if __name__ == "__main__":
    main() 