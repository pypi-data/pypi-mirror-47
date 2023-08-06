# Contractual
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![pipeline status](https://gitlab.com/pjbecotte/contractual/badges/master/pipeline.svg)](https://gitlab.com/pjbecotte/contractual/commits/master)
[![coverage report](https://gitlab.com/pjbecotte/contractual/badges/master/coverage.svg)](https://gitlab.com/pjbecotte/contractual/commits/master)

## Installation

`pip install contractual`


## Use

how to use-

## Contract Files

Contract files comply with the Pact file format seen at
https://github.com/pact-foundation/pact-specification/tree/version-2
There is a key difference though-

Contractual supports mocking out arbitrary interfaces, while Pact limits itself
to http requests. As such, a Contractual file can only be used with a Pact verifier
if you limit the unchecked mocks to `HttpContractMock`. In the files themselves,
you will see a list of interactions having the form


```json
{
    "description": "get all users for max",
    "request": {},
    "response": {},
    "providerState": "a user with an id named 'u:ser' exists"
}
```

        

That is a valid HTTP contract. A more general `ContractMock` contract would have the
form


```json
{
    "description": "get all users for max",
    "contractMock": {
        "contractName": "Name",
        "args": []
    },
    "response": {},
    "providerState": "a user with an id named 'user' exists"
}
```

## Development

### Development Environment

Poetry is used to manage the project and dependencies. Once you have poetry installed 
`pip install --user poetry`, you can run `poetry install` to setup a virtaulenv for
your project. Dependencies can be updated using `poetry add` or `poetry remove` and
committing the updated pyproject.toml and poetry.lock files.

### Release

CI is handled on Gitlab at https://gitlab.com/pjbecotte/contractual. There is a make
target to create a new release by tagging a new version and then incrementing to the
next beta version. (This requires permissions to push to master)
