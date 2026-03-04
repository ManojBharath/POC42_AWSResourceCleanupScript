# AWS Resource Cleanup Script

Simple Python and Terraform setup to identify and remove stopped EC2 instances, unattached EBS volumes, and snapshots.

## Files.

### Python Script
- **cleanup_aws_resources.py**: Main cleanup script

### Terraform Files  
- **provider.tf**: AWS provider configuration
- **variables.tf**: Input variables and defaults
- **main.tf**: Resource definitions (3 instances, 3 volumes, 3 snapshots)
- **outputs.tf**: Output values after Terraform apply

## Prerequisites

### For Python Script
```bash
pip install -r requirements.txt
```

AWS credentials must be configured:
```bash
aws configure
# OR set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1
```

### For Terraform
```bash
terraform --version  # Requires v1.0+
```

## Usage

### Step 1: Create Test Resources (Optional)
```bash
cd POC42_AWSResourceCleanupScript

# Initialize Terraform
terraform init

# Review what will be created
terraform plan

# Create 3 instances, 3 volumes, 3 snapshots
terraform apply
```

### Step 2: Run Cleanup Script
```bash
python cleanup_aws_resources.py
```

The script will:
1. List all stopped instances
2. List all unattached volumes
3. List all snapshots
4. Ask for confirmation before deleting
5. Delete selected resources

### Step 3: Clean Up Test Infrastructure
```bash
terraform destroy
```

## What the Script Does

### Identifies:
- **Stopped EC2 Instances**: Instances in "stopped" state
- **Unattached Volumes**: Volumes with "available" status
- **Snapshots**: All user-owned snapshots (review before deleting)

### Operations:
- Lists resources before deletion
- Asks for user confirmation
- Terminates instances
- Deletes volumes
- Deletes snapshots

## Safety Features

✓ Lists resources before deletion  
✓ Requires user confirmation  
✓ Shows errors without stopping (continues with other resources)  
✓ Display item counts  

## Notes

- **AMI ID**: Default AMI (Amazon Linux 2) may vary by region. Update in `variables.tf` if needed.
- **Region**: Default is `us-east-1`. Change with `terraform apply -var="aws_region=YOUR_REGION"`
- **Cost**: EBS volumes and snapshots incur charges. Test in non-production first!
- **Snapshots**: Review manually before deletion as they may be needed for backups.

## Example Terraform Apply Output
```
instance_ids = ["i-0123456789abcdef0", "i-0123456789abcdef1", "i-0123456789abcdef2"]
volume_ids = ["vol-0123456789abcdef0", "vol-0123456789abcdef1", "vol-0123456789abcdef2"]
snapshot_ids = ["snap-0123456789abcdef0", "snap-0123456789abcdef1", "snap-0123456789abcdef2"]
stopped_instance_ids = ["i-0123456789abcdef0", "i-0123456789abcdef1"]
```
