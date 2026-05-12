terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.31.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "gen-lang-client-0958813823"
  region  = "asia-south1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "gen-lang-client-0958813823-terra-bucket"
  location      = "ASIA"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}