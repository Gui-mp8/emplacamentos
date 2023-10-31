from google.cloud import bigquery

class BigQueryDataset():
    def __init__(self, config: dict) -> None:
        self.config = config
        self.client = bigquery.Client()


    def creation(self, dataset_name: str) -> bigquery.Dataset:
        dataset_id = bigquery.Dataset(f"{self.config['project_name']}.{dataset_name}")
        dataset_id.location = self.config["dataset_location"]

        return self.client.create_dataset(dataset_id, timeout=30)
        # print(f"Created dataset {self.client.project}.{dataset.dataset_id}")