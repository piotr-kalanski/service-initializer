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
- Extensibility - it is relativly easy to add support for automating new type of tasks
- Built in tasks ([see more](#supported-tasks))

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

## Supported tasks

### Create AWS Code Commit repository

```yaml
  steps:
  - name: Step name
    task:
      type: AWS/CodeCommit/CreateRepository

  [...]
```

## Add new task

Required steps:
1. Create new Python class
2. Add mapping from expected task type name to Task class in [WorkflowConfigurationReader](./src/workflow/configuration/workflow_configuration_reader.py).

### Create new Python class

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

### Add mapping from expected task type name to Task class

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
