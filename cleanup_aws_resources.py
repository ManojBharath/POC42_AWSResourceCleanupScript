#!/usr/bin/env python3
"""
Simple AWS Resource Cleanup Script
Identifies and removes:
- Stopped EC2 instances
- Unattached EBS volumes
- Snapshots (optional - can be filtered)
"""
# import the python dependencies
import boto3
import sys
import os
from botocore.exceptions import ClientError

# Get region from environment variable or use default
aws_region = os.environ.get('AWS_REGION', 'ap-south-2')

# Get AWS profile from environment or use 'authprofile'
aws_profile = os.environ.get('AWS_PROFILE', 'authprofile')

# Create session with named profile
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)

# Initialize AWS clients with session
ec2 = session.client('ec2')
ec2_resource = session.resource('ec2')

# function to fetch all the stopped Instances(EC2)
def get_stopped_instances():
    """Get all stopped EC2 instances"""
    try:
        instances = []
        paginator = ec2.get_paginator('describe_instances')
        
        # Paginate through all stopped instances
        page_iterator = paginator.paginate(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )
        
        for page in page_iterator:
            for reservation in page['Reservations']:
                for instance in reservation['Instances']:
                    instances.append(instance['InstanceId'])
        
        return instances
    except ClientError as e:
        print(f"Error fetching stopped instances: {e}")
        return []

# function to fetch all Volumes (In-USE, Available)
def get_all_volumes():
    """Get all EBS volumes segregated by status"""
    try:
        available_volumes = []
        in_use_volumes = []
        paginator = ec2.get_paginator('describe_volumes')
        
        # Paginate through all volumes
        page_iterator = paginator.paginate()
        
        for page in page_iterator:
            for vol in page['Volumes']:
                vol_info = {
                    'VolumeId': vol['VolumeId'],
                    'Size': vol['Size'],
                    'State': vol['State'],
                    'AvailabilityZone': vol['AvailabilityZone'],
                    'Attachments': vol['Attachments']
                }
                
                if vol['State'] == 'available':
                    available_volumes.append(vol_info)
                elif vol['State'] == 'in-use':
                    in_use_volumes.append(vol_info)
        
        return available_volumes, in_use_volumes
    except Exception as e:
        print(f"Error fetching volumes: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return [], []

# function to fetch all snapshots
def get_orphaned_snapshots():
    """Get all snapshots (user can filter manually)"""
    try:
        snapshots = []
        paginator = ec2.get_paginator('describe_snapshots')
        
        # Paginate through all snapshots
        page_iterator = paginator.paginate(OwnerIds=['self'])
        
        for page in page_iterator:
            for snap in page['Snapshots']:
                snapshots.append(snap['SnapshotId'])
        
        return snapshots
    except ClientError as e:
        print(f"Error fetching snapshots: {e}")
        return []

# function to deleted the stopped instances
def delete_instances(instance_ids):
    """Delete stopped instances"""
    if not instance_ids:
        print("No stopped instances to delete.")
        return
    
    print(f"\nDeleting {len(instance_ids)} stopped instance(s)...")
    for instance_id in instance_ids:
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
            print(f"✓ Terminated: {instance_id}")
        except ClientError as e:
            print(f"✗ Failed to terminate {instance_id}: {e}")

# function to delete the volumes (IN-USE, Available) 
def delete_volumes(volume_info_list):
    """Delete unattached volumes"""
    if not volume_info_list:
        print("No unattached volumes to delete.")
        return
    
    print(f"\nDeleting {len(volume_info_list)} unattached volume(s)...")
    for vol_info in volume_info_list:
        volume_id = vol_info['VolumeId']
        try:
            ec2.delete_volume(VolumeId=volume_id)
            print(f"✓ Deleted: {volume_id} ({vol_info['Size']}GB)")
        except ClientError as e:
            print(f"✗ Failed to delete {volume_id}: {e}")

# function to delete the snapshots
def delete_snapshots(snapshot_ids):
    """Delete snapshots"""
    if not snapshot_ids:
        print("No snapshots to delete.")
        return
    
    print(f"\nDeleting {len(snapshot_ids)} snapshot(s)...")
    for snapshot_id in snapshot_ids:
        try:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"✓ Deleted: {snapshot_id}")
        except ClientError as e:
            print(f"✗ Failed to delete {snapshot_id}: {e}")

def main():
    """Main cleanup function"""
    print("=" * 60)
    print("AWS Resource Cleanup Script")
    print("=" * 60)
    
    # Get resources
    print("\n[1/3] Scanning for stopped instances...")
    stopped_instances = get_stopped_instances()
    print(f"Found {len(stopped_instances)} stopped instance(s): {stopped_instances}")
    
    print("\n[2/3] Scanning for EBS volumes...")
    available_volumes, in_use_volumes = get_all_volumes()
    
    print(f"\n--- AVAILABLE VOLUMES (Unattached - Safe to Delete) ---")
    if available_volumes:
        for vol in available_volumes:
            print(f"  ✓ {vol['VolumeId']} | Size: {vol['Size']}GB | Zone: {vol['AvailabilityZone']} | State: {vol['State']}")
    else:
        print("  None")
    
    print(f"\n--- IN-USE VOLUMES (Attached - Do NOT Delete) ---")
    if in_use_volumes:
        for vol in in_use_volumes:
            attachments = ", ".join([f"Instance: {att['InstanceId']}" for att in vol['Attachments']])
            print(f"  ✗ {vol['VolumeId']} | Size: {vol['Size']}GB | Zone: {vol['AvailabilityZone']} | State: {vol['State']} | {attachments}")
    else:
        print("  None")
    
    print(f"\nTotal Summary:")
    print(f"  - Available (Unattached): {len(available_volumes)}")
    print(f"  - In-Use (Attached): {len(in_use_volumes)}")
    
    print("\n[3/3] Scanning for snapshots...")
    snapshots = get_orphaned_snapshots()
    print(f"Found {len(snapshots)} snapshot(s): {snapshots}")
    
    # Ask for confirmation
    print("\n" + "=" * 60)
    response = input("Delete unattached volumes and stopped instances? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Cleanup cancelled.")
        sys.exit(0)
    
    # Delete resources
    delete_instances(stopped_instances)
    delete_volumes(available_volumes)
    delete_snapshots(snapshots)
    
    print("\n" + "=" * 60)
    print("Cleanup complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

