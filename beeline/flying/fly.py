"""
Everything we need to fly!
"""

import os
import boto3

def list_job_definitions():
    """
    List all job definitions in the AWS Batch service and 
    retrieve the ones that start with 'beeline'.
    """
    client = boto3.client('batch', 'us-east-1')
    response = client.describe_job_definitions()
    job_defs = sorted([job_definition['jobDefinitionName'] for job_definition in response['jobDefinitions']])
    for job_def in job_defs:
        if job_def.startswith('beeline'): print(job_def)

def fly(job_definition, script_path, config):
    """
    Inputs:
    - job_definition: The name of the job definition to use.
    - script_path: The path to the script to run.
    - config: A dictionary containing the configuration for the job.
    
    Triggers the AWS Batch job with the specified job definition and script.
    """

    name = config['name']
    output_bucket = config['output_bucket']
    input_bucket = config['input_bucket']
    prefix = config['input_prefix']

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
                f"{name}.{extension}", name, output_bucket,
                input_bucket, prefix
            ]
        },
    )

def pull_script(script):
    """
    Inputs:
    - script: The name of the script to pull from S3.

    Downloads the specified script from S3 and saves it locally.
    """

    s3 = boto3.client('s3')
    bucket_name = 'beeline-wings'
    script_path = "script.R"
    s3.download_file(bucket_name, script, script_path)

def save_outputs(name, output_bucket):
    """
    Inputs:
    - name: The name of the job.
    - output_bucket: The name of the S3 bucket to save outputs to.

    Uploads all files from the 'outputs' directory to the specified S3 bucket.
    """

    file_paths = set()
    for root, _, files in os.walk('outputs'):
        for file in files:
            file_paths.add(os.path.join(root, file))
    
    s3 = boto3.client('s3')
    bucket_name = f'beeline-{output_bucket}'

    for file_path in file_paths:
        upload_path = os.path.join(name, '/'.join(file_path.split('/')[1:]))
        s3.upload_file(file_path, bucket_name, upload_path)

def pull_inputs(input_bucket, prefix):
    """
    Inputs:
    - input_bucket: The name of the S3 bucket to pull inputs from.
    - prefix: The prefix to filter the objects in the S3 bucket.

    Downloads all files from the specified S3 bucket and prefix to the local 'inputs' directory.
    """

    assert prefix.endswith('/'), "Prefix must end with a '/'"

    s3 = boto3.client('s3')
    bucket_name = f'beeline-{input_bucket}'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].endswith('/'): continue
            key = obj['Key']
            local_path = os.path.join(*(['inputs'] + key.split('/')[1:]))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(bucket_name, key, local_path)
