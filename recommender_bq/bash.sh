REGION='us-central1'
CLOUD_RUN_NAME='mobq_inr_recommender_bq'
SERVICE_ACCOUNT_CLOUD_RUN=''

echo ""
echo "--- INIT CONFIGURATION ---"
echo "--- ------------------ ---"
echo ""

PROJECT_ID=$(gcloud config get-value project)
echo ""
echo "PROJECT: $PROJECT_ID"

gcloud config set run/region $REGION

echo ""
echo "--- DEPLOY CLOUD RUN ($CLOUD_RUN_NAME) ---"
echo "---"
echo ""

echo "- BUILD DOCKER IMAGE"
gcloud builds submit --tag gcr.io/$PROJECT_ID/$CLOUD_RUN_NAME

echo ""
echo "- DEPLOY CLOUD RUN"
echo "SA: $SERVICE_ACCOUNT_CLOUD_RUN"

gcloud beta run jobs create ${CLOUD_RUN_NAME} \
    --image gcr.io/$PROJECT_ID/${CLOUD_RUN_NAME}\
    --tasks 1 \
    --cpu=1 \
    --max-retries 0 \
    --region $REGION \
    --project=$PROJECT_ID \
    --service-account $SERVICE_ACCOUNT_CLOUD_RUN \
  
#MULTILINE-COMMENT
echo ""
echo "--FINISH!"