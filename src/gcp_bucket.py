from google.cloud import storage


class MHGCPStorage:
    def __init__(self):
        client = storage.Client()

    def create_bucket_if_not_exist(self, bucket_name):
        pass