import boto3
import os

REGION_NAME = os.environ['RegionName']

ALLOWED_SERVICE_NAMES = [ 's3', 'dynamodb' ]
ALLOWED_KEYS = [ 'Cidrs', 'PrefixListId' ]

def get_available_regions():
    client = boto3.client('ec2')
    response = client.describe_regions()
    regions = []
    for r in response.get('Regions', []):
        region_name = r.get('RegionName', None)
        if region_name != None:
            regions.append(region_name)
    return regions

def get_prefix_lists_detail(region_name, service_name):
    client = boto3.client('ec2', region_name=region_name)
    filters = [
        {
            "Name" : "ByService",
            "Values" : [
                "com.amazonaws.{}.{}".format(region_name.lower(), service_name.lower())    
            ]
        }
    ]
    prefix_lists = []
    next_token = None
    resp = None
    while True:
        
        if next_token:
            resp = client.describe_prefix_lists(NextToken=next_token)
        else:
            resp = client.describe_prefix_lists()
        if len(resp.get('PrefixLists', [])):
            prefix_lists = prefix_lists + resp['PrefixLists']
        next_token = resp.get('NextToken', None)
        if not next_token:
            break
    return prefix_lists

def get_prefix_lists(region_name, service_name, keys):
    results = []
    details = get_prefix_lists_detail(region_name, service_name)
    for item in details:
        if service_name in item['PrefixListName']:
            ret_item = { 'PrefixListName' : item['PrefixListName'] }
            for k in keys:
                ret_item[k] = item.get(k, '')
            results.append(ret_item)
    return results

def get_region(event):
    region = event.get('RegionName', REGION_NAME)
    if region not in get_available_regions():
        raise Exception('Invalid RegionName {} specified.  Must be one of {}'.format(region, get_available_regions()))
    return region

def get_service(event):
    service = event.get('ServiceName', None)
    if service == None:
        raise Exception('ServiceName must be specified in the request')
    service = str(service).lower()
    if service not in ALLOWED_SERVICE_NAMES:
        raise Exception('Invalid ServiceName specified.  Must be one of: {}'.format(ALLOWED_SERVICE_NAMES))
    return service

def get_keys(event):
    keys = event.get('Keys', ALLOWED_KEYS)
    for key in keys:
        if key not in ALLOWED_KEYS:
            raise Exception('Invalid Key {} specified.  Must be one of: {}'.format(key, ALLOWED_KEYS))
    return keys

def process(event):
    region_name = get_region(event)
    service_name = get_service(event)
    keys = get_keys(event)
    return get_prefix_lists(region_name, service_name, keys)

def lambda_handler(event, context):
   return process(event)
