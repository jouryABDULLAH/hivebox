from io import BytesIO
from minio import Minio
from datetime import datetime
from app.metrics import storage_operations
import json

from app.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def store_sensor_data(data: dict):
    try:     
        bucket = "hivebox-data"
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)
        
        timestamp = datetime.now().isoformat().replace(":", "-")
        filename = f"sensor-data-{timestamp}.json"
        payload = json.dumps(data, indent=2).encode('utf-8')

        minio_client.put_object(
            bucket,
            filename,
            data= BytesIO(payload),
            length=len(payload),
            content_type="application/json"
        )

        storage_operations.labels(status='success').inc()
    except Exception:
        storage_operations.labels(status='failure').inc()
        raise

# Mock MinIo <before deployment>: 
# STORAGE_DIR = "/tmp/hivebox-storage"

# def store_sensor_data(data: dict):
#     """Mock MinIO storage - writes to local filesystem"""
#     storage_dir = "C:/temp/hivebox-storage"
#     os.makedirs(storage_dir, exist_ok=True)
    
#     timestamp = datetime.now().isoformat().replace(":", "-")
#     filename = f"sensor-data-{timestamp}.json"
#     filepath = f"{storage_dir}/{filename}"
    
#     with open(filepath, 'w') as f:
#         json.dump(data, f, indent=2)
    
#     print(f"Stored data to {filepath}")