Varsnap Python
==============

[![Codeship Status for albertyw/varsnap-python](https://app.codeship.com/projects/ec0db4a0-6736-0137-f93c-2a3aec68720b/status?branch=master)](https://app.codeship.com/projects/345464)

http://varsnap.com

Python VarSnap client

Usage
-----

Add the varsnap decorator in front of any function you'd like to make better:

```python
from varsnap import varsnap


@varsnap
def example(args, **kwargs):
    return 'output'
```

Requirements
------------

The varsnap client currently requires python 3.7.

The client depends on three environment variables to be set:

 - `VARSNAP` - Should be either `true` or `false`.  Varsnap will be disabled if the variable is anything other than `true`.
 - `ENV` - If set to `development`, the client will receive events from production.  If set to `production`, the client will emit events.
 - `VARSNAP_TOKEN` - Copied from https://www.varsnap.com/user/

Publishing
----------

```bash
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
