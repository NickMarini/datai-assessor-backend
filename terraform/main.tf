# Centralised naming — add new resources to this map.
# Each value gets "-dev" or "-prod" appended automatically.
locals {
  env = var.environment
  name = {
    docker_repo = "datai-assessor-repo-${var.environment}"
  }
}

# 1. Enable necessary GCP APIs automatically
resource "google_project_service" "services" {
  for_each = toset([
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com"
  ])
  service            = each.key
  disable_on_destroy = false
}

# 2. Create the Docker Repository
resource "google_artifact_registry_repository" "docker_repo" {
  location      = var.region
  repository_id = local.name["docker_repo"]
  description   = "Docker repository for datai.ch applications (${local.env})"
  format        = "DOCKER"

  depends_on = [google_project_service.services]
}

# 3. Create the Cloud Run API Service
resource "google_cloud_run_v2_service" "api_service" {
  name     = "datai-assessor-api-${local.env}"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.api_image
      
      ports {
        container_port = 8080
      }
      resources {
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
      }
    }
  }

  depends_on = [google_project_service.services]
}

# 4. Make it publicly accessible (so the frontend can hit the API)
resource "google_cloud_run_v2_service_iam_member" "api_public_access" {
  project  = google_cloud_run_v2_service.api_service.project
  location = google_cloud_run_v2_service.api_service.location
  name     = google_cloud_run_v2_service.api_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}