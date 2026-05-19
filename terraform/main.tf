resource "google_container_cluster" "hivebox_cluster" {
  name     = var.cluster_name
  location = var.region

  deletion_protection = false
  enable_autopilot = true

  ip_allocation_policy {
    cluster_ipv4_cidr_block  = "/17"
    services_ipv4_cidr_block = "/22"
  }
}

