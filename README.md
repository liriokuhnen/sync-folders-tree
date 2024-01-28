Sync Folders Tree
=================

Service to synchronize two folders source and destination in order to keep a identical copy in destination

# Virtual env

Create virtual environment

```
python3.11 -m venv .env
```

Activate virtual environment

```
source .env/bin/activate
```

# Install packages

Install packages requirements

```
pip install -r requirements.txt
```

# Tests

Run tests

```
pytest
```

# Code Lint

```
pylint src
```

# Coverage

Run coverage with pytest

```
coverage run -m pytest
```

report with lines not covered

```
coverage report -m
```

detailed report with html content

```
coverage html
```