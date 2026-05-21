variable "project_id" {
  description = "The target Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy E2 / GPU nodes"
  type        = string
  default     = "us-central1"
}
