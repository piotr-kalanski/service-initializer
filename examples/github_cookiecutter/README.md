# GitHub and Cookiecutter example

Basic worfklow example creating below resources:
- GitHub repository
- Generating directory structure using cookiecutter project template

## Run

### Set environment variable with GitHub auth token

#### Linux

    export GITHUB_AUTH_TOKEN = 'PASTE HERE YOUR GITHUB AUTH TOKEN'

#### Powershell

    $env:GITHUB_AUTH_TOKEN = 'PASTE HERE YOUR GITHUB AUTH TOKEN'

### Run initialize service command

    python initialize_service.py --configuration examples/github_cookiecutter/workflow.yaml --parameters examples/github_cookiecutter/service_metadata.yaml
