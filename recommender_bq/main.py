from google.cloud import recommender_v1
import pandas as pd
from google.cloud import bigquery
from google.cloud import secretmanager
import datetime
import json
import constants
import google.auth.transport.requests
import google.oauth2.id_token
from google.cloud import run_v2
from google.oauth2.credentials import Credentials
from google.auth import impersonated_credentials
from google.cloud import secretmanager
from google.auth.transport.requests import Request, AuthorizedSession
import os

# Function to extract dataset_id and table_id
def extract_dataset_table_ids(route):
    parts = route.split("/")
    dataset_id = parts[-3] if len(parts) >= 3 else None
    table_id = parts[-1] if len(parts) >= 1 else None
    return dataset_id, table_id

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    secret_version = client.access_secret_version(request={"name": secret_name})
    return secret_version.payload.data.decode("UTF-8")

def list_recommendations(secret_path):
    zones = ["us","us-central1-a", "us-central1-b", "us-central1-c"]
    projects = get_secret(secret_path)
    projects_json = json.loads(projects)
    project_ids = projects_json['projects'].split(',')
    project_ids = [project.strip("'") for project in project_ids]

     # Crear el cliente
    client = recommender_v1.RecommenderClient()
    tabla = []
    # Get the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Iteramos sobre proyectos y zonas
    for project in project_ids:
        for zone in zones:
            request = recommender_v1.ListRecommendationsRequest(
                parent="projects/"+project+"/locations/"+zone+"/recommenders/google.bigquery.table.PartitionClusterRecommender"
            )
            # Make the request
            recommendations = client.list_recommendations(request=request)
            
            for rec in recommendations:
                if rec.recommender_subtype=="CLUSTER":
                    column = rec.content.overview['clusterColumns'][0]
                    partitionUnit = ''
                if rec.recommender_subtype=="PARTITION":
                    partitionUnit = rec.content.overview['partitionTimeUnit']
                    column = rec.content.overview['partitionColumn']
                
                slotsProcessed = int(rec.content.overview['slotMsSavedMonthly'])
                slotHourSaved = (slotsProcessed/60000)
                slotHourCost = slotHourSaved*0.04

                bytesProcessed = int(rec.content.overview['bytesSavedMonthly'])
                tbSaved = bytesProcessed / (1099511627776) # Conversion a GB
                tbCost = tbSaved * 6.25 # Conversion a TB

                route = str(rec.content.operation_groups[0].operations[0].resource)
                dataset_id, table_id = extract_dataset_table_ids(route)

                tabla.append({
                    'project_id': str(project),
                    'dataset_id':dataset_id,
                    'table_id':table_id,
                    'recommender_subtype': str(rec.recommender_subtype),
                    'primary_impact':str(rec.primary_impact),
                    'additional_impact':str(rec.additional_impact[0]),
                    'priority':str(rec.priority),
                    'column': str(column),
                    'partitionUnit': str(partitionUnit),
                    'slotHourSavedMonthly':slotHourSaved,
                    'slotCostSaved':slotHourCost,
                    'terabytesSavedMonthly':tbSaved,
                    'onDemandCostSaved':tbCost,
                    'export_date': current_date 
                })
            
    # Create the final DataFrame with descriptions
    df_tabla = pd.DataFrame(tabla)

    return df_tabla

def insert_data_into_bigquery(df, project_id, dataset_id, table_id, table_id_hist):
    # Initialize a BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the job configuration
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True  # Automatically detect schema from DataFrame
    )
    table_id = project_id + "." + dataset_id + "." + table_id
    # Insert data into the BigQuery table
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete

    print(f"Inserted {len(df)} rows into {project_id}:{dataset_id}.{table_id}")

    # Inserción en la tabla histórica
    job_config_v2 = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True  
    )
    table_id_v2 = 'mobq_partitioncluster_recommendations_hist'
    table_id_v2 = project_id + "." + dataset_id + "." + table_id_v2
    # Insert data into the BigQuery table
    job = client.load_table_from_dataframe(df, table_id_v2, job_config=job_config_v2)
    job.result()  # Wait for the job to complete

    print(f"Inserted {len(df)} rows into {project_id}:{dataset_id}.{table_id_hist}")


if __name__ == "__main__":
    # Obtengo variables del JSON de entrada
    with open(constants.JSON_ENTRADA, 'r') as file:
        json_entrada = json.load(file)

    project_id = json_entrada['project_id']
    dataset_id = json_entrada['dataset_id']
    table_id = json_entrada['table_id']
    table_id_hist = json_entrada['table_id_hist']
    secret_path = json_entrada['secret_path']

    df = list_recommendations(secret_path)
    insert_data_into_bigquery(df,project_id,dataset_id,table_id,table_id_hist)