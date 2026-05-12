variable "cred" {
  description = "My credentials"
  default     = "./keys/my-cred.json"
}

variable "project" {
  description = "The project name"
  default     = "gen-lang-client-0958813823"
}

variable "region" {
  description = "The region"
  default     = "asia-south1"
}

variable "gcs_storage_bucket_name" {
  description = "Bucket name"
  default     = "gen-lang-client-0958813823-terra-bucket"
}

variable "location" {
  description = "Location of the resource"
  default     = "ASIA"
}