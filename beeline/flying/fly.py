import boto3

def list_job_definitions():
    client = boto3.client('batch', 'us-east-1')
    response = client.describe_job_definitions()
    job_defs = sorted([job_definition['jobDefinitionName'] for job_definition in response['jobDefinitions']])
    for job_def in job_defs:
        if job_def.startswith('beeline'): print(job_def)

def fly(job_definition, script_path, config):
    name = config['name']

    # upload the script to S3
    s3 = boto3.client('s3')
    bucket_name = 'beeline-wings'
    s3.upload_file(script_path, bucket_name, f"{name}.R")

    # submit the job
    client = boto3.client('batch', 'us-east-1')
    client.submit_job(
        jobName=f"{job_definition}",
        jobQueue="beeline-job-queue",
        jobDefinition=job_definition,
        containerOverrides={
            "command": [
                f"{name}.R",
            ]
        },
    )

def pull_script(script):
    s3 = boto3.client('s3')
    bucket_name = 'beeline-wings'
    script_path = "script.R"
    s3.download_file(bucket_name, script, script_path)
