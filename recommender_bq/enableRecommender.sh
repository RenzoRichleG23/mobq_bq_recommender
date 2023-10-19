prjs=('p-indgdb-ido-5oi9' 'd-indgdb-inr-d97v' 'p-indgdb-inr-h44l' 'p-indgdb-ago-y83k' 'd-indgdb-ago-d33v' 'p-indgdb-bil-b99u' 'p-indgdb-ipb-0ki7' 
'p-indgdb-ipv-5oi9' 'p-indgdb-inr-x49l' 'p-indgdb-sfc-p29t' 'p-indgdb-pbi-r60p' 'd-indgdb-pbi-a34z' 'e-indgdb-api-a12a' 'e-indgdb-aat-a14b' 
'd-indgdb-stg-a28p' 'e-indgdb-ppg-b29c' 'e-indgdb-vmc-a22b' 'e-indgdb-pla-a07a' 'e-indgdb-pla-a16a' 'prd-inr-data-sensitive-343514')
token=$(gcloud auth print-access-token)
for i in "${prjs[@]}"
    do
        echo "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" 
        echo "Setting Project: $i" 
        echo $(gcloud config set project $i )
        echo $(gcloud services enable recommender.googleapis.com)
    done