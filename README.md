# service-initializer

Tool for initializing new service (e.g. REST API, batch job).

## Table of contents

- [Motivation](#motivation)
- [Quick start](#quick-start)
- [Concepts](#concepts)
    * [Task](#task)
    * [Step](#step)
    * [Workflow configuration](#workflow-configuration)
    * [Service metadata](#service-metadata)    
- [Architecture](#architecture)
- [Command line](#command-line)
    * [Run workflow](#run-workflow)
- [Secrets](#secrets)
- [Supported tasks](#supported-tasks)
- [Add new task](#add-new-task)

## Motivation

When you start working on new Microservice you have to in each case do multiple repetitive and boring things like: create git repository, create basic directory structure in git repository, create CI/CD pipeline, create docker registry etc.

Aim of Service Initializer is to automate such tasks so that you can start from implementing business logic.

### Benefits

Benefits of Service Initializer:
- Reduce time spent on boring and repetitive tasks
- Support microservice architecture in your organization by reducing overhead on creating new service
- Increase standardization in your team/organization
- Speed up induction process of new developer in your team
- Technology and platform agnostic - you can use it to initialize any tech stack
- Built in tasks ([see more](#supported-tasks))
- Extensibility - it is relativly easy to add support for automating new type of tasks ([see more](#add-new-task))


## Quick start

TODO

## Concepts

### Task

Task is list of actions (recipe) with desired outcome.

Example tasks:
- create git repository
- create build plan
- create deployment plan
- create Docker registry

### Step

Step is parameterized task with assigned name.

### Workflow configuration

Workflow configuration is list of steps to be executed in sequence to initialize new service.
In other words it is recipe to initialize new service.
Workflow configuration is provided in YAML format.

#### Example workflow configuration file

Example workflow configuration YAML file:

```yaml
steps:
  - name: Step1
    task:
      type: AWS/CodeCommit/CreateRepository
  - name: Step2
    task:
      type: AWS/CodePipeline/CreatePipeline
  - name: Step3
    task:
      type: AWS/ECR/CreateRepository
  - name: Step4
    task:
      type: git/PushToRepository
```

Above workflow has four steps:
- create AWS Code Commit Repository
- create Code Pipeline pipeline
- create ECR repository
- push to git repository

### Service metadata

Service metadata is list of parameters that are provided when running workflow and can be input to tasks.

Service metadata schema:
- name - service name
- description - service description
- parameters - key value pairs

#### Example service metadata file

```yaml
name: service
description: service description
parameters:
  param1: value1
  param2: value2
  param3:
    field1: 1
    field2: f2
```

## Architecture

TODO

## Command line

### Run workflow

Command to initialize new service based on provided workflow and service metadata.

    python initialize_service.py --configuration PATH_TO_WORKFLOW_CONFIGURATION.yaml --parameters PATH_TO_SERVICE_METADATA.yaml

Example:

    python initialize_service.py --configuration workflow_simple.yaml --parameters service_metadata.yaml

## Secrets

You can provide secrets (e.g. token, API key) using environment variables and/or file.

Secrets are defined in Worfklow Configuration file in section *secrets*:

```yaml
secrets:
  [...]
  
steps:
  [...]
```

In Workflow Steps you can provide reference to secret value using syntax: ```{secret:NAME_OF_SECRET}```.

Example:

```yaml
steps:
  - name: Step name
    task:
      type: TYPE
      parameters:
        token: {secret:TOKEN}
```

### Secrets provided in environment variables

You can provide mapping from name of environment variable to secret name in section ```secrets.environment```.

Example:

```yaml
secrets:
  environment:
    ENVIRONMENT_VARIABLE_NAME: API_KEY
```

### Secrets provided in file

You can provide list of files with secrets in section ```secrets.files```.

Example:

```yaml
secrets:
  files:
    - /dir1/dir2/secrets1.yaml
    - /dir1/dir2/secrets2.yaml
```
Expected file format with secrets:

```yaml
secret_key1: value1
secret_key2: value2
```

## Supported tasks

### Create AWS Code Commit repository

```yaml
  steps:
  - name: Step name
    task:
      type: AWS/CodeCommit/CreateRepository

  [...]
```

### Create ECR repository

```yaml
  steps:
  - name: Step name
    task:
      type: AWS/ECR/CreateRepository

  [...]
```

### Create AWS CloudFormation stack

Example:

```yaml
  steps:
  - name: step
    task:
      type: AWS/CloudFormation/CreateStack
      parameters:
        template_body: >
          Resources:
            S3Bucket:
              Type: AWS::S3::Bucket
              DeletionPolicy: Retain
              Properties:
                BucketName: my-bucket
        service_metadata_parameter_with_stack_name: cf_stack_name
        service_metadata_parameter_with_stack_parameters: cf_stack_parameters
        stack_parameters:
          p1: v1
          p2: v2
  [...]
```

#### Parameters:

|Parameter|Required?|Description|
|---|---|---|
|template_body|YES|CloudFormation template body|
|service_metadata_parameter_with_stack_name|YES|name of field in Service Metadata with information about Stack name|
|service_metadata_parameter_with_stack_parameters|NO|name of field in Service Metadata with dictionary of parameters for CloudFormation stack|
|stack_parameters|NO|dictionary with parameters for CloudFormation stack common for all services|

### Generate project directory using cookiecutter template

Example:

```yaml
steps:
  - name: Generate project directory using cookiecutter
    task:
      type: Cookiecutter/GenerateProjectDirectory
      parameters:
        template_url_field_name: 'cookiecutter.template_url'
        parameters_field_name: 'cookiecutter.parameters'
        output_dir: 'dir1/dir2'

  [...]
```

#### Parameters:

|Parameter|Required?|Description|
|---|---|---|
|template_url_field_name|YES|name of field in Service Metadata with url to cookiecutter template|
|parameters_field_name|YES|name of field in Service Metadata with input parameters for cookiecutter template|
|output_dir|YES|output directory where to generate project template|

### Create GitHub repository

```yaml
  steps:
  - name: Step name
    task:
      type: GitHub/CreateRepository
      parameters:
        auth_token: TOKEN
        service_metadata_parameter_with_request_body: create_github_repository_body
  [...]
```

#### Parameters:

|Parameter|Required?|Description|
|---|---|---|
|auth_token|YES|Authentication token for GitHub API (https://developer.github.com/v3/#authentication)|
|service_metadata_parameter_with_request_body|YES|Name of parameter in Service Metadata with create GitHub repository request body (https://developer.github.com/v3/repos/#create-a-repository-for-the-authenticated-user)|

### Docker run task

Generic task for running task using Docker image for task.

#### Executed Docker run command

This task executes docker command using below template:

  docker run -it --rm CUSTOM_DOCKER_OPTIONS --name SERVICE_METADATA.name --description "SERVICE_METADATA.description" --parameters "CUSTOM_TASK_PARAMETERS" --service-metadata "SERVICE_METADATA.parameters"

where:
- ``SERVICE_METADATA.name.*`` are fields values from (Service Metadata)[#service-metadata]
- ``CUSTOM_DOCKER_OPTIONS`` is custom Docker run options that can be provided in Workflow Configuration file
- ``CUSTOM_TASK_PARAMETERS`` is custom task parameters that can be provided in Workflow Configuration file

#### Example in Workflow Configuration

```yaml
  steps:
  - name: Step name
    task:
      type: Docker/Run
      parameters:
        docker_image: piotrkalanski/service-initializer-cookiecutter-task
        task_parameters:
          template_url_field_name: 'template_url'
          output_dir: '/output/'
          parameters_field_name: 'params'
        docker_run_options:
          - '-v generated_project:/output'
  [...]
```
Based on above configuration following command will be executed:

  docker run -it --rm -v generated_project:/output piotrkalanski/service-initializer-cookiecutter-task --name SERVICE_METADATA.name --description "SERVICE_METADATA.description" --parameters "{'template_url_field_name': 'template_url', 'output_dir': '/output/', 'parameters_field_name': 'params'}" --service-metadata "SERVICE_METADATA.parameters"

#### Parameters

|Parameter|Required?|Description|
|---|---|---|
|docker_image|YES|Docker image|
|task_parameters|YES|Dictionary of custom parameters for your task|
|docker_run_options|NO|Additional Docker command options e.g. for mapping volume|

#### Create custom Docker image for your task

To create custom Docker image for new task you can use base Docker image: [piotr-kalanski/service-initializer-base-docker](#https://github.com/piotr-kalanski/service-initializer-base-docker).

You can find example task using Docker image here: https://github.com/piotr-kalanski/service-initializer-cookiecutter-task.

## Add new task

There are two methods for adding new tasks:
1. Create custom Python class for task
2. Use generic [Docker run task](#docker-run-task)

### Create custom Python class for task

Required steps:
1. Create new Python class
2. Add mapping from expected task type name to Task class in [WorkflowConfigurationReader](./src/workflow/configuration/workflow_configuration_reader.py).

#### Create new Python class

Create new Python class derived from *AbstractTask* class.

You need to implement one method *execute* responsible for executing task.

```python

import logging
from tasks.abstract_task import AbstractTask
from service_metadata.model import ServiceMetadata

class New_Task(AbstractTask):
    
    def execute(self, service_metadata: ServiceMetadata):
        logging.info("Pushing to git repository")
        # TODO - implementation
```

#### Add mapping from expected task type name to Task class

Add new mapping in [WorkflowConfigurationReader](./src/workflow/configuration/workflow_configuration_reader.py):

```python

class WorkflowConfigurationReader:
    [...]
    TASKS_CLASSES = {
        [...],
        "NewTask": New_Task,
    }

    [...]

```

where *NewTask* is used in workflow configuration file, example:

```yaml
steps:
  - name: Step
    task:
      type: NewTask
```
