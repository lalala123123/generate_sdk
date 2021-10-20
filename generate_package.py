from azure.ml.component import dsl

assets = {
    'workspace_dependent_component':
        "azureml://subscriptions/74eccef0-4b8d-4f83-b5f9-fa100d155b22/resourcegroups/lisal-dev/workspaces/lisal-amlservice/",
    'local_component': [
        'file:./local_components/mpi/component.yaml',
        'file:./local_components/copy_files/component.yaml',
        'file:./local_components/hdi-component/component_spec.yaml',
        'file:./local_components/scope_component/toss/component_spec.yaml',
        'file:./local_components/sweep_component/sweep.spec.yaml',
    ],
    'feed': ["azureml://feeds/azureml", "azureml://feeds/huggingface",]
}

source_dir = './generated_package'
dsl.generate_package(force_regenerate=True, assets=assets, package_name='generate_sdk', source_directory=source_dir, mode='snapshot')