variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-2"
}

variable "availability_zone" {
  description = "AWS availability zone"
  type        = string
  default     = "ap-south-2a"
}

variable "ami_id" {
  description = "AMI ID for EC2 instances (Amazon Linux 2)"
  type        = string
  default     = "ami-02774d409be696d81" # Note: Update AMI ID for ap-south-2 region
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "volume_size" {
  description = "EBS volume size in GB"
  type        = number
  default     = 10
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "test"
}

