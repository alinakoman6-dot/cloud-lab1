variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "db_password" {
  type      = string
  sensitive = true
}
