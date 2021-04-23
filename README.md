# Study Project for system architecture 
#### Service responsible for uploading and downloading data.
![Build Status](https://img.shields.io/github/workflow/status/unbrokenguy/sys-arch-client/lint?label=linters)
* [Installation](#installation)
* [Setup](#setup)
* [Usage](#usage)
* [Related repositories](#related-repositories)
## Installation

#### Install poetry
```shell
pip install poetry
```

#### Install the project dependencies
```shell
poetry install 
```

## Setup

#### Make sure you have installed and started these servers in this order 
1. [Configuration Server](https://github.com/unbrokenguy/sys-arch-conf-app)
2. [Authorization Server](https://github.com/unbrokenguy/sys-arch-auth-app)
3. [Data Server](https://github.com/unbrokenguy/sys-arch-server)
#### Add environments
* SERVER_URL: [Data Server](https://github.com/unbrokenguy/sys-arch-server) url.
## Usage
####  Spawn a shell within the virtual environment
```shell
poetry shell 
```
#### Start cli application
```
cd src && python main.py
```
## Related repositories
1. [Configuration Server](https://github.com/unbrokenguy/sys-arch-conf-app)
2. [Authorization Server](https://github.com/unbrokenguy/sys-arch-auth-app)
3. [Data Server](https://github.com/unbrokenguy/sys-arch-server)  
4. [Front end](https://github.com/niyazm524/arch_client_web)