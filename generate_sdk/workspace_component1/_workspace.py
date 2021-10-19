# THIS IS AN AUTO GENERATED FILE.
# PLEASE DO NOT MODIFY MANUALLY.
from azureml.core import Workspace


_lisal_amlservice_workspace = None


def lisal_amlservice():
    global _lisal_amlservice_workspace
    if _lisal_amlservice_workspace is None:
        _lisal_amlservice_workspace = Workspace.get(
            subscription_id='74eccef0-4b8d-4f83-b5f9-fa100d155b22',
            resource_group='lisal-dev',
            name='lisal-amlservice')
    return _lisal_amlservice_workspace
