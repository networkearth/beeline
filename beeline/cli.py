import click

from beeline.deployment.prep import prep_for_deploy as prep_for_deploy_func

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
