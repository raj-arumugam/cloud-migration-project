# Cloud Photo Transfer

A Python utility to transfer photos from Amazon Photos (AWS S3) to Google Drive.

## Features

- Authenticates with both Amazon Photos (AWS S3) and Google Drive
- Creates a dedicated folder in Google Drive for transferred photos
- Downloads photos from Amazon Photos and uploads them to Google Drive
- Handles temporary file cleanup automatically
- Supports batch transfer of multiple photos

## Prerequisites

- Python 3.6+
- Amazon AWS account with access to S3
- Google Cloud Console project with Drive API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd cloud-photo-transfer
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Configure Google Drive API:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one
   - Enable the Google Drive API
   - Configure the OAuth consent screen
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials and save as `credentials.json` in the project directory

4. Configure AWS credentials:
   - Create a `.env` file in the project root
   - Add your AWS credentials:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
```

## Usage

1. Update the main function in `cloud_transfer.py` with your bucket name:

```python
transfer.transfer_photos('your-amazon-photos-bucket')
```

2. Run the script:

```bash
python cloud_transfer.py
```

On first run, the script will:
- Open a browser window for Google authentication
- Create a token.json file for future authentication
- Create a new folder in Google Drive called "Amazon Photos Transfer"
- Begin transferring photos from Amazon Photos to Google Drive

## File Structure

```
cloud-photo-transfer/
├── cloud_transfer.py    # Main script
├── requirements.txt     # Python dependencies
├── .env                # AWS credentials
├── credentials.json    # Google OAuth credentials
└── token.json         # Generated Google OAuth token
```

## Dependencies

- google-api-python-client
- google-auth-oauthlib
- boto3
- python-dotenv

## Error Handling

The script includes error handling for common scenarios:
- Missing or invalid credentials
- Network connectivity issues
- File not found errors
- API rate limits

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Notes

- Never commit your `.env` file or `credentials.json` to version control
- Keep your `token.json` file secure
- Regularly rotate your AWS access keys
- Use appropriate IAM roles and permissions

## Troubleshooting

1. **Authentication Issues**
   - Ensure credentials.json is properly configured
   - Delete token.json and re-authenticate if needed
   - Verify AWS credentials in .env file

2. **Transfer Problems**
   - Check internet connectivity
   - Verify S3 bucket permissions
   - Ensure sufficient disk space for temporary files

3. **Rate Limits**
   - The script includes basic rate limiting
   - For large transfers, consider implementing additional delays

## Support

For issues and feature requests, please create an issue in the repository.

