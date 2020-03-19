# service-initializer

Tool for initializing new service

## Table of contents

- [Concepts](#concepts)
    * [Task](#task)
    * [Step](#step)
    * [Workflow configuration](#workflow-configuration)
    * [Service metadata](#service-metadata)
- [Architecture](#architecture)
- [Command line](#command-line)
    * [Run workflow](#run-workflow)
- [Supported tasks](#supported-tasks)

## Concepts

### Task

Task is list of action (recipe) that needs to be executed.

Example tasks:
- create git repository
- create build plan
- create deployment plan
- create Docker registry

### Step

Step is parameterized task with assigned name.

### Workflow configuration

Workflow configuration it is list of steps to be executed to initialize new service.
Each step has name and is related to executing specific task.

Workflow configuration is provided in YAML format.

#### Example

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

#### Example file

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

Command to run workflow.

    python initialize_service.py --configuration PATH_TO_WORKFLOW_CONFIGURATION.yaml --parameters PATH_TO_SERVICE_METADATA.yaml

Example usage:

    python initialize_service.py --configuration workflow_simple.yaml --parameters service_metadata.yaml

## Supported tasks

TODO
