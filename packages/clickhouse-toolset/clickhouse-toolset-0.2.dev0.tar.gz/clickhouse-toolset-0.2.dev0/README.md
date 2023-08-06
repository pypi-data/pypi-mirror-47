# ClickHouse query tools
Exposes ClickHouse internals to parse and manipulate ClickHouse queries.

## Install pre-built packages
You can install a pre-compiled package for your platform, e.g.:
```
pip install dist/clickhouse_toolset-0.2dev-cp37-cp37m-linux_x86_64.whl
```

## Development

First, you need to clone the repo and its submodules.

```
git clone --recursive git@gitlab.com:tinybird/clickhouse-toolset.git
```

Then, you will compile the dependencies and the module itself. For this task you need to have gcc/g++ 8.

```
pip install --editable .
```

### Generate pre-built packages

You can generate pre-compiled binaries for your platform using:
```
python setup.py sdist bdist_wheel
python setup.py sdist
twine upload --repository-url https://test.pypi.org/legacy/ dist/clickhouse-toolset-0.2dev0.tar.gz
```

### Development

```
pip install --editable .
```

## Examples

Check tests directory.
