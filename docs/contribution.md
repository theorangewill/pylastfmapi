# How to contribute

If you want to contribute to the project, you will need to understand the project structure and how to setup the development environment.

## Project structure


```mermaid
flowchart
	. --> docs
	. --> pylastfm
	. --> tests
    . --> mkdocs.yml
    . --> pyproject.toml
    . --> README.md
```

The project has three directories: `docs`, `pylastfm`, and `tests`.
It also has the `pyproject.toml` defining the whole project environment, `mkdocs.yml` with documentation settings, and the `README.md`.

### pylastfm

```mermaid
flowchart
	. --> pylastfm
    pylastfm --> client.py
    pylastfm --> constants.py
    pylastfm --> exceptions.py
    pylastfm --> requests.py
    pylastfm --> settings.py
    pylastfm --> typehints.py
    pylastfm --> utils.py
```

The `pylastfm` directory has all the source code of the package.

- **[`client.py`](api/client.md)**: the LastFM API class with all methods implemented.
- **[`constants.py`](api/constants.md)**: all constants used in the project to interact with the LastFM API, like backend methods names, and pre-defined values for some operations.
- **[`exceptions.py`](api/exceptions.md)**: just specific exceptions
- **[`requests.py`](api/requests.md)**: defines a `RequestController` class for managing API requests and handling cached responses for the LastFM API. It includes methods for making requests, handling pagination, and managing cached responses.
- **[`settings.py`](api/settings.md)**: a Settings class using Pydantic's `BaseSettings` for configuration management, particularly for environment variables.
- **[`typehints.py`](api/typehints.md)**: type aliases for various fixed sets of string values using Python's Literal from the typing module. These are used to ensure that variables or parameters adhere to a specific set of valid values.
- **[`utils.py`](api/utils.md)**: contains utility functions shared between LastFM class methods.


### tests

```mermaid
flowchart
	. --> tests
    tests --> conftest.py
    tests --> integration
    integration --> test_integration_client.py
    tests --> unit
    unit --> test_request.py
    unit --> test_utils.py
    unit --> client
    client --> ...
```

The `test` directory has all the tests of the package.

- **`conftest.py`**: fixture for the tests
- **`integration/test_integration_client.py`**: integration tests for the package
- **`unit/test_request.py`**: unit tests for [`requests.py`](api/requests.md)
- **`unit/test_utils.py`**: unit tests for [`utils.py`](api/utils.md)
- **`unit/client/...`**: unit tests for [`client.py`](api/client.md) separated in multiple scripts depending on the scope of the method (album, artist, chart, country, tag, track, and user)


### docs

```mermaid
flowchart
	. --> docs
    docs --> api
    api --> ...
    docs --> contribution.md
    docs --> index.md
    docs --> methods.md
```

The `docs` directory has all the documentation of the package.

- **`index.md`**: main page
- **`methods.md`**: all methods implemented
- **`contribution.md`**: guidelines to contributing
- **`api/`**: all the pages with the tech doc for each one of the scripts in package (client, constants, exceptions...)

***


## Environment & Tools

### Creating environment 

All the requirements are explicitly described in `pyproject.toml` file, with their respective versions.

Following the steps you will be able to build the environment with Poetry:

```bash
git clone https://github.com/theorangewill/pylastfm.git
poetry install
poetry shell
```
### Setting credentials

Before executing any test, it is necessary to create `.env` file with the `USER_AGENT` and `API_KEY` to connect with LastFM API.

```txt
API_KEY="api-key"
USER_AGENT="user-agent"
```

### Running tests

To execute the tests, it will check the code with Ruff and Black, test with Pytest and, then, check the coverage:

```bash
task test
```

### Starting doc server

To start the doc server, simply:
```{.sh}
task docs
```

### List of main technologies used

For production environment:

- `request` to handle with HTTPs requests

For development environment

- Pytest for tests
- Ruff, Black and Mypy
- Taskipy to create commands aliases
- Pydantic to set the credentials in `.env`

For documentation environment

- MkDocs

### Useful alias

With Taskipy, you can easily execute some commands:

- `task format`: to execute Ruff and Black
- `task mypy`: to execute Mypy
- `task test`: to execute Pytest
- `task docs`: to start MkDocs server

## What could I do

- Improve anything you think that can be improved
- Implement POST methods that require user authentication
- Fix any bug that you found