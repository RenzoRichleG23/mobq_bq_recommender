#!/bin/bash
PROJECT_MAIN=p-indgdb-sfc-p29t
GCP_PROJECTS=('p-indgdb-ido-5oi9' 'd-indgdb-inr-d97v' 'p-indgdb-inr-h44l' 'p-indgdb-ago-y83k' 'd-indgdb-ago-d33v' 'p-indgdb-bil-b99u' 'p-indgdb-ipb-0ki7' 'p-indgdb-ipv-5oi9' 'p-indgdb-inr-x49l' 'p-indgdb-sfc-p29t' 'p-indgdb-pbi-r60p' 'd-indgdb-pbi-a34z' 'e-indgdb-api-a12a' 'e-indgdb-aat-a14b' 'd-indgdb-stg-a28p' 'e-indgdb-ppg-b29c' 'e-indgdb-vmc-a22b' 'e-indgdb-pla-a07a' 'e-indgdb-pla-a16a' 'prd-inr-data-sensitive-343514')
SERVICE_ACCOUNT=bq-reservation-admin@e-indgdb-api-a12a.iam.gserviceaccount.com

gcloud iam roles create indgdb_data_mobq_bq_recommender --project=$PROJECT_MAIN \
    --file=mobq_reservation_role.yml

gcloud projects add-iam-policy-binding $PROJECT_MAIN \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=projects/$PROJECT_MAIN/roles/indgdb_data_mobq_bq_recommender

gcloud projects add-iam-policy-binding "$PROJECT" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"

for PROJECT in "${GCP_PROJECTS[@]}"
do
    gcloud projects add-iam-policy-binding "$PROJECT" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/recommender.bigqueryPartitionClusterViewer"

    gcloud projects add-iam-policy-binding "$PROJECT" \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/bigquery.dataViewer"
done