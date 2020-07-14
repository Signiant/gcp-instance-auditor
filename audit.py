import argparse
import warnings
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

warnings.filterwarnings('ignore', 'Your application has authenticated using end user credentials')


def list_projects(credentials, parent):
    if credentials is not None:
        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
    else:
        service = discovery.build('cloudresourcemanager', 'v1')
    request = service.projects().list()
    response = request.execute()
    all_projects = response.get('projects', [])
    trimmed_list = []
    for project in all_projects:
        if (not parent) or project['parent']['id'] in parent:
            trimmed_list.append(project)
    return sorted(trimmed_list, key=lambda i: i['projectId'])


def list_instances(credentials, project_id):
    instance_list = []
    if credentials is not None:
        compute = discovery.build('compute', 'v1', credentials=credentials)
    else:
        compute = discovery.build('compute', 'v1')
    try:
        zone_list = compute.zones().list(project=project_id).execute()
    except HttpError as err:
        if err.resp.status in [403, 404]:
            zone_list = None
        else:
            raise
    if zone_list:
        for zone in zone_list['items']:
            project_instances = compute.instances().list(project=project_id, zone=zone['name']).execute()
            if 'items' in project_instances:
                for instance in project_instances['items']:
                    instance_list.append(instance)
    return instance_list


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Get all instances running in GCP, grouped by project')
    parser.add_argument('--folder', help='Limit audit to projects in these folders.')
    parser.add_argument('--account', help='Full path to service account JSON file')
    args = parser.parse_args()

    if args.folder is not None:
        parent_folder = args.folder
        print('Only getting instances in projects: %s' % parent_folder)
    else:
        parent_folder = None
        print('No folder filter, getting instances from all projects')

    if args.account is not None:
        credentials = service_account.Credentials.from_service_account_file(args.account)
    else:
        credentials = None

    project_list = list_projects(credentials, parent_folder)
    total = 0
    for project in project_list:
        instances = list_instances(credentials, project['projectId'])
        if instances:
            print('\nProject: %s' % project['name'])
            print('instance count: %s' % len(instances))
            total += len(instances)
            for instance in instances:
                instance_type = instance['machineType'].split('/')[-1]
                print('  %s - %s' % (instance['name'], instance_type))
    print('\n\nTotal number of instances: %s' % total)
