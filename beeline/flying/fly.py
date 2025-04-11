import os
import boto3

def list_job_definitions():
    client = boto3.client('batch', 'us-east-1')
    response = client.describe_job_definitions()
    job_defs = sorted([job_definition['jobDefinitionName'] for job_definition in response['jobDefinitions']])
    for job_def in job_defs:
        if job_def.startswith('beeline'): print(job_def)

def fly(job_definition, script_path, config):
    name = config['name']
    output_bucket = config['output_bucket']

    # upload the script to S3
    s3 = boto3.client('s3')
    bucket_name = 'beeline-wings'
    extension = script_path.split('.')[-1]
    s3.upload_file(script_path, bucket_name, f"{name}.{extension}")

    # submit the job
    client = boto3.client('batch', 'us-east-1')
    client.submit_job(
        jobName=f"{job_definition}",
        jobQueue="beeline-job-queue",
        jobDefinition=job_definition,
        containerOverrides={
            "command": [
                f"{name}.{extension}", name, output_bucket
            ]
        },
    )

def pull_script(script):
    s3 = boto3.client('s3')
    bucket_name = 'beeline-wings'
    script_path = "script.R"
    s3.download_file(bucket_name, script, script_path)

def save_outputs(name, output_bucket):
    file_paths = set()
    for root, _, files in os.walk('output'):
        for file in files:
            file_paths.add(os.path.join(root, file))
    
    s3 = boto3.client('s3')
    bucket_name = f'beeline-{output_bucket}'

    for file_path in file_paths:
        upload_path = os.path.join(name, '/'.join(*file_path.split('/')[1:]))
        s3.upload_file(file_path, bucket_name, upload_path)
