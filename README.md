# gcp-instance-auditor
List all instances in Google Cloud, sorted by project. You can filter by a folder number

This script can be run directly, or from the Docker container.
You can either mount in a service account JSON file, or mount in your local credentials.

# Usage Examples:
`docker run --rm -t -v ~/Downloads/service-account.json:/root/service-account.json:ro signiant/gcp-instance-auditor --folder 210998941515 --account /root/service-account.json`  

`docker run --rm -t -v ~/.config/gcloud:/root/.config/gcloud:ro signiant/gcp-instance-auditor --folder '210998941515 71318573357'`

Flags:  
--folder *GCP folder(s) to limit your search. If not given, will default to all projects*  
--account *service account JSON file to use to authenticate. If not supplied, use default application credentials*

Credentials in ~/.config/gcloud are created by the gcloud cli tool  

`gcloud auth application-default login`