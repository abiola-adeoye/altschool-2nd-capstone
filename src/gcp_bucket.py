import json

from google.cloud import storage

from .log import load_logging


class MHGCPStorage:
    def __init__(self, bucket_name: str):
        self.logger = load_logging(__class__.__name__)
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.get_or_create_bucket()

    def get_or_create_bucket(self) -> 'storage.Bucket':
        bucket = self.client.bucket(self.bucket_name)
        if bucket.exists() is False:
            bucket.storage_class = 'STANDARD'
            bucket.create()
        self.logger.info(f"Bucket {self.bucket_name} is ready for use")
        return bucket

    def create_or_append_json_data(self, file_name: str, records: list[dict]):
        current_records = []
        blob = self.bucket.blob(f"{file_name}.json")
        if blob.exists():
            current_records = json.loads(blob.download_as_text())
            self.logger.info("Previous records exist, will update...")

        current_records.extend(records)
        try:
            blob.upload_from_string(json.dumps(current_records), content_type='application/json')
            self.logger.info(f"records have been pushed to {file_name}.json...")
        except Exception:
            self.logger.error(f"There was an error pushing records to {file_name}.json", exc_info=True)
