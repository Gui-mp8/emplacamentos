from google.cloud import bigquery
import pandas as pd
import pandas_gbq

class BigQueryTable():
    def __init__(self, config:dict) -> None:
        self.config = config
        self.client = bigquery.Client(project=self.config['project_name'])

    def create_table(self, df: pd.DataFrame, table_name: str) -> bigquery.Table:
        table_id = f"{self.config['project_name']}.{self.config['dataset_name']}.{table_name}"

        return pandas_gbq.to_gbq(df, destination_table=table_id, project_id=self.config["project_name"], if_exists="append")

    # def drop_table(self, table_name: str):
    #     table = pandas_gbq.context.get_context()
    #     table_id = f"{self.config['project_name']}.{self.config['dataset_name']}.{table_name}"
    #     return pandas_gbq.bq.delete_table(table_id, context=table)



    # def writing_data(self, df, current_month):
    #     # Check if the current month (YYYY-MM) exists in the table
    #     table_id = f"{self.config['project_name']}.{self.config['dataset_name']}.{self.table_name}"
    #     sql_query = f"SELECT COUNT(*) FROM {table_id} WHERE mes_referencia = '{current_month}'"
    #     query_job = self.client.query(sql_query)
    #     results = query_job.result()
    #     count = next(results)[0]

    #     if count == 0:
    #         return to_gbq(df, destination_table=table_id, project_id=self.config["project_name"], if_exists="append")

    #     else:
    #         print(f"Data for {current_month} already exists in the table.")