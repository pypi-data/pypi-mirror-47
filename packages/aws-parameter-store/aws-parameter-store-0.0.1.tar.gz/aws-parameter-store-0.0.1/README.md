# aws-parameter-store

AWS SSM parameter store client that constructs nested dictionary out of hierarchical path

## Features
- Gets parameters by path
- Collects all paged results automatically
- Lightweight

## Installation
Install with `pip`:

>  `pip install aws-parameter-store  `

## Getting started

Import the module and create a new instance of `AwsParameterStore`.

```python
from aws_parameter_store import AwsParameterStore

store = AwsParameterStore('us-east-1')
```
## API
### overview

By default
* JSON parameters are being evaluated
* Parameters are decrypted

### Examples


Given the parameters:

| Name  | Value |
| ------------- | ------------- |
| key-a | wrong |
| example/key-b | flat |
| example/key-c | secret |
| example/path1/path2/key-d | deep |
```py
ret = param_store.get_parameters_dict('/example/')
assert ret ==  {
    'key-b': 'flat',
    'key-c': 'secret',
    'path1': { 'path2': { 'key-d': 'deep' } }
}
```

## Requirements
* Python3.6+

## Contributing
You are welcome to contribute and join our family =)

# License



See the [LICENSE](https://github.com/Vonage/aws-parameter-store-py/blob/master/LICENSE.txt) file for license rights and limitations (Apache License, Version 2.0)