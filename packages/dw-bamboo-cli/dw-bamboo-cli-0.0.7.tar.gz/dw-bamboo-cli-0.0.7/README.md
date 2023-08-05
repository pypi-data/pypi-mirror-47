# Bamboo Command Line Interface (CLI)

The Bamboo CLI allows users to modify pipeline parameters without the need to change any code or configuration files.

## Installation
`pip install dw-bamboo-cli`

## Example Usage
```
bamboo-cli --folder /my/bamboo/pipeline/folder --entry health_runner.run_health --param1=value1 --param2=value2
```

Note that the entry function should be supplied as `module_name`.`function_name`. And the function should follow the form of:

```python
def entry_func(params, **kwargs):
  # where params is a dictionary of key/values for the pipeline and MyPipeline is your customized
  # subclass of BasePipeline
  pipeline = MyPipeline()
  pipeline.run(params)
```
