variable "region" {
  description = "AWS region"
  default = "eu-west-1"
  type        = string
}

variable "key_pair_name" {
  description = "Name of the AWS key pair"
  type        = string
  default = "k8s-test"
}

variable "vpc_id" {
  description = "VPC id"
  type        = string
}

variable "subnets" {
  description = "subnets"
  type        = list(string)
}
