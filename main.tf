# Create 3 EBS Volumes
resource "aws_ebs_volume" "volumes" {
  count             = 3
  availability_zone = var.availability_zone
  size              = var.volume_size
  encrypted         = false

  tags = {
    Name        = "cleanup-test-volume-${count.index + 1}"
    Environment = var.environment
    Purpose     = "cleanup-testing"
  }
}

# Create 3 EC2 Instances
resource "aws_instance" "instances" {
  count             = 3
  ami               = var.ami_id
  instance_type     = var.instance_type
  availability_zone = var.availability_zone

  tags = {
    Name        = "cleanup-test-instance-${count.index + 1}"
    Environment = var.environment
    Purpose     = "cleanup-testing"
  }
}

# Create 3 Snapshots from the volumes
resource "aws_ebs_snapshot" "snapshots" {
  count       = 3
  volume_id   = aws_ebs_volume.volumes[count.index].id
  description = "Snapshot for cleanup-test-volume-${count.index + 1}"

  tags = {
    Name        = "cleanup-test-snapshot-${count.index + 1}"
    Environment = var.environment
    Purpose     = "cleanup-testing"
  }
}

