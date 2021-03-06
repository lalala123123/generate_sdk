# generate_sdk
The pypi package is generated by `dsl.generate_packge`. You could execute `generate_package.py` to regenerate package.
```
from azure.ml.component import dsl

assets = {
    'components': [
        'file:./local_components/mpi/component.yaml',
        'file:./local_components/copy_files/component.yaml',
        'file:./local_components/hdi-component/component_spec.yaml',
        'file:./local_components/scope_component/toss/component_spec.yaml',
        'file:./local_components/sweep_component/sweep.spec.yaml',
        'azureml://feeds/azureml',
        'azureml://feeds/huggingface',
    ],
}
source_dir = './generated_package'
dsl.generate_package(force_regenerate=True, assets=assets, package_name='generate_sdk', source_directory=source_dir, mode='snapshot')
```

You could follow these [steps](https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project) to package and upload your project to pypi.

This is an example of [pypi package](https://pypi.org/project/generate-sdk/) generated by `dsl.generate_package`.


You could follow these [steps](https://docs.readthedocs.io/en/stable/tutorial/#first-steps) to upload your package reference doc to [readthedocs](https://readthedocs.org/).

This is the [reference doc link](https://generate-sdk.readthedocs.io/en/workspace_dependent/index.html#) generated by this pypi package.
