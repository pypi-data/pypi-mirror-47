# Python juliohmtools

A collection of Python libraries. Releases are uploaded to <https://pypi.org/project/juliohmtools/>, so you can easily use Pip to install the library.

## Installation

Preferably, install the library to your user only, or to a Python Environment using `pipenv`.

```bash
pip install -U juliohmtools
```

## Libraries included

* [k8scontroller - Kubernetes Controller Wrapper](docs/k8scontroller/README.md)

## Local Testing

To create an environment for testing and development, use `pipenv`. In the root directory:

```bash
# if you still don't have pipenv
pip install -U --upgrade pipenv

# install all dependencies into a dedicated python environment
pipenv install

# open a shell to that environment
pipenv shell
```

From inside the pipenv shell, add this module as local symlink installation.

```bash
pip install -e .
```

To remove the symlink from the environment:

```bash
pip uninstall juliohmtools
```
