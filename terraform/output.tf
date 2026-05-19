
output "cluster_name" {
  value = google_container_cluster.hivebox_cluster.name
}

output "cluster_location" {
  value = google_container_cluster.hivebox_cluster.location
}

output "connect_command" {
  value = "gcloud container clusters get-credentials ${google_container_cluster.hivebox_cluster.name} --region ${google_container_cluster.hivebox_cluster.location} --project ${var.project_id}"
}