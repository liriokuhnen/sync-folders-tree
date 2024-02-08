Sync Folders Tree
=================

Service to synchronize two folders source and destination in order to keep an identical copy in destination

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

# Run with CLI

use CLI commands to execute a sync loop with the configuration

```
python src/run_sync.py {source_path} {destination_path} {interval_loop} {file_log_path}
```

**Optional sha245**

The strategy to confirm if file is different or not by default will be file size + last modified date, avoiding the need of open both files and read them line by line which means spend less power computer resources, but it also means this check could not be 100% precise once it will depend the OS date updating.

An optional sha256 flag can be used in order to change the diff strategy, sha256 will read both files content by chunks and will create a hash to be able to identify if a file is different, in this case the diff will be 100% precise but it will spend more power computer resources.

to use hash strategy use the flag `--sha256` or `-s`

```
python src/run_sync.py {source_path} {destination_path} {interval_loop} {file_log_path} --sha256
```

**Optional symlink**

flag `--symlink` or `l` will follow symlink in the synchronization process although be aware it can lead to infinite recursion problem if a link points to a parent directory inside a sync folder.

the symlink will be created on destination as a new folder.

```
python src/run_sync.py {source_path} {destination_path} {interval_loop} {file_log_path} --symlink
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