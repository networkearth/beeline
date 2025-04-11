import click

from beeline.deployment.prep import prep_for_deploy as prep_for_deploy_func
from beeline.flying.fly import fly as fly_func
from beeline.flying.fly import list_job_definitions as list_job_definitions_func

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
    list_job_definitions_func()

@cli.command()
@click.argument('job_definition')
def fly(job_definition):
    """
    Run a job!
    """
    fly_func(job_definition)
