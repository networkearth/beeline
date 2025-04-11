"""
This script prepares for deployment by generating a job definition.
"""

import os
import shutil
import json

JOB_DEF_PARENT_FOLDER = 'job_definitions'

def sanitize(name):
    """
    Inputs:
    - name: The name to sanitize.

    Sanitize the name by replacing dots with dashes and converting to lowercase.
    """
    return name.replace('.', '-').lower()

def prep_for_deploy(container, configuration, requirements, entrypoint):
    """
    Inputs:
    - container: The name of the container to use.
    - configuration: The name of the configuration to use.
    - requirements: The name of the requirements file to use.
    - entrypoint: The name of the entrypoint script to use.

    Prepare for deployment by generating a job definition.
    """

    job_definition = '-'.join([
        sanitize(container),
        sanitize(configuration),
        sanitize(requirements),
        sanitize(entrypoint)
    ])

    configuraton_path = os.path.join('apps', 'jobs', 'configurations', f'{configuration}.json')
    assert os.path.exists(configuraton_path), f"Configuration file {configuraton_path} does not exist."

    container_path = os.path.join('apps', 'jobs', 'containers', container)
    assert os.path.exists(container_path), f"Container file {container_path} does not exist."

    requirements_path = os.path.join('apps', 'jobs', 'requirements', f'{requirements}.txt')
    assert os.path.exists(requirements_path), f"Requirements file {requirements_path} does not exist."

    entrypoint_path = os.path.join('apps', 'jobs', 'entrypoints', f'{entrypoint}.sh')
    assert os.path.exists(entrypoint_path), f"Entrypoint file {entrypoint_path} does not exist."

    if not os.path.exists(JOB_DEF_PARENT_FOLDER):
        os.makedirs(JOB_DEF_PARENT_FOLDER)
    
    job_def_folder = os.path.join(JOB_DEF_PARENT_FOLDER, job_definition)
    if not os.path.exists(job_def_folder):
        os.makedirs(job_def_folder)

    configuration_dest = os.path.join(job_def_folder, 'cdk.json')
    shutil.copy(configuraton_path, configuration_dest)

    container_dest = os.path.join(job_def_folder, 'Dockerfile')
    shutil.copy(container_path, container_dest)

    requirements_dest = os.path.join(job_def_folder, 'requirements.txt')
    shutil.copy(requirements_path, requirements_dest)

    entrypoint_dest = os.path.join(job_def_folder, 'main.sh')
    shutil.copy(entrypoint_path, entrypoint_dest)

    with open(configuration_dest, 'r') as fh:
        config = json.load(fh)

    config['context']['config']['job_name'] = job_definition

    with open(configuration_dest, 'w') as fh:
        json.dump(config, fh, indent=4)
