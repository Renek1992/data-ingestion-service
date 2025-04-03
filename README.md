<img src="docs/images/ts_logo.png" alt="Diagram 1" width="80">


# data-dw-ingestions
Repo for an application responsible in ingesting data into the Data Warehouse Snowflake. External data sources are being tapped into utilising available REST APIs to either extract data objects or reports. <br> 
These API calls are being computed through a AWS Lambda setup and stored in AWS S3 as relevant format such as .csv or .json. The S3 location serves as 



## Architecture
This project contains resources and components to build additional Lambda applications. Components are stored within lambda layers and can be attached to the Lambda function itself through the application cloudformation templates. 

Generally components can be categorised in utilities and and helpers. Utilities in this project are:

- Cloudwatch Logs (logging application activities)
- Secretsmanager (storing confidential information)
- Slack Alerts (sending alerts to a Slack Channel)
<br>

Helpers represent pyhton classes that allow the easier orechstration and utilize dependecy, config and api interaction:

- Configuration (Allows the easy handling of environments)
- Dependecies (Installation of required libraries)
- Shared Modules (Code for interacting with AWS + telemetry)
<br>

The following diagram shows the end-to-end application structure from external data sources to the storage component through AWS S3. 
<img src="docs/images/data-ingest.svg">

### Environments
The data ingestion project is currently split into distinct environments. These environments are being used are used to separate different stages of the software development lifecycle and to ensure that code changes are thoroughly tested before being deployed to production. 
Currently this repo is built with the methodology of three repos:

<b>Local:</b><br>
This is where developers write, test, and debug code locally on their machines. 

<b>Development:</b><br>
This is where software changes are tested rigorously before being released to production.

<b>Production:</b><br>
This is the live environment where the software application is accessed and used by end-users.

<img src="docs/images/environments.svg">

### Project Structure
The porject follows a conventional directory and folder structure with commonly found naming conventions such as src, shared and deploy for categoization of code in respect to their purpose.

```bash
./root
    |-- deploy                      Folder for deployment files.
        |-- cicd                    CI-CD pipeline.
        |-- infra                   Application infrastructure.
    |-- docs                        Documentation.
    |-- events                      Local dev events for Lambda.
    |-- shared                      Shared Modules.
        |-- aws                     AWS Clients.
        |-- common                  Types.
        |-- recurly                 Recurly API wrapper.
        |-- telemetry               Logging and alerting.
    |-- src                         Source folder for apps.
        |-- {__apps__}              Apps folder.
        |-- config.py               Config orchestrator.
    |-- tests                       Tests folder for unit tests.
    |-- env.example                 Local env file.
    |-- Pipfile                     Dependency management.
```

## Contribution
This repo is activly developed on, meaning It is subject to constant exapnsion and change of current code to fulfill business needs. The following sections describe the setup of a development environment to activly develop lambda applications in python.


### Local Env Setup
Currently the project is orchestrated soley through python's Pipenv. To activate the environment and install dependencies execute the following:
```bash
pipenv install 
pipenv install -d 

pipenv shell
```

If necessary, the pythonpath can be set through the following commpand (Ensure you are in the project's root directory before executing):

```bash
export PYTHONPATH=$(pwd)
```

### Code Linting & Formatting
Code linting and code testing are part of the core essentials to safeguard the code integrity of this repo. The implemented tests are here to ensure the code quality doesn't deminish and bugs are caught early on before appearing in a production environment.

#### Code Linting
In this repo, the python llibrary [Ruff](https://docs.astral.sh/ruff/) is being utilized for code linting and formatting. Ruff is a python library written in Rust allowing linting and formatting in unmached speed compared to others. 

Within this project Ruff is installed as part of the developer dependecies (`ruff = "*"`) and is executable within the pipenv shell.

For code linting run: 
```bash
ruff check          # Lint all files in the current directory.
ruff check --fix    # Lint all files in the current directory, and fix any fixable errors.
```

#### Code Formatting
Ruff also containes a built in python code formatter that allows easy acode formatting on the go. The Ruff formatter is available as of Ruff v0.1.2.

For code formatting run:
```bash
ruff format         # Format all files in the current directory.
```

### Code Testing
This repostory relies on the implementation of python unit tests. Herefore the standard library is [Pytest](https://docs.pytest.org/en/8.0.x/). Pytest is a widely-used testing framework for Python that makes writing simple unit tests and complex functional tests easier. It offers a simple syntax, robust fixtures, and extensive plugin support, making it highly customizable and adaptable to various testing needs.

To execute pytests, run the following within the pipenv shell:
```bash
pytest tests/
```

A coverage report can be created through the following command utilizing `pytest-coverage` (ensure you are in the project root directory):
```bash
pytest --cov=./ tests/
```


### Docs
More documentation on contribution guidelines can be found in the following markdown file: <br>
Path: `./docs.COMMIT_GUIDELINES.md`


## Deployment
Code deployment is the process of releasing software updates from development to production. It involves preparing the code, testing it thoroughly, deploying it to production, monitoring its performance, and potentially rolling back changes if issues arise. Effective deployment relies on planning, collaboration, and the use of tools to ensure a smooth and reliable release process.

### GitHub Branches
This project utilizes a thre branch repo strategy. Herefore there is a `feature` branch, `dev` branch and `main` branch:

- feature branch: serves for local development
- dev branch: serves as source for deployment into dev AWS account
- prod branch: serves as source for deployment into prod AWS account


### Deployment Files
This project follows the Infrastructure-as-Code principle. Infrastructure-as-Code (IaC) is a concept in software engineering that involves managing and provisioning computing infrastructure through machine-readable definition files, rather than physical hardware configuration or interactive configuration tools.

The following folder structure shows relevant files needed for the deployment: 

```bash
./deploy
    |-- cicd
        |-- buildspec.yml       > specs for codebuild build project
        |-- pipeline.yml        > cicd template
        |-- testspec.yml        > specs for codebuild test project
    |-- infra
        |-- template.yml        > app template

```


### CI-CD Pipeline
A CI/CD pipeline automates the process of building, testing, and deploying software changes. Developers regularly integrate code changes into a shared repository:
- (`Continuous Integration`) where automated tests ensure code quality. After passing tests, changes are automatically deployed to staging 
- (`Continuous Delivery`), and optionally to production 
- (`Continuous Deployment`), streamlining the release process. This automation saves time, reduces errors, and enables faster delivery of software updates.

For this project AWS Codepipeline is polling from a respective GitHub repo and creates a soure artifact. Following this, AWS Codebuild is being utilized to build and test the source code. 

The last step is the deployment through AWS Codedeploy sending the prepared template to cloudformation in order to build the infrastructure.

<img src="docs/images/deployment_workflow.svg">

## Issues and Feedback
If you encounter any issues or have feedback, please open an issue. We welcome contributions and suggestions to improve this python project.
