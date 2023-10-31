from google.cloud import bigquery
import pandas as pd
from pandas_gbq import to_gbq

class BigQueryTable():
    def __init__(self, config:dict) -> None:
        self.config = config
        self.client = bigquery.Client(project=self.config['project_name'])

    def create_table(self, csv_path: pd.DataFrame, table_name: str) -> bigquery.Table:
        table_id = f"{self.config['project_name']}.{self.config['dataset_name']}.{table_name}"
        df = pd.read_csv(csv_path, delimiter=',')

        return to_gbq(df, destination_table=table_id, project_id=self.config["project_name"], if_exists="replace")