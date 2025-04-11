import click
import json

from beeline.deployment.prep import prep_for_deploy as prep_for_deploy_func
from beeline.flying.fly import fly as fly_func
from beeline.flying.fly import list_job_definitions as list_job_definitions_func
from beeline.flying.fly import pull_script as pull_script_func
from beeline.flying.fly import save_outputs as save_outputs_func
from beeline.flying.fly import pull_inputs as pull_inputs_func

@click.group()
def cli():
    pass

@cli.command()
@click.argument('container')
@click.argument('configuration')
@click.argument('requirements')
@click.argument('entrypoint')
def prep_for_deploy(container, configuration, requirements, entrypoint):
    """
    Prepare for deployment by generating a job definition.
    """
    prep_for_deploy_func(container, configuration, requirements, entrypoint)

@cli.command()
def options():
    """
    List all job definitions in the AWS Batch service 
    and retrieve the ones that start with 'beeline'.
    """
    list_job_definitions_func()

@cli.command()
@click.argument('job_definition')
@click.argument('script_path')
@click.argument('config_path')
def fly(job_definition, script_path, config_path):
    """
    Run a job!
    """
    with open(config_path, 'r') as fh:
        config = json.load(fh)
    fly_func(job_definition, script_path, config)

@cli.command()
@click.argument('script')
def pull_script(script):
    """
    Pull a script from S3.
    """
    pull_script_func(script)

@cli.command()
@click.argument('name')
@click.argument('output_bucket')
def save_outputs(name, output_bucket):
    """
    Save outputs to S3.
    """
    save_outputs_func(name, output_bucket)

@cli.command()
@click.argument('input_bucket')
@click.argument('prefix')
def pull_inputs(input_bucket, prefix):
    """
    Load inputs from S3.
    """
    pull_inputs_func(input_bucket, prefix)
