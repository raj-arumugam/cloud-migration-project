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
- Sufficient storage space for temporary files during transfer

## Setup

1. Clone the repository:

```bash
git clone https://github.com/raj-arumugam/cloud-migration-project
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
   - Add your AWS credentials and S3 bucket name:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET_NAME=your-bucket-name
```

## Usage

1. Run the script:

```bash
python cloud_transfer.py
```

The script will:
- Authenticate with Google Drive on first run
- Create a "Amazon Photos Transfer" folder in Google Drive
- Transfer photos from your configured S3 bucket to Google Drive
- Display progress during transfer

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

## Performance Considerations

- Large transfers may take significant time
- Consider running transfers during off-peak hours
- Memory usage scales with file size
- Temporary storage needs equal to largest file being transferred

## Known Limitations

- Does not preserve original photo upload dates
- No support for photo metadata transfer
- Maximum file size limited by available RAM

# Cloud Migration System Design

## Architecture Diagram

```mermaid
graph TB
    subgraph "On-Premises"
        LB[Load Balancer]
        APP[Legacy Applications]
        DB[(Database)]
        DP[Data Pipeline]
    end

    subgraph "Cloud Infrastructure"
        CLB[Cloud Load Balancer]
        subgraph "Application Layer"
            API[API Gateway]
            MSV[Microservices]
            CONT[Containers]
        end
        subgraph "Data Layer"
            CDB[(Cloud Database)]
            CACHE[Cache]
            ETL[ETL Process]
            DV[Data Validation]
        end
        subgraph "Security"
            IAM[Identity & Access Management]
            WAF[Web Application Firewall]
            ENC[Encryption Service]
        end
        MON[Monitoring & Logging]
    end

    LB --> APP
    APP --> DB
    DB --> DP
    DP --> ETL
    ETL --> CDB
    ETL --> DV
    DV --> MON
    CLB --> API
    API --> MSV
    MSV --> CONT
    CONT --> CDB
    CDB --> CACHE
    WAF --> API
    IAM --> MSV
    ENC --> CDB
```

## Components Description

1. **On-Premises Infrastructure**
   - Legacy applications and databases that need to be migrated
   - Existing load balancer for traffic distribution

2. **Cloud Infrastructure**
   - Cloud Load Balancer for traffic distribution
   - API Gateway for request routing and management
   - Containerized microservices architecture
   - Cloud-native database solutions
   - Caching layer for performance optimization
   - Security components (IAM, WAF)
   - Monitoring and logging system

## Data Migration Architecture

### Data Transfer Pipeline
1. **Source Connection**
   - Database connectors for various source systems
   - Configurable batch sizes and throttling
   - Connection pool management

2. **ETL Process**
   - Incremental data extraction
   - Schema mapping and transformation
   - Data type conversion and normalization
   - Parallel processing capabilities

3. **Validation Layer**
   - Checksum verification
   - Record count validation
   - Data integrity checks
   - Error logging and reporting

4. **Performance Considerations**
   - Batch processing optimization
   - Network bandwidth management
   - Resource utilization monitoring
   - Retry mechanism with exponential backoff

## Migration Strategy

The migration will follow a phased approach:
1. Infrastructure setup in cloud
2. Data migration
3. Application containerization
4. Gradual traffic shift
5. Legacy system decommissioning

## Security Considerations

- All data encrypted in transit and at rest
- IAM policies for access control
- Web Application Firewall for threat protection
- Regular security audits and compliance checks

## Data Transfer Logic

The data transfer process is managed by the `cloud_transfer.py` script, which implements the following business logic:

### Transfer Workflow

1. **Pre-transfer Validation**
   - Source system availability check
   - Destination system capacity verification
   - Network bandwidth assessment
   - Required permissions validation

2. **Data Extraction Process**
   ```python
   def extract_data():
       - Implement connection pooling
       - Use configurable batch sizes (default: 1000 records)
       - Apply source-specific filters
       - Track extraction progress
       - Generate extraction metrics
   ```

3. **Transformation Rules**
   - Schema mapping based on configuration
   - Data type conversions
   - Field normalization
   - Business logic application
   - Data enrichment

4. **Loading Strategy**
   ```python
   def load_data():
       - Bulk insert optimization
       - Transaction management
       - Conflict resolution
       - Progress tracking
       - Performance metrics collection
   ```

### Business Rules Implementation

1. **Data Prioritization**
   - Critical business data first
   - Historical data in phases
   - Dependencies management
   - Resource allocation based on priority

2. **Validation Checkpoints**
   - Source-target record count match
   - Data integrity verification
   - Business rule compliance
   - Referential integrity checks
   - Custom validation rules

3. **Error Management**
   ```python
   def handle_errors():
       - Retry logic with exponential backoff
       - Error categorization
       - Notification system
       - Recovery procedures
       - Audit logging
   ```

### Performance Optimization

1. **Resource Management**
   - Dynamic scaling of resources
   - Load balancing
   - Memory optimization
   - Connection pooling
   - Batch size tuning

2. **Monitoring and Metrics**
   - Transfer speed tracking
   - Resource utilization
   - Error rates
   - Processing time
   - Success/failure ratios

### Rollback Procedures

1. **Checkpoint System**
   - Regular state snapshots
   - Transaction logging
   - Recovery points creation
   - Version control

2. **Recovery Process**
   ```python
   def rollback_transfer():
       - Identify failure point
       - Restore to last checkpoint
       - Validate restored state
       - Resume transfer
   ```

## Business Continuity

1. **Zero Downtime Strategy**
   - Parallel processing
   - Shadow writing
   - Progressive cutover
   - Fallback mechanisms

2. **Data Consistency**
   - ACID compliance
   - Eventually consistent model
   - Conflict resolution
   - Data reconciliation
