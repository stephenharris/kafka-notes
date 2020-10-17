
locals {
  cluster_name = "kstream-wordcount"
}

provider "aws" {
  version = ">= 2.28.1"
  region  = var.region
}

module "eks" {
  source = "terraform-aws-modules/eks/aws"
  cluster_version = "1.17"
  cluster_name = local.cluster_name

  tags = {
    Environment = "sandbox"
    App = "kstream-wordcount"
  }

  subnets  = var.subnets
  vpc_id = var.vpc_id

  worker_groups = [
    {
      name                          = "worker-group-1"
      disk_size                     = 20
      instance_type                 = "t2.small"
      additional_userdata           = "echo foo bar"
      asg_desired_capacity          = 1
      asg_min_size = 1
      asg_max_size = 1
      additional_security_group_ids = [aws_security_group.worker_group_mgmt_one.id]
    } 
  ]
}


data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}


resource "aws_kms_key" "eks" {
  description = "EKS Secret Encryption Key"
}


resource "aws_security_group" "worker_group_mgmt_one" {
  name_prefix = "worker_group_mgmt_one"
  vpc_id      = var.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
    ]
  }
}
