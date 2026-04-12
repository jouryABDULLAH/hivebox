# HiveBox

  

HiveBox is a platform for tracking the environmental sensor data from [openSenseMap](https://opensensemap.org/).

  
  

## Setup

  

1. Clone the repository

2. Create a virtual environment: `python -m venv venv`

3. Activate it: `source venv/bin/activate`

4. Install dependencies: `pip install -r requirements.txt`

5. Copy `.env.example` to `.env` and fill in your senseBox IDs

  
## Versioning

This project uses Semantic Versioning (SemVer).
Current version: v0.0.1


- MAJOR: Breaking changes  
- MINOR: New features  
- PATCH: Bug fixes  


## Testing

> *Documentation will be updated as the project develops.*

The current version of this project includes a simple version-printing application.

To test that the application works correctly inside a Docker container:

1. Build the Docker image:<br>
`docker build -t hivebox:0.0.1 .`

2. Rin the container:<br>
`docker run hivebox:0.0.1 `

3. Verify the output:<br>
The container should print the current application version:
`0.0.1`
