import unittest
from unittest.mock import patch, MagicMock
from cloud_transfer import CloudTransfer

class TestCloudTransfer(unittest.TestCase):

    @patch('cloud_transfer.build')
    @patch('cloud_transfer.boto3.client')
    @patch('cloud_transfer.CloudTransfer._get_google_credentials')
    def setUp(self, mock_get_google_credentials, mock_boto_client, mock_build):
        # Mock Google credentials and service
        mock_get_google_credentials.return_value = MagicMock()
        mock_build.return_value = MagicMock()

        # Mock S3 client
        mock_boto_client.return_value = MagicMock()

        self.cloud_transfer = CloudTransfer()

    def test_initialization(self):
        self.assertIsNotNone(self.cloud_transfer.creds)
        self.assertIsNotNone(self.cloud_transfer.service)
        self.assertIsNotNone(self.cloud_transfer.s3)

    @patch('cloud_transfer.CloudTransfer.create_drive_folder')
    def test_create_drive_folder(self, mock_create_drive_folder):
        folder_name = 'TestFolder'
        self.cloud_transfer.create_drive_folder(folder_name)
        mock_create_drive_folder.assert_called_with(folder_name)

    @patch('cloud_transfer.CloudTransfer.upload_to_drive')
    def test_upload_to_drive(self, mock_upload_to_drive):
        file_path = 'test.jpg'
        folder_id = 'folder_id'
        self.cloud_transfer.upload_to_drive(file_path, folder_id)
        mock_upload_to_drive.assert_called_with(file_path, folder_id)

    @patch('cloud_transfer.CloudTransfer.download_from_amazon')
    def test_download_from_amazon(self, mock_download_from_amazon):
        bucket_name = 'test-bucket'
        object_key = 'test.jpg'
        download_path = 'downloads/test.jpg'
        self.cloud_transfer.download_from_amazon(bucket_name, object_key, download_path)
        mock_download_from_amazon.assert_called_with(bucket_name, object_key, download_path)

if __name__ == '__main__':
    unittest.main()