variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "jwt_secret" {
  type      = string
  sensitive = true
}

variable "alert_email" {
  type        = string
  description = "komar.alina080@gmail.com"
}

variable "github_repo" {
  type    = string
  default = "alinakoman6-dot/cloud-lab1"
}
