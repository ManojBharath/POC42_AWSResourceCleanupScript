output "instance_ids" {
  description = "IDs of created EC2 instances"
  value       = aws_instance.instances[*].id
}

output "volume_ids" {
  description = "IDs of created EBS volumes"
  value       = aws_ebs_volume.volumes[*].id
}

output "snapshot_ids" {
  description = "IDs of created snapshots"
  value       = aws_ebs_snapshot.snapshots[*].id
}

