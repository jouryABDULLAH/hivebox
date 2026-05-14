# HiveBox

  
Real-time environmental monitoring system that aggregates and processes sensor data from [openSenseMap](https://opensensemap.org/) IoT devices.
 


## Objective
HiveBox provides a RESTful API for querying temperature data from distributed senseBox sensors, with built-in caching, storage, and observability features.

## Features

- **Real-time data aggregation** from multiple openSenseMap sensors
- **Intelligent caching** using Redis/Valkey to reduce external API calls
- **Persistent storage** with MinIO for historical data analysis  
- **Production-ready deployment** on Google Kubernetes Engine
- **Automated CI/CD pipeline** with security scanning and quality gates
- **Infrastructure as Code** using Terraform and Helm

  
## API Endpoints
- `GET /version` - Application version
- `GET /temperature` - Current temperature from configured sensors
- `GET /metrics` - Prometheus metrics
- `POST /store` - Manual data persistence triggers

## Deployment
Deployed on Google Kubernetes Engine with:
- Helm chart for application packaging
- Terraform for infrastructure provisioning
- Automated CI/CD via GitHub Actions
- Horizontal pod autoscaling

## Versioning
This project uses Semantic Versioning (SemVer).
Current version: v0.0.1
- MAJOR: Breaking changes  
- MINOR: New features  
- PATCH: Bug fixes  

## Notes
*Documentation will expand as the system evolves.*
