#!/usr/bin/env python3
import boto3
import os
from pprint import pprint

BUCKET = 'sample-bucket'


endpoint_url = "http://localhost.localstack.cloud:4566"
client = boto3.client("s3", endpoint_url=endpoint_url, aws_access_key_id="accesskey", aws_secret_access_key="secretkey",)
# alternatively, to use HTTPS endpoint on port 443:
# endpoint_url = "https://localhost.localstack.cloud"

def list_buckets():
    pprint(client.list_buckets())


def list_objects():
    pprint(client.list_objects_v2(Bucket=BUCKET))


def upload(source:str):
    pprint(client.upload_file(source, BUCKET, os.path.split(source)[1]))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode')
    parser.add_argument('--source', '-s')
    args = parser.parse_args()

    match args.mode:
        case 'list-buckets':
            list_buckets()
        case 'list-objects':
            list_objects()
        case 'upload':
            upload(args.source)
        case default:
            print(f'unknown mode: {args.mode}')
