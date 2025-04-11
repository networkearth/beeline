import boto3

def list_job_definitions():
    client = boto3.client('batch', 'us-east-1')
    response = client.describe_job_definitions()
    job_defs = sorted([job_definition['jobDefinitionName'] for job_definition in response['jobDefinitions']])
    for job_def in job_defs:
        if job_def.startswith('beeline'): print(job_def)

def fly(job_definition):
    client = boto3.client('batch', 'us-east-1')
    client.submit_job(
        jobName=f"{job_definition}",
        jobQueue="beeline-job-queue",
        jobDefinition=job_definition,
    )