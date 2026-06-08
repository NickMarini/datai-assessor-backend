variable "project_id" {
  description = "The GCP Project ID passed from CI/CD variables"
  type        = string
}

variable "region" {
  description = "The default GCP region"
  type        = string
  default     = "europe-west6"
}

variable "environment" {
  description = "Deployment environment (dev or prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Environment must be 'dev' or 'prod'."
  }
}

variable "api_image" {
  description = "The Docker image to deploy to Cloud Run"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder to solve the chicken-and-egg problem
}