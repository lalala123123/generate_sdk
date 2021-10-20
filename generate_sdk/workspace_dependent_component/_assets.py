# THIS IS AN AUTO GENERATED FILE.
# PLEASE DO NOT MODIFY MANUALLY.
# Components included in this generated file:
#  - CompareModule::0.1.1
#  - Sample Module::0.1.0
#  - convert2ss::0.0.1
#  - eselect::0.0.1
#  - lisal-amlservice://Compare::0.0.1
#  - lisal-amlservice://par15::0.0.2
#  - microsoft.com.azureml.samples.XGBRegressorTraining::0.0.2
#  - microsoft.com.azureml.samples.compare_2_models::0.1.0
#  - microsoft.com.azureml.samples.evaluate::0.0.5
#  - microsoft.com.azureml.samples.score::0.0.4
#  - microsoft.com.azureml.samples.train::0.0.4
#  - microsoft.com.azureml.samples.train.test::0.0.5
#  - microsoft.com/aml/samples://Compare::0.0.1
#  - microsoft.com/aml/samples://Compare 2 Models::0.0.10
#  - microsoft.com/aml/samples://Evaluate::0.0.8
#  - microsoft.com/aml/samples://MPI Train::0.0.10
#  - microsoft.com/aml/samples://Score::0.0.6
#  - microsoft.com/aml/samples://Train::0.0.5
#  - microsoft.com/aml/samples://to_dfd::0.0.1
#  - microsoft.com/aml/sc://Tokenizer::0.0.10
#  - microsoft.com/azureml/samples1-o://Hello World Output 10::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 11::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 12::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 2::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 3::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 4::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 5::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 6::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 7::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 8::0.0.0
#  - microsoft.com/azureml/samples1-o://Hello World Output 9::0.0.0
#  - microsoft.com/azureml/samples1://Hello World::0.0.2
#  - microsoft.com/azureml/samples1://Hello World Input - 0::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 10::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 11::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 12::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 13::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 2::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 3::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 4::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 5::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 6::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 7::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 8::0.0.0
#  - microsoft.com/azureml/samples1://Hello World Input 9::0.0.0
#  - microsoft.com/azureml/samples://Convert Multi Parquet Files to DataFrameDirectory::0.0.1
#  - microsoft.com/azureml/samples://First Module::0.0.1
#  - microsoft.com/azureml/samples://Hello World::0.0.1
#  - microsoft.com/azureml/samples://Hello World MPI Job::0.0.1
#  - microsoft.com/azureml/samples://MPI Train::0.0.1
#  - microsoft.com/azureml/samples://MPI Train Wide and Deep Recommender::0.0.1
#  - microsoft.com/azureml/samples://MetricDummyModuleCLI::0.4
#  - microsoft.com/azureml/samples://Parallel Score Wide and Deep Recommender::0.0.1
#  - microsoft.com/bing://ejoin::0.0.5
#  - microsoft.com/bing://eselect2::0.0.2
#  - microsoft.com/cat://MAP::1.1.1
#  - microsoft.com/cat://Precision at K::1.1.1
#  - microsoft.com/cat://Recall at K::1.1.1
#  - microsoft.com/cat://SAR Scoring::1.1.1
#  - microsoft.com/cat://SAR Training::1.1.1
#  - microsoft.com/cat://Stratified Splitter::1.1.1
#  - microsoft.com/cat://nDCG::1.1.1
#  - microsoft.com/office://Mpi Module::0.0.1
#  - microsoft.com/office://Sample Module::0.1.0
#  - scopemultijoin::0.0.2
#  - train::0.1.0
#  - xslapper::0.0.1
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Union

from azure.ml.component import Component
from azure.ml.component.component import Input, Output
from azureml.core import Dataset

from . import _workspace


SOURCE_DIRECTORY = Path(__file__).parent / ".."


class _CommandComponentRunsettingDockerConfiguration:
    """Docker configuration section specify the docker runtime properties for the Run.."""
    arguments: Union[str, list]
    """Extra arguments to the Docker run command. The extra docker container options like --cpus=2, --memory=1024"""
    shared_volumes: bool
    """Indicates whether to use shared volumes. Set to False if necessary to work around shared volume bugs on Windows. The default is True."""
    shm_size: str
    """The size of the Docker container's shared memory block. If not set, the default 2g is used."""
    use_docker: bool
    """Specifies whether the environment to run the experiment should be Docker-based. Amlcompute linux clusters require that jobs running inside Docker containers. The backend will override the value to be true for Amlcompute linux clusters."""


class _CommandComponentRunsettingEnvironment:
    """Environment section set runtime environment."""
    conda: str
    """Defines conda dependencies"""
    docker: str
    """Defines settings to customize the Docker image built to the environment's specifications."""
    os: str
    """Defines the operating system the component running on. Could be Windows or Linux. Defaults to Linux if not specified. (enum: ['Windows', 'Linux'])"""


class _CommandComponentRunsettingResourceLayout:
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    instance_count: int
    """Number of instances in the compute target used for training. (min: 1)"""
    instance_type: str
    """Instance type used for training."""
    node_count: int
    """Number of nodes in the compute target used for training. (min: 1)"""


class _CommandComponentRunsettingTargetSelector:
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""
    allow_spot_vm: bool
    """Flag to enable target selector service to send job to low priority VM. Currently it only works for AmlK8s."""
    cluster_block_list: Union[str, list]
    """User specified block list of Cluster."""
    compute_type: str
    """Compute type that target selector could route job to. (enum: ['AmlCompute', 'AmlK8s'])"""
    instance_types: Union[str, list]
    """List of instance_type that job could use. If no instance_type specified, all sizes are allowed."""
    my_resource_only: bool
    """Flag to control whether the job should be sent to the cluster owned by user. If False, target selector may send the job to shared cluster. Currently it only works for AmlK8s."""
    regions: Union[str, list]
    """List of region that would like to submit job to. If no region specified, all regions are allowed."""
    vc_block_list: Union[str, list]
    """User specified block list of VC."""


class _CommandComponentRunsetting:
    """Run setting configuration for CommandComponent"""
    environment_variables: Union[str, dict]
    """Environment variables can be used to specify environment variables to be passed. It is a dictionary of environment name to environment value mapping. User can use this to adjust some component runtime behavior which is not exposed as component parameter, e.g. enable some debug switch."""
    priority: int
    """The priority of a job which is a integer. For AmlK8s Compute, User can set it to 100~200. Any value larger than 200 or less than 100 will be treated as 200. For Aml Compute, User can set it to 1~1000. Any value larger than 1000 or less than 1 will be treated as 1000."""
    target: str
    """The compute target to use"""
    docker_configuration: _CommandComponentRunsettingDockerConfiguration
    """Docker configuration section specify the docker runtime properties for the Run.."""
    environment: _CommandComponentRunsettingEnvironment
    """Environment section set runtime environment."""
    resource_layout: _CommandComponentRunsettingResourceLayout
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    target_selector: _CommandComponentRunsettingTargetSelector
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""


class _ScopeComponentRunsettingScope:
    """This section contains specific settings for scope component."""
    adla_account_name: str
    """The name of the Cosmos-migrated Azure Data Lake Analytics account to submit scope job."""
    custom_job_name_suffix: str
    """Optional parameter defining custom string to append to job name."""
    scope_param: str
    """Parameters to pass to scope e.g. Nebula parameters, VC allocation parameters etc."""


class _ScopeComponentRunsetting:
    """Run setting configuration for ScopeComponent"""
    scope: _ScopeComponentRunsettingScope
    """This section contains specific settings for scope component."""


class _ParallelComponentRunsettingDockerConfiguration:
    """Docker configuration section specify the docker runtime properties for the Run.."""
    arguments: Union[str, list]
    """Extra arguments to the Docker run command. The extra docker container options like --cpus=2, --memory=1024"""
    shared_volumes: bool
    """Indicates whether to use shared volumes. Set to False if necessary to work around shared volume bugs on Windows. The default is True."""
    shm_size: str
    """The size of the Docker container's shared memory block. If not set, the default 2g is used."""
    use_docker: bool
    """Specifies whether the environment to run the experiment should be Docker-based. Amlcompute linux clusters require that jobs running inside Docker containers. The backend will override the value to be true for Amlcompute linux clusters."""


class _ParallelComponentRunsettingEnvironment:
    """Environment section set runtime environment."""
    conda: str
    """Defines conda dependencies"""
    docker: str
    """Defines settings to customize the Docker image built to the environment's specifications."""
    os: str
    """Defines the operating system the component running on. Could be Windows or Linux. Defaults to Linux if not specified. (enum: ['Windows', 'Linux'])"""


class _ParallelComponentRunsettingParallel:
    """This section contains specific settings for parallel component."""
    error_threshold: int
    """The number of record failures for TabularDataset and file failures for FileDataset that should be ignored during processing. If the error count goes above this value, then the job will be aborted. Error threshold is for the entire input and not for individual mini-batches sent to run() method. The range is [-1, int.max]. -1 indicates ignore all failures during processing. (min: -1, max: 2147483647)"""
    logging_level: str
    """A string of the logging level name, which is defined in 'logging'. Possible values are 'WARNING', 'INFO', and 'DEBUG'."""
    max_node_count: int
    """The maximum node count that the Parallel job can scale out to."""
    mini_batch_size: str
    """For FileDataset input, this field is the number of files user script can process in one run() call. For TabularDataset input, this field is the approximate size of data the user script can process in one run() call. Example values are 1024, 1024KB, 10MB, and 1GB."""
    node_count: int
    """Number of nodes in the compute target used for running the Parallel Run."""
    process_count_per_node: int
    """Number of processes executed on each node. Optional, default value is number of cores on node."""
    run_invocation_timeout: int
    """Timeout in seconds for each invocation of the run() method."""
    run_max_try: int
    """The number of maximum tries for a failed or timeout mini batch. A mini batch with dequeue count greater than this won't be processed again and will be deleted directly. (min: 1)"""
    version: str
    """The version of back-end to serve the module. Please set as \"preview\" only if you are using preview feature and instructed to do so. Otherwise use the default value."""


class _ParallelComponentRunsettingResourceLayout:
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    instance_count: int
    """Number of instances in the compute target used for training. (min: 1)"""
    instance_type: str
    """Instance type used for training."""


class _ParallelComponentRunsettingTargetSelector:
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""
    allow_spot_vm: bool
    """Flag to enable target selector service to send job to low priority VM. Currently it only works for AmlK8s."""
    cluster_block_list: Union[str, list]
    """User specified block list of Cluster."""
    compute_type: str
    """Compute type that target selector could route job to. (enum: ['AmlCompute', 'AmlK8s'])"""
    instance_types: Union[str, list]
    """List of instance_type that job could use. If no instance_type specified, all sizes are allowed."""
    my_resource_only: bool
    """Flag to control whether the job should be sent to the cluster owned by user. If False, target selector may send the job to shared cluster. Currently it only works for AmlK8s."""
    regions: Union[str, list]
    """List of region that would like to submit job to. If no region specified, all regions are allowed."""
    vc_block_list: Union[str, list]
    """User specified block list of VC."""


class _ParallelComponentRunsetting:
    """Run setting configuration for ParallelComponent"""
    environment_variables: Union[str, dict]
    """Environment variables can be used to specify environment variables to be passed. It is a dictionary of environment name to environment value mapping. User can use this to adjust some component runtime behavior which is not exposed as component parameter, e.g. enable some debug switch."""
    priority: int
    """The priority of a job which is a integer. For AmlK8s Compute, User can set it to 100~200. Any value larger than 200 or less than 100 will be treated as 200. For Aml Compute, User can set it to 1~1000. Any value larger than 1000 or less than 1 will be treated as 1000."""
    target: str
    """The compute target to use"""
    docker_configuration: _ParallelComponentRunsettingDockerConfiguration
    """Docker configuration section specify the docker runtime properties for the Run.."""
    environment: _ParallelComponentRunsettingEnvironment
    """Environment section set runtime environment."""
    parallel: _ParallelComponentRunsettingParallel
    """This section contains specific settings for parallel component."""
    resource_layout: _ParallelComponentRunsettingResourceLayout
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    target_selector: _ParallelComponentRunsettingTargetSelector
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""


class _DistributedComponentRunsettingDockerConfiguration:
    """Docker configuration section specify the docker runtime properties for the Run.."""
    arguments: Union[str, list]
    """Extra arguments to the Docker run command. The extra docker container options like --cpus=2, --memory=1024"""
    shared_volumes: bool
    """Indicates whether to use shared volumes. Set to False if necessary to work around shared volume bugs on Windows. The default is True."""
    shm_size: str
    """The size of the Docker container's shared memory block. If not set, the default 2g is used."""
    use_docker: bool
    """Specifies whether the environment to run the experiment should be Docker-based. Amlcompute linux clusters require that jobs running inside Docker containers. The backend will override the value to be true for Amlcompute linux clusters."""


class _DistributedComponentRunsettingEnvironment:
    """Environment section set runtime environment."""
    conda: str
    """Defines conda dependencies"""
    docker: str
    """Defines settings to customize the Docker image built to the environment's specifications."""
    os: str
    """Defines the operating system the component running on. Could be Windows or Linux. Defaults to Linux if not specified. (enum: ['Windows', 'Linux'])"""


class _DistributedComponentRunsettingResourceLayout:
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    instance_count: int
    """Number of instances in the compute target used for training. (min: 1)"""
    instance_type: str
    """Instance type used for training."""
    node_count: int
    """Number of nodes in the compute target used for training. (min: 1)"""
    process_count_per_instance: int
    """Number of processes per instance. If greater than 1, mpi distributed job will be run. Only AmlCompute compute target is supported for distributed jobs. (min: 1, max: 8)"""


class _DistributedComponentRunsettingTargetSelector:
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""
    allow_spot_vm: bool
    """Flag to enable target selector service to send job to low priority VM. Currently it only works for AmlK8s."""
    cluster_block_list: Union[str, list]
    """User specified block list of Cluster."""
    compute_type: str
    """Compute type that target selector could route job to. (enum: ['AmlCompute', 'AmlK8s'])"""
    instance_types: Union[str, list]
    """List of instance_type that job could use. If no instance_type specified, all sizes are allowed."""
    my_resource_only: bool
    """Flag to control whether the job should be sent to the cluster owned by user. If False, target selector may send the job to shared cluster. Currently it only works for AmlK8s."""
    regions: Union[str, list]
    """List of region that would like to submit job to. If no region specified, all regions are allowed."""
    vc_block_list: Union[str, list]
    """User specified block list of VC."""


class _DistributedComponentRunsetting:
    """Run setting configuration for DistributedComponent"""
    environment_variables: Union[str, dict]
    """Environment variables can be used to specify environment variables to be passed. It is a dictionary of environment name to environment value mapping. User can use this to adjust some component runtime behavior which is not exposed as component parameter, e.g. enable some debug switch."""
    priority: int
    """The priority of a job which is a integer. For AmlK8s Compute, User can set it to 100~200. Any value larger than 200 or less than 100 will be treated as 200. For Aml Compute, User can set it to 1~1000. Any value larger than 1000 or less than 1 will be treated as 1000."""
    target: str
    """The compute target to use"""
    docker_configuration: _DistributedComponentRunsettingDockerConfiguration
    """Docker configuration section specify the docker runtime properties for the Run.."""
    environment: _DistributedComponentRunsettingEnvironment
    """Environment section set runtime environment."""
    resource_layout: _DistributedComponentRunsettingResourceLayout
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    target_selector: _DistributedComponentRunsettingTargetSelector
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""


class _ComparemoduleInput:
    data1: Input = None
    """['AnyFile', 'AnyDirectory']"""
    data2: Input = None
    """['AnyFile', 'AnyDirectory']"""
    modulename: str = 'CompareModule'
    """string"""
    param1: str = '1'
    """string"""
    sourcezipfilename: str = 'mysteps.zip'
    """string"""


class _ComparemoduleOutput:
    output: Output = None
    """AnyFile"""


class _ComparemoduleComponent(Component):
    inputs: _ComparemoduleInput
    outputs: _ComparemoduleOutput
    runsettings: _CommandComponentRunsetting


_comparemodule = None


def comparemodule(
    data1: Path = None,
    data2: Path = None,
    modulename: str = 'CompareModule',
    param1: str = '1',
    sourcezipfilename: str = 'mysteps.zip',
) -> _ComparemoduleComponent:
    """CompareModule
    
    :param data1: ['AnyFile', 'AnyDirectory']
    :type data1: Path
    :param data2: ['AnyFile', 'AnyDirectory']
    :type data2: Path
    :param modulename: string
    :type modulename: str
    :param param1: string
    :type param1: str
    :param sourcezipfilename: string
    :type sourcezipfilename: str
    :output output: AnyFile
    :type: output: Output
    """
    global _comparemodule
    if _comparemodule is None:
        _comparemodule = Component.load(
            _workspace.lisal_amlservice(),
            name='CompareModule', version='0.1.1')
    return _comparemodule(
            data1=data1,
            data2=data2,
            modulename=modulename,
            param1=param1,
            sourcezipfilename=sourcezipfilename,)


class _SampleModuleCleaningModeEnum(Enum):
    custom_substitution_value = 'Custom substitution value'
    replace_with_mean = 'Replace with mean'
    replace_with_median = 'Replace with median'
    replace_with_mode = 'Replace with mode'
    remove_entire_row = 'Remove entire row'
    remove_entire_column = 'Remove entire column'


class _SampleModuleColsWithAllMissingValuesEnum(Enum):
    propagate = 'Propagate'
    remove = 'Remove'


class _SampleModuleInput:
    dataset: Input = None
    """Dataset to be cleaned"""
    columns_to_be_cleaned: str = None
    """Columns for missing values clean operation"""
    minimum_missing_value_ratio: float = 0.0
    """Clean only column with missing value ratio above specified value, out of set of all selected columns (max: 1.0)"""
    maximum_missing_value_ratio: float = 1.0
    """Clean only columns with missing value ratio below specified value, out of set of all selected columns (max: 1.0)"""
    cleaning_mode: _SampleModuleCleaningModeEnum = _SampleModuleCleaningModeEnum.custom_substitution_value
    """Algorithm to clean missing values (enum: ['Custom substitution value', 'Replace with mean', 'Replace with median', 'Replace with mode', 'Remove entire row', 'Remove entire column'])"""
    replacement_value: str = '0'
    """Type the value that takes the place of missing values (optional)"""
    generate_missing_value_indicator_column: bool = False
    """Generate a column that indicates which rows were cleaned (optional)"""
    cols_with_all_missing_values: _SampleModuleColsWithAllMissingValuesEnum = _SampleModuleColsWithAllMissingValuesEnum.remove
    """Cols with all missing values (optional, enum: ['Propagate', 'Remove'])"""


class _SampleModuleOutput:
    cleaned_dataset: Output = None
    """Cleaned dataset"""
    cleaning_transformation: Output = None
    """Transformation to be passed to Apply Transformation module to clean new data"""


class _SampleModuleComponent(Component):
    inputs: _SampleModuleInput
    outputs: _SampleModuleOutput
    runsettings: _CommandComponentRunsetting


_sample_module = None


def sample_module(
    dataset: Path = None,
    columns_to_be_cleaned: str = None,
    minimum_missing_value_ratio: float = 0.0,
    maximum_missing_value_ratio: float = 1.0,
    cleaning_mode: _SampleModuleCleaningModeEnum = _SampleModuleCleaningModeEnum.custom_substitution_value,
    replacement_value: str = '0',
    generate_missing_value_indicator_column: bool = False,
    cols_with_all_missing_values: _SampleModuleColsWithAllMissingValuesEnum = _SampleModuleColsWithAllMissingValuesEnum.remove,
) -> _SampleModuleComponent:
    """Specifies how to handle the values missing from a dataset.
    
    :param dataset: Dataset to be cleaned
    :type dataset: Path
    :param columns_to_be_cleaned: Columns for missing values clean operation
    :type columns_to_be_cleaned: str
    :param minimum_missing_value_ratio: Clean only column with missing value ratio above specified value, out of set of all selected columns (max: 1.0)
    :type minimum_missing_value_ratio: float
    :param maximum_missing_value_ratio: Clean only columns with missing value ratio below specified value, out of set of all selected columns (max: 1.0)
    :type maximum_missing_value_ratio: float
    :param cleaning_mode: Algorithm to clean missing values (enum: ['Custom substitution value', 'Replace with mean', 'Replace with median', 'Replace with mode', 'Remove entire row', 'Remove entire column'])
    :type cleaning_mode: _SampleModuleCleaningModeEnum
    :param replacement_value: Type the value that takes the place of missing values (optional)
    :type replacement_value: str
    :param generate_missing_value_indicator_column: Generate a column that indicates which rows were cleaned (optional)
    :type generate_missing_value_indicator_column: bool
    :param cols_with_all_missing_values: Cols with all missing values (optional, enum: ['Propagate', 'Remove'])
    :type cols_with_all_missing_values: _SampleModuleColsWithAllMissingValuesEnum
    :output cleaned_dataset: Cleaned dataset
    :type: cleaned_dataset: Output
    :output cleaning_transformation: Transformation to be passed to Apply Transformation module to clean new data
    :type: cleaning_transformation: Output
    """
    global _sample_module
    if _sample_module is None:
        _sample_module = Component.load(
            _workspace.lisal_amlservice(),
            name='Sample Module', version='0.1.0')
    return _sample_module(
            dataset=dataset,
            columns_to_be_cleaned=columns_to_be_cleaned,
            minimum_missing_value_ratio=minimum_missing_value_ratio,
            maximum_missing_value_ratio=maximum_missing_value_ratio,
            cleaning_mode=cleaning_mode,
            replacement_value=replacement_value,
            generate_missing_value_indicator_column=generate_missing_value_indicator_column,
            cols_with_all_missing_values=cols_with_all_missing_values,)


class _Convert2SsInput:
    TextData: Input = None
    """text file on ADLS storage"""
    ExtractionClause: str = None
    """the extraction clause, something like \"column1:string, column2:int\""""


class _Convert2SsOutput:
    SSPath: Output = None
    """the converted structured stream"""


class _Convert2SsComponent(Component):
    inputs: _Convert2SsInput
    outputs: _Convert2SsOutput
    runsettings: _ScopeComponentRunsetting


_convert2ss = None


def convert2ss(
    TextData: Path = None,
    ExtractionClause: str = None,
) -> _Convert2SsComponent:
    """Convert adls test data to SS format
    
    :param TextData: text file on ADLS storage
    :type TextData: Path
    :param ExtractionClause: the extraction clause, something like \"column1:string, column2:int\"
    :type ExtractionClause: str
    :output SSPath: the converted structured stream
    :type: SSPath: Output
    """
    global _convert2ss
    if _convert2ss is None:
        _convert2ss = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/convert2ss/0.0.1/convert2ss.yaml")
    return _convert2ss(
            TextData=TextData,
            ExtractionClause=ExtractionClause,)


class _EselectInput:
    input: Input = None
    """the input file path, only TSV supported"""
    columns: str = None
    """column name list with ; as delimeter"""


class _EselectOutput:
    output: Output = None
    """the output file path"""


class _EselectComponent(Component):
    inputs: _EselectInput
    outputs: _EselectOutput
    runsettings: _CommandComponentRunsetting


_eselect = None


def eselect(
    input: Path = None,
    columns: str = None,
) -> _EselectComponent:
    """Selects columns from input file based on the column description in the first line. Similar to cut (and grep), but column names can be used.
    
    :param input: the input file path, only TSV supported
    :type input: Path
    :param columns: column name list with ; as delimeter
    :type columns: str
    :output output: the output file path
    :type: output: Output
    """
    global _eselect
    if _eselect is None:
        _eselect = Component.load(
            _workspace.lisal_amlservice(),
            name='eselect', version='0.0.1')
    return _eselect(
            input=input,
            columns=columns,)


class _LisalAmlserviceCompareInput:
    model1: Input = None
    """The first model to compare with"""
    eval_result1: Input = None
    """The evaluation result of first model"""
    model2: Input = None
    """The second model to compare"""
    eval_result2: Input = None
    """The evaluation result of second model"""
    metrics: str = None
    """The metrics to select better model"""


class _LisalAmlserviceCompareOutput:
    best_model: Output = None
    """The better model among the two"""


class _LisalAmlserviceCompareComponent(Component):
    inputs: _LisalAmlserviceCompareInput
    outputs: _LisalAmlserviceCompareOutput
    runsettings: _CommandComponentRunsetting


_lisal_amlservice_compare = None


def lisal_amlservice_compare(
    model1: Path = None,
    eval_result1: Path = None,
    model2: Path = None,
    eval_result2: Path = None,
    metrics: str = None,
) -> _LisalAmlserviceCompareComponent:
    """lisal-amlservice://Compare
    
    :param model1: The first model to compare with
    :type model1: Path
    :param eval_result1: The evaluation result of first model
    :type eval_result1: Path
    :param model2: The second model to compare
    :type model2: Path
    :param eval_result2: The evaluation result of second model
    :type eval_result2: Path
    :param metrics: The metrics to select better model
    :type metrics: str
    :output best_model: The better model among the two
    :type: best_model: Output
    """
    global _lisal_amlservice_compare
    if _lisal_amlservice_compare is None:
        _lisal_amlservice_compare = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/lisal_amlservice_compare/0.0.1/compare_entry.spec.yaml")
    return _lisal_amlservice_compare(
            model1=model1,
            eval_result1=eval_result1,
            model2=model2,
            eval_result2=eval_result2,
            metrics=metrics,)


class _LisalAmlservicePar15Input:
    input_files: Input = None
    """AnyDirectory"""
    side_input: Input = None
    """AnyDirectory(optional)"""
    param0: str = 'abc'
    """string (optional)"""
    param1: int = 10
    """integer (optional)"""


class _LisalAmlservicePar15Output:
    output_dir: Output = None
    """AnyDirectory"""


class _LisalAmlservicePar15Component(Component):
    inputs: _LisalAmlservicePar15Input
    outputs: _LisalAmlservicePar15Output
    runsettings: _ParallelComponentRunsetting


_lisal_amlservice_par15 = None


def lisal_amlservice_par15(
    input_files: Path = None,
    side_input: Path = None,
    param0: str = 'abc',
    param1: int = 10,
) -> _LisalAmlservicePar15Component:
    """lisal-amlservice://par15
    
    :param input_files: AnyDirectory
    :type input_files: Path
    :param side_input: AnyDirectory(optional)
    :type side_input: Path
    :param param0: string (optional)
    :type param0: str
    :param param1: integer (optional)
    :type param1: int
    :output output_dir: AnyDirectory
    :type: output_dir: Output
    """
    global _lisal_amlservice_par15
    if _lisal_amlservice_par15 is None:
        _lisal_amlservice_par15 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/lisal_amlservice_par15/0.0.2/par15.spec.yaml")
    return _lisal_amlservice_par15(
            input_files=input_files,
            side_input=side_input,
            param0=param0,
            param1=param1,)


class _MicrosoftComAzuremlSamplesXgbregressortrainingInput:
    Training_Data: Input = None
    """DataFrameDirectory"""
    Lable_Col: str = None
    """Lable column in the dataset."""
    Model_FileName: str = None
    """Name of the model file."""
    Learning_rate: float = 0.1
    """Boosting learning rate"""
    Max_depth: int = 5
    """Maximum tree depth for base learners."""


class _MicrosoftComAzuremlSamplesXgbregressortrainingOutput:
    Model_Path: Output = None
    """AnyDirectory"""


class _MicrosoftComAzuremlSamplesXgbregressortrainingComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesXgbregressortrainingInput
    outputs: _MicrosoftComAzuremlSamplesXgbregressortrainingOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_xgbregressortraining = None


def microsoft_com_azureml_samples_xgbregressortraining(
    Training_Data: Path = None,
    Lable_Col: str = None,
    Model_FileName: str = None,
    Learning_rate: float = 0.1,
    Max_depth: int = 5,
) -> _MicrosoftComAzuremlSamplesXgbregressortrainingComponent:
    """microsoft.com.azureml.samples.XGBRegressorTraining
    
    :param Training_Data: DataFrameDirectory
    :type Training_Data: Path
    :param Lable_Col: Lable column in the dataset.
    :type Lable_Col: str
    :param Model_FileName: Name of the model file.
    :type Model_FileName: str
    :param Learning_rate: Boosting learning rate
    :type Learning_rate: float
    :param Max_depth: Maximum tree depth for base learners.
    :type Max_depth: int
    :output Model_Path: AnyDirectory
    :type: Model_Path: Output
    """
    global _microsoft_com_azureml_samples_xgbregressortraining
    if _microsoft_com_azureml_samples_xgbregressortraining is None:
        _microsoft_com_azureml_samples_xgbregressortraining = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_xgbregressortraining/0.0.2/https:/github.com/Azure/AzureMachineLearningGallery/blob/main/components/automobile-price-prediction/xgboost-regressor-training/XGBRegressorTraining.spec.yaml")
    return _microsoft_com_azureml_samples_xgbregressortraining(
            Training_Data=Training_Data,
            Lable_Col=Lable_Col,
            Model_FileName=Model_FileName,
            Learning_rate=Learning_rate,
            Max_depth=Max_depth,)


class _MicrosoftComAzuremlSamplesCompare2ModelsInput:
    model1: Input = None
    """The first model to compare with(optional)"""
    eval_result1: Input = None
    """The evaluation result of first model(optional)"""
    model2: Input = None
    """The second model to compare(optional)"""
    eval_result2: Input = None
    """The evaluation result of second model(optional)"""


class _MicrosoftComAzuremlSamplesCompare2ModelsOutput:
    best_model: Output = None
    """The better model among the two"""
    best_result: Output = None
    """The better model evaluation result among the two"""


class _MicrosoftComAzuremlSamplesCompare2ModelsComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesCompare2ModelsInput
    outputs: _MicrosoftComAzuremlSamplesCompare2ModelsOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_compare_2_models = None


def microsoft_com_azureml_samples_compare_2_models(
    model1: Path = None,
    eval_result1: Path = None,
    model2: Path = None,
    eval_result2: Path = None,
) -> _MicrosoftComAzuremlSamplesCompare2ModelsComponent:
    """A dummy comparison module takes two models as input and outputs the better one
    
    :param model1: The first model to compare with(optional)
    :type model1: Path
    :param eval_result1: The evaluation result of first model(optional)
    :type eval_result1: Path
    :param model2: The second model to compare(optional)
    :type model2: Path
    :param eval_result2: The evaluation result of second model(optional)
    :type eval_result2: Path
    :output best_model: The better model among the two
    :type: best_model: Output
    :output best_result: The better model evaluation result among the two
    :type: best_result: Output
    """
    global _microsoft_com_azureml_samples_compare_2_models
    if _microsoft_com_azureml_samples_compare_2_models is None:
        _microsoft_com_azureml_samples_compare_2_models = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_compare_2_models/0.1.0/https:/github.com/lisagreenview/hello-aml-modules/blob/master/train-score-eval/compare2.yaml")
    return _microsoft_com_azureml_samples_compare_2_models(
            model1=model1,
            eval_result1=eval_result1,
            model2=model2,
            eval_result2=eval_result2,)


class _MicrosoftComAzuremlSamplesEvaluateInput:
    scoring_result: Input = None
    """Scoring result file in TSV format"""


class _MicrosoftComAzuremlSamplesEvaluateOutput:
    eval_output: Output = None
    """Evaluation result"""


class _MicrosoftComAzuremlSamplesEvaluateComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesEvaluateInput
    outputs: _MicrosoftComAzuremlSamplesEvaluateOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_evaluate = None


def microsoft_com_azureml_samples_evaluate(
    scoring_result: Path = None,
) -> _MicrosoftComAzuremlSamplesEvaluateComponent:
    """A dummy evaluate module
    
    :param scoring_result: Scoring result file in TSV format
    :type scoring_result: Path
    :output eval_output: Evaluation result
    :type: eval_output: Output
    """
    global _microsoft_com_azureml_samples_evaluate
    if _microsoft_com_azureml_samples_evaluate is None:
        _microsoft_com_azureml_samples_evaluate = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_evaluate/0.0.5/eval.yaml")
    return _microsoft_com_azureml_samples_evaluate(
            scoring_result=scoring_result,)


class _MicrosoftComAzuremlSamplesScoreInput:
    model_input: Input = None
    """Zipped model file"""
    test_data: Input = None
    """Test data organized in the torchvision format/structure"""


class _MicrosoftComAzuremlSamplesScoreOutput:
    score_output: Output = None
    """The scoring result in TSV"""


class _MicrosoftComAzuremlSamplesScoreComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesScoreInput
    outputs: _MicrosoftComAzuremlSamplesScoreOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_score = None


def microsoft_com_azureml_samples_score(
    model_input: Path = None,
    test_data: Path = None,
) -> _MicrosoftComAzuremlSamplesScoreComponent:
    """A dummy scoring module
    
    :param model_input: Zipped model file
    :type model_input: Path
    :param test_data: Test data organized in the torchvision format/structure
    :type test_data: Path
    :output score_output: The scoring result in TSV
    :type: score_output: Output
    """
    global _microsoft_com_azureml_samples_score
    if _microsoft_com_azureml_samples_score is None:
        _microsoft_com_azureml_samples_score = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_score/0.0.4/score.yaml")
    return _microsoft_com_azureml_samples_score(
            model_input=model_input,
            test_data=test_data,)


class _MicrosoftComAzuremlSamplesTrainInput:
    training_data: Input = None
    """Training data organized in the torchvision format/structure"""
    max_epochs: int = None
    """Maximum number of epochs for the training"""
    learning_rate: float = 0.01
    """Learning rate, default is 0.01"""


class _MicrosoftComAzuremlSamplesTrainOutput:
    model_output: Output = None
    """The output model"""


class _MicrosoftComAzuremlSamplesTrainComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesTrainInput
    outputs: _MicrosoftComAzuremlSamplesTrainOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_train = None


def microsoft_com_azureml_samples_train(
    training_data: Path = None,
    max_epochs: int = None,
    learning_rate: float = 0.01,
) -> _MicrosoftComAzuremlSamplesTrainComponent:
    """A dummy training module
    
    :param training_data: Training data organized in the torchvision format/structure
    :type training_data: Path
    :param max_epochs: Maximum number of epochs for the training
    :type max_epochs: int
    :param learning_rate: Learning rate, default is 0.01
    :type learning_rate: float
    :output model_output: The output model
    :type: model_output: Output
    """
    global _microsoft_com_azureml_samples_train
    if _microsoft_com_azureml_samples_train is None:
        _microsoft_com_azureml_samples_train = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_train/0.0.4/train.yaml")
    return _microsoft_com_azureml_samples_train(
            training_data=training_data,
            max_epochs=max_epochs,
            learning_rate=learning_rate,)


class _MicrosoftComAzuremlSamplesTrainTestInput:
    training_data: Input = None
    """Training data organized in the torchvision format/structure"""
    max_epochs: int = None
    """Maximum number of epochs for the training"""
    learning_rate: float = 0.01
    """Learning rate, default is 0.01"""


class _MicrosoftComAzuremlSamplesTrainTestOutput:
    model_output: Output = None
    """The output model"""


class _MicrosoftComAzuremlSamplesTrainTestComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesTrainTestInput
    outputs: _MicrosoftComAzuremlSamplesTrainTestOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_train_test = None


def microsoft_com_azureml_samples_train_test(
    training_data: Path = None,
    max_epochs: int = None,
    learning_rate: float = 0.01,
) -> _MicrosoftComAzuremlSamplesTrainTestComponent:
    """# A dummy training module
- list 1
- list 2

    
    :param training_data: Training data organized in the torchvision format/structure
    :type training_data: Path
    :param max_epochs: Maximum number of epochs for the training
    :type max_epochs: int
    :param learning_rate: Learning rate, default is 0.01
    :type learning_rate: float
    :output model_output: The output model
    :type: model_output: Output
    """
    global _microsoft_com_azureml_samples_train_test
    if _microsoft_com_azureml_samples_train_test is None:
        _microsoft_com_azureml_samples_train_test = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_train_test/0.0.5/train.yaml")
    return _microsoft_com_azureml_samples_train_test(
            training_data=training_data,
            max_epochs=max_epochs,
            learning_rate=learning_rate,)


class _MicrosoftComAmlSamplesCompareInput:
    input01: Input = None
    """AnyFile(optional)"""
    input02: Input = None
    """AnyFile(optional)"""
    input03: Input = None
    """AnyFile(optional)"""
    input04: Input = None
    """AnyFile(optional)"""
    input05: Input = None
    """AnyFile(optional)"""
    input06: Input = None
    """AnyFile(optional)"""
    input07: Input = None
    """AnyFile(optional)"""
    input08: Input = None
    """AnyFile(optional)"""
    input09: Input = None
    """AnyFile(optional)"""
    input10: Input = None
    """AnyFile(optional)"""


class _MicrosoftComAmlSamplesCompareOutput:
    compare_output: Output = None
    """AnyDirectory"""


class _MicrosoftComAmlSamplesCompareComponent(Component):
    inputs: _MicrosoftComAmlSamplesCompareInput
    outputs: _MicrosoftComAmlSamplesCompareOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_compare = None


def microsoft_com_aml_samples_compare(
    input01: Path = None,
    input02: Path = None,
    input03: Path = None,
    input04: Path = None,
    input05: Path = None,
    input06: Path = None,
    input07: Path = None,
    input08: Path = None,
    input09: Path = None,
    input10: Path = None,
) -> _MicrosoftComAmlSamplesCompareComponent:
    """microsoft.com/aml/samples://Compare
    
    :param input01: AnyFile(optional)
    :type input01: Path
    :param input02: AnyFile(optional)
    :type input02: Path
    :param input03: AnyFile(optional)
    :type input03: Path
    :param input04: AnyFile(optional)
    :type input04: Path
    :param input05: AnyFile(optional)
    :type input05: Path
    :param input06: AnyFile(optional)
    :type input06: Path
    :param input07: AnyFile(optional)
    :type input07: Path
    :param input08: AnyFile(optional)
    :type input08: Path
    :param input09: AnyFile(optional)
    :type input09: Path
    :param input10: AnyFile(optional)
    :type input10: Path
    :output compare_output: AnyDirectory
    :type: compare_output: Output
    """
    global _microsoft_com_aml_samples_compare
    if _microsoft_com_aml_samples_compare is None:
        _microsoft_com_aml_samples_compare = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_compare/0.0.1/compare.yaml")
    return _microsoft_com_aml_samples_compare(
            input01=input01,
            input02=input02,
            input03=input03,
            input04=input04,
            input05=input05,
            input06=input06,
            input07=input07,
            input08=input08,
            input09=input09,
            input10=input10,)


class _MicrosoftComAmlSamplesCompare2ModelsInput:
    model1: Input = None
    """The first model to compare with(optional)"""
    eval_result1: Input = None
    """The evaluation result of first model(optional)"""
    model2: Input = None
    """The second model to compare(optional)"""
    eval_result2: Input = None
    """The evaluation result of second model(optional)"""


class _MicrosoftComAmlSamplesCompare2ModelsOutput:
    best_model: Output = None
    """The better model among the two"""
    best_result: Output = None
    """The better model evaluation result among the two"""


class _MicrosoftComAmlSamplesCompare2ModelsComponent(Component):
    inputs: _MicrosoftComAmlSamplesCompare2ModelsInput
    outputs: _MicrosoftComAmlSamplesCompare2ModelsOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_compare_2_models = None


def microsoft_com_aml_samples_compare_2_models(
    model1: Path = None,
    eval_result1: Path = None,
    model2: Path = None,
    eval_result2: Path = None,
) -> _MicrosoftComAmlSamplesCompare2ModelsComponent:
    """A dummy comparison module takes two models as input and outputs the better one
    
    :param model1: The first model to compare with(optional)
    :type model1: Path
    :param eval_result1: The evaluation result of first model(optional)
    :type eval_result1: Path
    :param model2: The second model to compare(optional)
    :type model2: Path
    :param eval_result2: The evaluation result of second model(optional)
    :type eval_result2: Path
    :output best_model: The better model among the two
    :type: best_model: Output
    :output best_result: The better model evaluation result among the two
    :type: best_result: Output
    """
    global _microsoft_com_aml_samples_compare_2_models
    if _microsoft_com_aml_samples_compare_2_models is None:
        _microsoft_com_aml_samples_compare_2_models = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_compare_2_models/0.0.10/https:/github.com/lisagreenview/hello-aml-modules/blob/master/train-score-eval/compare2.yaml")
    return _microsoft_com_aml_samples_compare_2_models(
            model1=model1,
            eval_result1=eval_result1,
            model2=model2,
            eval_result2=eval_result2,)


class _MicrosoftComAmlSamplesEvaluateInput:
    scoring_result: Input = None
    """Scoring result file in TSV format"""


class _MicrosoftComAmlSamplesEvaluateOutput:
    eval_output: Output = None
    """Evaluation result"""


class _MicrosoftComAmlSamplesEvaluateComponent(Component):
    inputs: _MicrosoftComAmlSamplesEvaluateInput
    outputs: _MicrosoftComAmlSamplesEvaluateOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_evaluate = None


def microsoft_com_aml_samples_evaluate(
    scoring_result: Path = None,
) -> _MicrosoftComAmlSamplesEvaluateComponent:
    """A dummy evaluate module
    
    :param scoring_result: Scoring result file in TSV format
    :type scoring_result: Path
    :output eval_output: Evaluation result
    :type: eval_output: Output
    """
    global _microsoft_com_aml_samples_evaluate
    if _microsoft_com_aml_samples_evaluate is None:
        _microsoft_com_aml_samples_evaluate = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_evaluate/0.0.8/https:/github.com/lisagreenview/hello-aml-modules/blob/master/train-score-eval/eval.yaml")
    return _microsoft_com_aml_samples_evaluate(
            scoring_result=scoring_result,)


class _MicrosoftComAmlSamplesMpiTrainInput:
    training_data: Input = None
    """Training data organized in the torchvision format/structure"""
    max_epochs: int = None
    """Maximum number of epochs for the training"""
    learning_rate: float = 0.01
    """Learning rate, default is 0.01"""


class _MicrosoftComAmlSamplesMpiTrainOutput:
    model_output: Output = None
    """The output model (zipped)"""


class _MicrosoftComAmlSamplesMpiTrainComponent(Component):
    inputs: _MicrosoftComAmlSamplesMpiTrainInput
    outputs: _MicrosoftComAmlSamplesMpiTrainOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_aml_samples_mpi_train = None


def microsoft_com_aml_samples_mpi_train(
    training_data: Path = None,
    max_epochs: int = None,
    learning_rate: float = 0.01,
) -> _MicrosoftComAmlSamplesMpiTrainComponent:
    """A dummy module to show how to describe MPI module with custom module spec.
    
    :param training_data: Training data organized in the torchvision format/structure
    :type training_data: Path
    :param max_epochs: Maximum number of epochs for the training
    :type max_epochs: int
    :param learning_rate: Learning rate, default is 0.01
    :type learning_rate: float
    :output model_output: The output model (zipped)
    :type: model_output: Output
    """
    global _microsoft_com_aml_samples_mpi_train
    if _microsoft_com_aml_samples_mpi_train is None:
        _microsoft_com_aml_samples_mpi_train = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_mpi_train/0.0.10/https:/github.com/lisagreenview/hello-aml-modules/blob/master/train-score-eval/mpi_train.yaml")
    return _microsoft_com_aml_samples_mpi_train(
            training_data=training_data,
            max_epochs=max_epochs,
            learning_rate=learning_rate,)


class _MicrosoftComAmlSamplesScoreInput:
    model_input: Input = None
    """Zipped model file"""
    test_data: Input = None
    """Test data organized in the torchvision format/structure"""


class _MicrosoftComAmlSamplesScoreOutput:
    score_output: Output = None
    """The scoring result in TSV"""


class _MicrosoftComAmlSamplesScoreComponent(Component):
    inputs: _MicrosoftComAmlSamplesScoreInput
    outputs: _MicrosoftComAmlSamplesScoreOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_score = None


def microsoft_com_aml_samples_score(
    model_input: Path = None,
    test_data: Path = None,
) -> _MicrosoftComAmlSamplesScoreComponent:
    """A dummy scoring module
    
    :param model_input: Zipped model file
    :type model_input: Path
    :param test_data: Test data organized in the torchvision format/structure
    :type test_data: Path
    :output score_output: The scoring result in TSV
    :type: score_output: Output
    """
    global _microsoft_com_aml_samples_score
    if _microsoft_com_aml_samples_score is None:
        _microsoft_com_aml_samples_score = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_score/0.0.6/https:/github.com/lisagreenview/hello-aml-modules/blob/master/train-score-eval/score.yaml")
    return _microsoft_com_aml_samples_score(
            model_input=model_input,
            test_data=test_data,)


class _MicrosoftComAmlSamplesTrainInput:
    training_data_organized_in_the_torchvision_format_structure: Input = None
    """['AnyFile', 'AnyDirectory']"""
    max_epochs: int = None
    """integer"""
    learning_rate: float = 0.01
    """float"""


class _MicrosoftComAmlSamplesTrainOutput:
    the_output_model_zipped: Output = None
    """AnyFile"""


class _MicrosoftComAmlSamplesTrainComponent(Component):
    inputs: _MicrosoftComAmlSamplesTrainInput
    outputs: _MicrosoftComAmlSamplesTrainOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_train = None


def microsoft_com_aml_samples_train(
    training_data_organized_in_the_torchvision_format_structure: Path = None,
    max_epochs: int = None,
    learning_rate: float = 0.01,
) -> _MicrosoftComAmlSamplesTrainComponent:
    """microsoft.com/aml/samples://Train
    
    :param training_data_organized_in_the_torchvision_format_structure: ['AnyFile', 'AnyDirectory']
    :type training_data_organized_in_the_torchvision_format_structure: Path
    :param max_epochs: integer
    :type max_epochs: int
    :param learning_rate: float
    :type learning_rate: float
    :output the_output_model_zipped: AnyFile
    :type: the_output_model_zipped: Output
    """
    global _microsoft_com_aml_samples_train
    if _microsoft_com_aml_samples_train is None:
        _microsoft_com_aml_samples_train = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_train/0.0.5/train.yaml")
    return _microsoft_com_aml_samples_train(
            training_data_organized_in_the_torchvision_format_structure=training_data_organized_in_the_torchvision_format_structure,
            max_epochs=max_epochs,
            learning_rate=learning_rate,)


class _MicrosoftComAmlSamplesToDfdInput:
    input: Input = None
    """AnyDirectory"""


class _MicrosoftComAmlSamplesToDfdOutput:
    output: Output = None
    """DataFrameDirectory"""


class _MicrosoftComAmlSamplesToDfdComponent(Component):
    inputs: _MicrosoftComAmlSamplesToDfdInput
    outputs: _MicrosoftComAmlSamplesToDfdOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_aml_samples_to_dfd = None


def microsoft_com_aml_samples_to_dfd(
    input: Path = None,
) -> _MicrosoftComAmlSamplesToDfdComponent:
    """Convert tsv/csv file to dataframe directory with simple visualization
    
    :param input: AnyDirectory
    :type input: Path
    :output output: DataFrameDirectory
    :type: output: Output
    """
    global _microsoft_com_aml_samples_to_dfd
    if _microsoft_com_aml_samples_to_dfd is None:
        _microsoft_com_aml_samples_to_dfd = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_samples_to_dfd/0.0.1/amlmodule.yaml")
    return _microsoft_com_aml_samples_to_dfd(
            input=input,)


class _MicrosoftComAmlScTokenizerModeEnum(Enum):
    train = 'train'
    inference = 'inference'
    spacy = 'spacy'


class _MicrosoftComAmlScTokenizerTypeEnum(Enum):
    word = 'word'
    sentence = 'sentence'


class _MicrosoftComAmlScTokenizerInput:
    input_file_path: Input = None
    """Input text file path"""
    input_is_tsv: bool = False
    """bool determining whether to use tsv related options (optional)"""
    delimiter: str = None
    """optional, delimiter to use if parsing a tsv type file (optional)"""
    ignore_cols: str = None
    """indices of columns to ignore if parsing a tsv (optional)"""
    mode: _MicrosoftComAmlScTokenizerModeEnum = _MicrosoftComAmlScTokenizerModeEnum.train
    """Tokenizer to use [train, inference, spacy] (enum: ['train', 'inference', 'spacy'])"""
    type: _MicrosoftComAmlScTokenizerTypeEnum = _MicrosoftComAmlScTokenizerTypeEnum.word
    """Whether to use word tokenizer or sentence tokenizer (enum: ['word', 'sentence'])"""


class _MicrosoftComAmlScTokenizerOutput:
    output_dir_path: Output = None
    """Output file directory path"""


class _MicrosoftComAmlScTokenizerComponent(Component):
    inputs: _MicrosoftComAmlScTokenizerInput
    outputs: _MicrosoftComAmlScTokenizerOutput
    runsettings: _ParallelComponentRunsetting


_microsoft_com_aml_sc_tokenizer = None


def microsoft_com_aml_sc_tokenizer(
    input_file_path: Path = None,
    input_is_tsv: bool = False,
    delimiter: str = None,
    ignore_cols: str = None,
    mode: _MicrosoftComAmlScTokenizerModeEnum = _MicrosoftComAmlScTokenizerModeEnum.train,
    type: _MicrosoftComAmlScTokenizerTypeEnum = _MicrosoftComAmlScTokenizerTypeEnum.word,
) -> _MicrosoftComAmlScTokenizerComponent:
    """Three different tokenizers, 1) TrainingTokenizer -- mimics the tokenization method used for tokenizing words for training LM in QAS; 2)InferenceTokenizer -- mimics the tokenization method used for tokenizing words for trie lookup; 3)SpacyTokenizer -- uses spaCy's default word/sentence tokenizer
    
    :param input_file_path: Input text file path
    :type input_file_path: Path
    :param input_is_tsv: bool determining whether to use tsv related options (optional)
    :type input_is_tsv: bool
    :param delimiter: optional, delimiter to use if parsing a tsv type file (optional)
    :type delimiter: str
    :param ignore_cols: indices of columns to ignore if parsing a tsv (optional)
    :type ignore_cols: str
    :param mode: Tokenizer to use [train, inference, spacy] (enum: ['train', 'inference', 'spacy'])
    :type mode: _MicrosoftComAmlScTokenizerModeEnum
    :param type: Whether to use word tokenizer or sentence tokenizer (enum: ['word', 'sentence'])
    :type type: _MicrosoftComAmlScTokenizerTypeEnum
    :output output_dir_path: Output file directory path
    :type: output_dir_path: Output
    """
    global _microsoft_com_aml_sc_tokenizer
    if _microsoft_com_aml_sc_tokenizer is None:
        _microsoft_com_aml_sc_tokenizer = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_aml_sc_tokenizer/0.0.10/module_spec.yaml")
    return _microsoft_com_aml_sc_tokenizer(
            input_file_path=input_file_path,
            input_is_tsv=input_is_tsv,
            delimiter=delimiter,
            ignore_cols=ignore_cols,
            mode=mode,
            type=type,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput10Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput10Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput10Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput10Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput10Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_10 = None


def microsoft_com_azureml_samples1_o_hello_world_output_10(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput10Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_10
    if _microsoft_com_azureml_samples1_o_hello_world_output_10 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_10 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_10/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_10(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput11Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput11Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput11Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput11Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput11Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_11 = None


def microsoft_com_azureml_samples1_o_hello_world_output_11(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput11Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_11
    if _microsoft_com_azureml_samples1_o_hello_world_output_11 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_11 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_11/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_11(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput12Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput12Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput12Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput12Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput12Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_12 = None


def microsoft_com_azureml_samples1_o_hello_world_output_12(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput12Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_12
    if _microsoft_com_azureml_samples1_o_hello_world_output_12 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_12 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_12/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_12(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput2Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput2Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput2Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput2Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput2Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_2 = None


def microsoft_com_azureml_samples1_o_hello_world_output_2(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput2Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_2
    if _microsoft_com_azureml_samples1_o_hello_world_output_2 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_2 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_2/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_2(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput3Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput3Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput3Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput3Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput3Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_3 = None


def microsoft_com_azureml_samples1_o_hello_world_output_3(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput3Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_3
    if _microsoft_com_azureml_samples1_o_hello_world_output_3 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_3 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_3/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_3(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput4Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput4Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput4Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput4Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput4Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_4 = None


def microsoft_com_azureml_samples1_o_hello_world_output_4(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput4Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_4
    if _microsoft_com_azureml_samples1_o_hello_world_output_4 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_4 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_4/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_4(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput5Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput5Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput5Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput5Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput5Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_5 = None


def microsoft_com_azureml_samples1_o_hello_world_output_5(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput5Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_5
    if _microsoft_com_azureml_samples1_o_hello_world_output_5 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_5 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_5/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_5(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput6Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput6Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput6Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput6Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput6Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_6 = None


def microsoft_com_azureml_samples1_o_hello_world_output_6(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput6Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_6
    if _microsoft_com_azureml_samples1_o_hello_world_output_6 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_6 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_6/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_6(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput7Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput7Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput7Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput7Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput7Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_7 = None


def microsoft_com_azureml_samples1_o_hello_world_output_7(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput7Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_7
    if _microsoft_com_azureml_samples1_o_hello_world_output_7 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_7 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_7/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_7(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput8Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput8Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput8Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput8Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput8Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_8 = None


def microsoft_com_azureml_samples1_o_hello_world_output_8(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput8Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_8
    if _microsoft_com_azureml_samples1_o_hello_world_output_8 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_8 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_8/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_8(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1OHelloWorldOutput9Input:
    input_path: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput9Output:
    output_path: Output = None
    """The directory contains a dataframe."""
    output_path_1: Output = None
    """The directory contains dataframe."""
    output_path_2: Output = None
    """The directory contains dataframe."""
    output_path_3: Output = None
    """The directory contains dataframe."""
    output_path_4: Output = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1OHelloWorldOutput9Component(Component):
    inputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput9Input
    outputs: _MicrosoftComAzuremlSamples1OHelloWorldOutput9Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_o_hello_world_output_9 = None


def microsoft_com_azureml_samples1_o_hello_world_output_9(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamples1OHelloWorldOutput9Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    :output output_path_1: The directory contains dataframe.
    :type: output_path_1: Output
    :output output_path_2: The directory contains dataframe.
    :type: output_path_2: Output
    :output output_path_3: The directory contains dataframe.
    :type: output_path_3: Output
    :output output_path_4: The directory contains dataframe.
    :type: output_path_4: Output
    """
    global _microsoft_com_azureml_samples1_o_hello_world_output_9
    if _microsoft_com_azureml_samples1_o_hello_world_output_9 is None:
        _microsoft_com_azureml_samples1_o_hello_world_output_9 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_o_hello_world_output_9/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_o_hello_world_output_9(
            input_path=input_path,)


class _MicrosoftComAzuremlSamples1HelloWorldInput:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldOutput:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldComponent(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput
    outputs: _MicrosoftComAzuremlSamples1HelloWorldOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world = None


def microsoft_com_azureml_samples1_hello_world(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldComponent:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world
    if _microsoft_com_azureml_samples1_hello_world is None:
        _microsoft_com_azureml_samples1_hello_world = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world/0.0.2/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput0Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput0Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput0Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput0Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput0Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_0 = None


def microsoft_com_azureml_samples1_hello_world_input_0(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput0Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_0
    if _microsoft_com_azureml_samples1_hello_world_input_0 is None:
        _microsoft_com_azureml_samples1_hello_world_input_0 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_0/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_0(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput10Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput10Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput10Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput10Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput10Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_10 = None


def microsoft_com_azureml_samples1_hello_world_input_10(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput10Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_10
    if _microsoft_com_azureml_samples1_hello_world_input_10 is None:
        _microsoft_com_azureml_samples1_hello_world_input_10 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_10/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_10(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput11Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput11Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput11Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput11Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput11Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_11 = None


def microsoft_com_azureml_samples1_hello_world_input_11(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput11Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_11
    if _microsoft_com_azureml_samples1_hello_world_input_11 is None:
        _microsoft_com_azureml_samples1_hello_world_input_11 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_11/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_11(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput12Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput12Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput12Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput12Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput12Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_12 = None


def microsoft_com_azureml_samples1_hello_world_input_12(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput12Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_12
    if _microsoft_com_azureml_samples1_hello_world_input_12 is None:
        _microsoft_com_azureml_samples1_hello_world_input_12 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_12/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_12(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput13Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput13Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput13Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput13Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput13Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_13 = None


def microsoft_com_azureml_samples1_hello_world_input_13(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput13Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_13
    if _microsoft_com_azureml_samples1_hello_world_input_13 is None:
        _microsoft_com_azureml_samples1_hello_world_input_13 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_13/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_13(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput2Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput2Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput2Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput2Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput2Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_2 = None


def microsoft_com_azureml_samples1_hello_world_input_2(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput2Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_2
    if _microsoft_com_azureml_samples1_hello_world_input_2 is None:
        _microsoft_com_azureml_samples1_hello_world_input_2 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_2/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_2(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput3Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput3Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput3Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput3Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput3Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_3 = None


def microsoft_com_azureml_samples1_hello_world_input_3(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput3Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_3
    if _microsoft_com_azureml_samples1_hello_world_input_3 is None:
        _microsoft_com_azureml_samples1_hello_world_input_3 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_3/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_3(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput4Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput4Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput4Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput4Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput4Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_4 = None


def microsoft_com_azureml_samples1_hello_world_input_4(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput4Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_4
    if _microsoft_com_azureml_samples1_hello_world_input_4 is None:
        _microsoft_com_azureml_samples1_hello_world_input_4 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_4/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_4(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput5Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput5Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput5Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput5Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput5Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_5 = None


def microsoft_com_azureml_samples1_hello_world_input_5(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput5Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_5
    if _microsoft_com_azureml_samples1_hello_world_input_5 is None:
        _microsoft_com_azureml_samples1_hello_world_input_5 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_5/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_5(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput6Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput6Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput6Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput6Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput6Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_6 = None


def microsoft_com_azureml_samples1_hello_world_input_6(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput6Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_6
    if _microsoft_com_azureml_samples1_hello_world_input_6 is None:
        _microsoft_com_azureml_samples1_hello_world_input_6 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_6/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_6(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput7Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput7Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput7Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput7Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput7Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_7 = None


def microsoft_com_azureml_samples1_hello_world_input_7(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput7Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_7
    if _microsoft_com_azureml_samples1_hello_world_input_7 is None:
        _microsoft_com_azureml_samples1_hello_world_input_7 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_7/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_7(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput8Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput8Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput8Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput8Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput8Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_8 = None


def microsoft_com_azureml_samples1_hello_world_input_8(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput8Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_8
    if _microsoft_com_azureml_samples1_hello_world_input_8 is None:
        _microsoft_com_azureml_samples1_hello_world_input_8 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_8/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_8(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamples1HelloWorldInput9Input:
    input_path: Input = None
    """The directory contains dataframe."""
    input_path_1: Input = None
    """The directory contains dataframe."""
    input_path_2: Input = None
    """The directory contains dataframe."""
    input_path_3: Input = None
    """The directory contains dataframe."""
    input_path_4: Input = None
    """The directory contains dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput9Output:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamples1HelloWorldInput9Component(Component):
    inputs: _MicrosoftComAzuremlSamples1HelloWorldInput9Input
    outputs: _MicrosoftComAzuremlSamples1HelloWorldInput9Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples1_hello_world_input_9 = None


def microsoft_com_azureml_samples1_hello_world_input_9(
    input_path: Path = None,
    input_path_1: Path = None,
    input_path_2: Path = None,
    input_path_3: Path = None,
    input_path_4: Path = None,
) -> _MicrosoftComAzuremlSamples1HelloWorldInput9Component:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param input_path_1: The directory contains dataframe.
    :type input_path_1: Path
    :param input_path_2: The directory contains dataframe.
    :type input_path_2: Path
    :param input_path_3: The directory contains dataframe.
    :type input_path_3: Path
    :param input_path_4: The directory contains dataframe.
    :type input_path_4: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples1_hello_world_input_9
    if _microsoft_com_azureml_samples1_hello_world_input_9 is None:
        _microsoft_com_azureml_samples1_hello_world_input_9 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples1_hello_world_input_9/0.0.0/module_spec.yaml")
    return _microsoft_com_azureml_samples1_hello_world_input_9(
            input_path=input_path,
            input_path_1=input_path_1,
            input_path_2=input_path_2,
            input_path_3=input_path_3,
            input_path_4=input_path_4,)


class _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryInput:
    input_path: Input = None
    """The directory contains multiple parquet files."""


class _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryOutput:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryInput
    outputs: _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory = None


def microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory(
    input_path: Path = None,
) -> _MicrosoftComAzuremlSamplesConvertMultiParquetFilesToDataframedirectoryComponent:
    """microsoft.com/azureml/samples://Convert Multi Parquet Files to DataFrameDirectory
    
    :param input_path: The directory contains multiple parquet files.
    :type input_path: Path
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory
    if _microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory is None:
        _microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory/0.0.1/convert_multi_parquet_to_dfd.yaml")
    return _microsoft_com_azureml_samples_convert_multi_parquet_files_to_dataframedirectory(
            input_path=input_path,)


class _MicrosoftComAzuremlSamplesFirstModuleInput:
    pass


class _MicrosoftComAzuremlSamplesFirstModuleOutput:
    pass


class _MicrosoftComAzuremlSamplesFirstModuleComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesFirstModuleInput
    outputs: _MicrosoftComAzuremlSamplesFirstModuleOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_first_module = None


def microsoft_com_azureml_samples_first_module(
) -> _MicrosoftComAzuremlSamplesFirstModuleComponent:
    """First module created for AzureML.
    
    """
    global _microsoft_com_azureml_samples_first_module
    if _microsoft_com_azureml_samples_first_module is None:
        _microsoft_com_azureml_samples_first_module = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_first_module/0.0.1/module_spec.yaml")
    return _microsoft_com_azureml_samples_first_module()


class _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum(Enum):
    option1 = 'option1'
    option2 = 'option2'
    option3 = 'option3'


class _MicrosoftComAzuremlSamplesHelloWorldInput:
    input_path: Input = None
    """The directory contains dataframe."""
    string_parameter: str = None
    """A parameter accepts a string value. (optional)"""
    int_parameter: int = 3
    """A parameter accepts an int value. (min: 1, max: 5)"""
    boolean_parameter: bool = False
    """A parameter accepts a boolean value."""
    enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum = _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum.option1
    """enum (enum: ['option1', 'option2', 'option3'])"""


class _MicrosoftComAzuremlSamplesHelloWorldOutput:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamplesHelloWorldComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesHelloWorldInput
    outputs: _MicrosoftComAzuremlSamplesHelloWorldOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_hello_world = None


def microsoft_com_azureml_samples_hello_world(
    input_path: Path = None,
    string_parameter: str = None,
    int_parameter: int = 3,
    boolean_parameter: bool = False,
    enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum = _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum.option1,
) -> _MicrosoftComAzuremlSamplesHelloWorldComponent:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param string_parameter: A parameter accepts a string value. (optional)
    :type string_parameter: str
    :param int_parameter: A parameter accepts an int value. (min: 1, max: 5)
    :type int_parameter: int
    :param boolean_parameter: A parameter accepts a boolean value.
    :type boolean_parameter: bool
    :param enum_parameter: enum (enum: ['option1', 'option2', 'option3'])
    :type enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldEnumParameterEnum
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples_hello_world
    if _microsoft_com_azureml_samples_hello_world is None:
        _microsoft_com_azureml_samples_hello_world = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_hello_world/0.0.1/module_spec.yaml")
    return _microsoft_com_azureml_samples_hello_world(
            input_path=input_path,
            string_parameter=string_parameter,
            int_parameter=int_parameter,
            boolean_parameter=boolean_parameter,
            enum_parameter=enum_parameter,)


class _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum(Enum):
    option1 = 'option1'
    option2 = 'option2'
    option3 = 'option3'


class _MicrosoftComAzuremlSamplesHelloWorldMpiJobInput:
    input_path: Input = None
    """The directory contains dataframe."""
    string_parameter: str = None
    """A parameter accepts a string value. (optional)"""
    int_parameter: int = 3
    """A parameter accepts an int value. (min: 1, max: 5)"""
    boolean_parameter: bool = False
    """A parameter accepts a boolean value."""
    enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum = _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum.option1
    """enum (enum: ['option1', 'option2', 'option3'])"""


class _MicrosoftComAzuremlSamplesHelloWorldMpiJobOutput:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamplesHelloWorldMpiJobComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesHelloWorldMpiJobInput
    outputs: _MicrosoftComAzuremlSamplesHelloWorldMpiJobOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_azureml_samples_hello_world_mpi_job = None


def microsoft_com_azureml_samples_hello_world_mpi_job(
    input_path: Path = None,
    string_parameter: str = None,
    int_parameter: int = 3,
    boolean_parameter: bool = False,
    enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum = _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum.option1,
) -> _MicrosoftComAzuremlSamplesHelloWorldMpiJobComponent:
    """A hello world tutorial to create a MPI module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param string_parameter: A parameter accepts a string value. (optional)
    :type string_parameter: str
    :param int_parameter: A parameter accepts an int value. (min: 1, max: 5)
    :type int_parameter: int
    :param boolean_parameter: A parameter accepts a boolean value.
    :type boolean_parameter: bool
    :param enum_parameter: enum (enum: ['option1', 'option2', 'option3'])
    :type enum_parameter: _MicrosoftComAzuremlSamplesHelloWorldMpiJobEnumParameterEnum
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples_hello_world_mpi_job
    if _microsoft_com_azureml_samples_hello_world_mpi_job is None:
        _microsoft_com_azureml_samples_hello_world_mpi_job = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_hello_world_mpi_job/0.0.1/module_spec.yaml")
    return _microsoft_com_azureml_samples_hello_world_mpi_job(
            input_path=input_path,
            string_parameter=string_parameter,
            int_parameter=int_parameter,
            boolean_parameter=boolean_parameter,
            enum_parameter=enum_parameter,)


class _MicrosoftComAzuremlSamplesMpiTrainInput:
    training_data: Input = None
    """Training data organized in the torchvision format/structure"""
    max_epochs: int = None
    """Maximum number of epochs for the training"""
    learning_rate: float = 0.01
    """Learning rate, default is 0.01"""


class _MicrosoftComAzuremlSamplesMpiTrainOutput:
    model_output: Output = None
    """The output model"""


class _MicrosoftComAzuremlSamplesMpiTrainComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesMpiTrainInput
    outputs: _MicrosoftComAzuremlSamplesMpiTrainOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_azureml_samples_mpi_train = None


def microsoft_com_azureml_samples_mpi_train(
    training_data: Path = None,
    max_epochs: int = None,
    learning_rate: float = 0.01,
) -> _MicrosoftComAzuremlSamplesMpiTrainComponent:
    """A dummy module to show how to describe MPI module with custom module spec.
    
    :param training_data: Training data organized in the torchvision format/structure
    :type training_data: Path
    :param max_epochs: Maximum number of epochs for the training
    :type max_epochs: int
    :param learning_rate: Learning rate, default is 0.01
    :type learning_rate: float
    :output model_output: The output model
    :type: model_output: Output
    """
    global _microsoft_com_azureml_samples_mpi_train
    if _microsoft_com_azureml_samples_mpi_train is None:
        _microsoft_com_azureml_samples_mpi_train = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_mpi_train/0.0.1/mpi_train.yaml")
    return _microsoft_com_azureml_samples_mpi_train(
            training_data=training_data,
            max_epochs=max_epochs,
            learning_rate=learning_rate,)


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum(Enum):
    adagrad = 'Adagrad'
    adam = 'Adam'
    ftrl = 'Ftrl'
    rmsprop = 'RMSProp'
    sgd = 'SGD'
    adadelta = 'Adadelta'


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum(Enum):
    adagrad = 'Adagrad'
    adam = 'Adam'
    ftrl = 'Ftrl'
    rmsprop = 'RMSProp'
    sgd = 'SGD'
    adadelta = 'Adadelta'


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum(Enum):
    relu = 'ReLU'
    sigmoid = 'Sigmoid'
    tanh = 'Tanh'
    linear = 'Linear'
    leakyrelu = 'LeakyReLU'


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderInput:
    training_dataset_of_user_item_rating_triples: Input = None
    """Ratings of items by users, expressed as triple (User, Item, Rating)"""
    epochs: int = 15
    """Maximum number of epochs to perform while training (min: 1)"""
    batch_size: int = 64
    """Number of consecutive samples to combine in a single batch"""
    wide_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum.adagrad
    """Optimizer used to apply gradients to the wide part of the model (enum: ['Adagrad', 'Adam', 'Ftrl', 'RMSProp', 'SGD', 'Adadelta'])"""
    wide_optimizer_learning_rate: float = 0.1
    """Size of each step in the learning process for wide part of the model (min: 2.220446049250313e-16, max: 2.0)"""
    crossed_feature_dimension: int = 1000
    """Crossed feature dimension for wide part model (min: 1)"""
    deep_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum.adagrad
    """Optimizer used to apply gradients to the deep part of the model (enum: ['Adagrad', 'Adam', 'Ftrl', 'RMSProp', 'SGD', 'Adadelta'])"""
    deep_optimizer_learning_rate: float = 0.1
    """Size of each step in the learning process for deep part of the model (min: 2.220446049250313e-16, max: 2.0)"""
    user_embedding_dimension: int = 16
    """User embedding dimension for deep part model (min: 1)"""
    item_embedding_dimension: int = 16
    """Item embedding dimension for deep part model (min: 1)"""
    categorical_features_embedding_dimension: int = 4
    """Categorical features embedding dimension for deep part model (min: 1)"""
    hidden_units: str = '256,128'
    """Hidden units per layer for deep part model"""
    activation_function: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum.relu
    """Activation function applied to each layer in deep part model (enum: ['ReLU', 'Sigmoid', 'Tanh', 'Linear', 'LeakyReLU'])"""
    dropout: float = 0.8
    """Probability that each element is dropped in deep part model (max: 1.0)"""
    batch_normalization: bool = True
    """Whether to use batch normalization after each hidden layer"""


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderOutput:
    trained_wide_and_deep_recommendation_model: Output = None
    """Trained Wide and Deep recommendation model"""


class _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderInput
    outputs: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender = None


def microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender(
    training_dataset_of_user_item_rating_triples: Path = None,
    epochs: int = 15,
    batch_size: int = 64,
    wide_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum.adagrad,
    wide_optimizer_learning_rate: float = 0.1,
    crossed_feature_dimension: int = 1000,
    deep_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum.adagrad,
    deep_optimizer_learning_rate: float = 0.1,
    user_embedding_dimension: int = 16,
    item_embedding_dimension: int = 16,
    categorical_features_embedding_dimension: int = 4,
    hidden_units: str = '256,128',
    activation_function: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum = _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum.relu,
    dropout: float = 0.8,
    batch_normalization: bool = True,
) -> _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderComponent:
    """Train a recommender based on Wide & Deep model.
    
    :param training_dataset_of_user_item_rating_triples: Ratings of items by users, expressed as triple (User, Item, Rating)
    :type training_dataset_of_user_item_rating_triples: Path
    :param epochs: Maximum number of epochs to perform while training (min: 1)
    :type epochs: int
    :param batch_size: Number of consecutive samples to combine in a single batch
    :type batch_size: int
    :param wide_part_optimizer: Optimizer used to apply gradients to the wide part of the model (enum: ['Adagrad', 'Adam', 'Ftrl', 'RMSProp', 'SGD', 'Adadelta'])
    :type wide_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderWidePartOptimizerEnum
    :param wide_optimizer_learning_rate: Size of each step in the learning process for wide part of the model (min: 2.220446049250313e-16, max: 2.0)
    :type wide_optimizer_learning_rate: float
    :param crossed_feature_dimension: Crossed feature dimension for wide part model (min: 1)
    :type crossed_feature_dimension: int
    :param deep_part_optimizer: Optimizer used to apply gradients to the deep part of the model (enum: ['Adagrad', 'Adam', 'Ftrl', 'RMSProp', 'SGD', 'Adadelta'])
    :type deep_part_optimizer: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderDeepPartOptimizerEnum
    :param deep_optimizer_learning_rate: Size of each step in the learning process for deep part of the model (min: 2.220446049250313e-16, max: 2.0)
    :type deep_optimizer_learning_rate: float
    :param user_embedding_dimension: User embedding dimension for deep part model (min: 1)
    :type user_embedding_dimension: int
    :param item_embedding_dimension: Item embedding dimension for deep part model (min: 1)
    :type item_embedding_dimension: int
    :param categorical_features_embedding_dimension: Categorical features embedding dimension for deep part model (min: 1)
    :type categorical_features_embedding_dimension: int
    :param hidden_units: Hidden units per layer for deep part model
    :type hidden_units: str
    :param activation_function: Activation function applied to each layer in deep part model (enum: ['ReLU', 'Sigmoid', 'Tanh', 'Linear', 'LeakyReLU'])
    :type activation_function: _MicrosoftComAzuremlSamplesMpiTrainWideAndDeepRecommenderActivationFunctionEnum
    :param dropout: Probability that each element is dropped in deep part model (max: 1.0)
    :type dropout: float
    :param batch_normalization: Whether to use batch normalization after each hidden layer
    :type batch_normalization: bool
    :output trained_wide_and_deep_recommendation_model: Trained Wide and Deep recommendation model
    :type: trained_wide_and_deep_recommendation_model: Output
    """
    global _microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender
    if _microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender is None:
        _microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender/0.0.1/train_mpi.yaml")
    return _microsoft_com_azureml_samples_mpi_train_wide_and_deep_recommender(
            training_dataset_of_user_item_rating_triples=training_dataset_of_user_item_rating_triples,
            epochs=epochs,
            batch_size=batch_size,
            wide_part_optimizer=wide_part_optimizer,
            wide_optimizer_learning_rate=wide_optimizer_learning_rate,
            crossed_feature_dimension=crossed_feature_dimension,
            deep_part_optimizer=deep_part_optimizer,
            deep_optimizer_learning_rate=deep_optimizer_learning_rate,
            user_embedding_dimension=user_embedding_dimension,
            item_embedding_dimension=item_embedding_dimension,
            categorical_features_embedding_dimension=categorical_features_embedding_dimension,
            hidden_units=hidden_units,
            activation_function=activation_function,
            dropout=dropout,
            batch_normalization=batch_normalization,)


class _MicrosoftComAzuremlSamplesMetricdummymodulecliInput:
    pass


class _MicrosoftComAzuremlSamplesMetricdummymodulecliOutput:
    pass


class _MicrosoftComAzuremlSamplesMetricdummymodulecliComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesMetricdummymodulecliInput
    outputs: _MicrosoftComAzuremlSamplesMetricdummymodulecliOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_azureml_samples_metricdummymodulecli = None


def microsoft_com_azureml_samples_metricdummymodulecli(
) -> _MicrosoftComAzuremlSamplesMetricdummymodulecliComponent:
    """This module probes the logging and environment in python.
    
    """
    global _microsoft_com_azureml_samples_metricdummymodulecli
    if _microsoft_com_azureml_samples_metricdummymodulecli is None:
        _microsoft_com_azureml_samples_metricdummymodulecli = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_metricdummymodulecli/0.4/metrics_dummy_spec.yaml")
    return _microsoft_com_azureml_samples_metricdummymodulecli()


class _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum(Enum):
    rating_prediction = 'Rating Prediction'


class _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderInput:
    trained_wide_and_deep_recommendation_model: Input = None
    """Trained Wide and Deep recommendation model"""
    dataset_to_score: Input = None
    """Dataset to score"""
    recommender_prediction_kind: _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum = _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum.rating_prediction
    """Specify the type of prediction the recommendation should output (enum: ['Rating Prediction'])"""


class _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderOutput:
    scored_dataset: Output = None
    """Scored dataset"""


class _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderInput
    outputs: _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderOutput
    runsettings: _ParallelComponentRunsetting


_microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender = None


def microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender(
    trained_wide_and_deep_recommendation_model: Path = None,
    dataset_to_score: Path = None,
    recommender_prediction_kind: _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum = _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum.rating_prediction,
) -> _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderComponent:
    """Score a dataset using the Wide and Deep recommendation model.
    
    :param trained_wide_and_deep_recommendation_model: Trained Wide and Deep recommendation model
    :type trained_wide_and_deep_recommendation_model: Path
    :param dataset_to_score: Dataset to score
    :type dataset_to_score: Path
    :param recommender_prediction_kind: Specify the type of prediction the recommendation should output (enum: ['Rating Prediction'])
    :type recommender_prediction_kind: _MicrosoftComAzuremlSamplesParallelScoreWideAndDeepRecommenderRecommenderPredictionKindEnum
    :output scored_dataset: Scored dataset
    :type: scored_dataset: Output
    """
    global _microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender
    if _microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender is None:
        _microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender/0.0.1/score_parallel.yaml")
    return _microsoft_com_azureml_samples_parallel_score_wide_and_deep_recommender(
            trained_wide_and_deep_recommendation_model=trained_wide_and_deep_recommendation_model,
            dataset_to_score=dataset_to_score,
            recommender_prediction_kind=recommender_prediction_kind,)


class _MicrosoftComBingEjoinJointypeEnum(Enum):
    hashinner = 'HashInner'
    hashdiff = 'HashDiff'
    hashleft = 'HashLeft'
    sortinner = 'SortInner'
    sortleft = 'SortLeft'
    sortright = 'SortRight'
    sortouter = 'SortOuter'
    presortedinner = 'PresortedInner'
    presortedleft = 'PresortedLeft'
    presortedright = 'PreSortedRight'
    presortedouter = 'PresortedOuter'


class _MicrosoftComBingEjoinInput:
    leftinput: Input = None
    """['AnyFile', 'AnyDirectory']"""
    rightinput: Input = None
    """['AnyFile', 'AnyDirectory']"""
    leftcolumns: str = None
    """string"""
    rightcolumns: str = None
    """string"""
    leftkeys: str = None
    """string"""
    rightkeys: str = None
    """string"""
    jointype: _MicrosoftComBingEjoinJointypeEnum = None
    """enum (enum: ['HashInner', 'HashDiff', 'HashLeft', 'SortInner', 'SortLeft', 'SortRight', 'SortOuter', 'PresortedInner', 'PresortedLeft', 'PreSortedRight', 'PresortedOuter'])"""


class _MicrosoftComBingEjoinOutput:
    ejoin_output: Output = None
    """AnyFile"""


class _MicrosoftComBingEjoinComponent(Component):
    inputs: _MicrosoftComBingEjoinInput
    outputs: _MicrosoftComBingEjoinOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_bing_ejoin = None


def microsoft_com_bing_ejoin(
    leftinput: Path = None,
    rightinput: Path = None,
    leftcolumns: str = None,
    rightcolumns: str = None,
    leftkeys: str = None,
    rightkeys: str = None,
    jointype: _MicrosoftComBingEjoinJointypeEnum = None,
) -> _MicrosoftComBingEjoinComponent:
    """Combines two TSVs by performing a join on the key fields.
    
    :param leftinput: ['AnyFile', 'AnyDirectory']
    :type leftinput: Path
    :param rightinput: ['AnyFile', 'AnyDirectory']
    :type rightinput: Path
    :param leftcolumns: string
    :type leftcolumns: str
    :param rightcolumns: string
    :type rightcolumns: str
    :param leftkeys: string
    :type leftkeys: str
    :param rightkeys: string
    :type rightkeys: str
    :param jointype: enum (enum: ['HashInner', 'HashDiff', 'HashLeft', 'SortInner', 'SortLeft', 'SortRight', 'SortOuter', 'PresortedInner', 'PresortedLeft', 'PreSortedRight', 'PresortedOuter'])
    :type jointype: _MicrosoftComBingEjoinJointypeEnum
    :output ejoin_output: AnyFile
    :type: ejoin_output: Output
    """
    global _microsoft_com_bing_ejoin
    if _microsoft_com_bing_ejoin is None:
        _microsoft_com_bing_ejoin = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_bing_ejoin/0.0.5/https:/github.com/lisagreenview/hello-aml-modules/blob/master/ejoin/amlmodule.yaml")
    return _microsoft_com_bing_ejoin(
            leftinput=leftinput,
            rightinput=rightinput,
            leftcolumns=leftcolumns,
            rightcolumns=rightcolumns,
            leftkeys=leftkeys,
            rightkeys=rightkeys,
            jointype=jointype,)


class _MicrosoftComBingEselect2Input:
    input: Input = None
    """AnyDirectory"""
    columns: str = None
    """string"""


class _MicrosoftComBingEselect2Output:
    output: Output = None
    """AnyFile"""


class _MicrosoftComBingEselect2Component(Component):
    inputs: _MicrosoftComBingEselect2Input
    outputs: _MicrosoftComBingEselect2Output
    runsettings: _CommandComponentRunsetting


_microsoft_com_bing_eselect2 = None


def microsoft_com_bing_eselect2(
    input: Path = None,
    columns: str = None,
) -> _MicrosoftComBingEselect2Component:
    """Selects columns from input file based on the column description in the first line. Similar to cut (and grep), but column names can be used.
    
    :param input: AnyDirectory
    :type input: Path
    :param columns: string
    :type columns: str
    :output output: AnyFile
    :type: output: Output
    """
    global _microsoft_com_bing_eselect2
    if _microsoft_com_bing_eselect2 is None:
        _microsoft_com_bing_eselect2 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_bing_eselect2/0.0.2/amlmodule.yaml")
    return _microsoft_com_bing_eselect2(
            input=input,
            columns=columns,)


class _MicrosoftComCatMapInput:
    rating_true: Input = None
    """True DataFrame."""
    rating_pred: Input = None
    """Predicted DataFrame."""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    rating_column: str = 'Rating'
    """Column name of ratings."""
    prediction_column: str = 'prediction'
    """Column name of predictions."""
    relevancy_method: str = 'top_k'
    """method for determining relevancy ['top_k', 'by_threshold']."""
    top_k: int = 10
    """Number of top k items per user."""
    threshold: float = 10.0
    """Threshold of top items per user."""


class _MicrosoftComCatMapOutput:
    score: Output = None
    """MAP at k (min=0, max=1)."""


class _MicrosoftComCatMapComponent(Component):
    inputs: _MicrosoftComCatMapInput
    outputs: _MicrosoftComCatMapOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_map = None


def microsoft_com_cat_map(
    rating_true: Path = None,
    rating_pred: Path = None,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    rating_column: str = 'Rating',
    prediction_column: str = 'prediction',
    relevancy_method: str = 'top_k',
    top_k: int = 10,
    threshold: float = 10.0,
) -> _MicrosoftComCatMapComponent:
    """Mean Average Precision at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param rating_true: True DataFrame.
    :type rating_true: Path
    :param rating_pred: Predicted DataFrame.
    :type rating_pred: Path
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param rating_column: Column name of ratings.
    :type rating_column: str
    :param prediction_column: Column name of predictions.
    :type prediction_column: str
    :param relevancy_method: method for determining relevancy ['top_k', 'by_threshold'].
    :type relevancy_method: str
    :param top_k: Number of top k items per user.
    :type top_k: int
    :param threshold: Threshold of top items per user.
    :type threshold: float
    :output score: MAP at k (min=0, max=1).
    :type: score: Output
    """
    global _microsoft_com_cat_map
    if _microsoft_com_cat_map is None:
        _microsoft_com_cat_map = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_map/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/map.yaml")
    return _microsoft_com_cat_map(
            rating_true=rating_true,
            rating_pred=rating_pred,
            user_column=user_column,
            item_column=item_column,
            rating_column=rating_column,
            prediction_column=prediction_column,
            relevancy_method=relevancy_method,
            top_k=top_k,
            threshold=threshold,)


class _MicrosoftComCatPrecisionAtKInput:
    rating_true: Input = None
    """True DataFrame."""
    rating_pred: Input = None
    """Predicted DataFrame."""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    rating_column: str = 'Rating'
    """Column name of ratings."""
    prediction_column: str = 'prediction'
    """Column name of predictions."""
    relevancy_method: str = 'top_k'
    """method for determining relevancy ['top_k', 'by_threshold']."""
    top_k: int = 10
    """Number of top k items per user."""
    threshold: float = 10.0
    """Threshold of top items per user."""


class _MicrosoftComCatPrecisionAtKOutput:
    score: Output = None
    """Precision at k (min=0, max=1)."""


class _MicrosoftComCatPrecisionAtKComponent(Component):
    inputs: _MicrosoftComCatPrecisionAtKInput
    outputs: _MicrosoftComCatPrecisionAtKOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_precision_at_k = None


def microsoft_com_cat_precision_at_k(
    rating_true: Path = None,
    rating_pred: Path = None,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    rating_column: str = 'Rating',
    prediction_column: str = 'prediction',
    relevancy_method: str = 'top_k',
    top_k: int = 10,
    threshold: float = 10.0,
) -> _MicrosoftComCatPrecisionAtKComponent:
    """Precision at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param rating_true: True DataFrame.
    :type rating_true: Path
    :param rating_pred: Predicted DataFrame.
    :type rating_pred: Path
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param rating_column: Column name of ratings.
    :type rating_column: str
    :param prediction_column: Column name of predictions.
    :type prediction_column: str
    :param relevancy_method: method for determining relevancy ['top_k', 'by_threshold'].
    :type relevancy_method: str
    :param top_k: Number of top k items per user.
    :type top_k: int
    :param threshold: Threshold of top items per user.
    :type threshold: float
    :output score: Precision at k (min=0, max=1).
    :type: score: Output
    """
    global _microsoft_com_cat_precision_at_k
    if _microsoft_com_cat_precision_at_k is None:
        _microsoft_com_cat_precision_at_k = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_precision_at_k/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/precision_at_k.yaml")
    return _microsoft_com_cat_precision_at_k(
            rating_true=rating_true,
            rating_pred=rating_pred,
            user_column=user_column,
            item_column=item_column,
            rating_column=rating_column,
            prediction_column=prediction_column,
            relevancy_method=relevancy_method,
            top_k=top_k,
            threshold=threshold,)


class _MicrosoftComCatRecallAtKInput:
    rating_true: Input = None
    """True DataFrame."""
    rating_pred: Input = None
    """Predicted DataFrame."""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    rating_column: str = 'Rating'
    """Column name of ratings."""
    prediction_column: str = 'prediction'
    """Column name of predictions."""
    relevancy_method: str = 'top_k'
    """method for determining relevancy ['top_k', 'by_threshold']."""
    top_k: int = 10
    """Number of top k items per user."""
    threshold: float = 10.0
    """Threshold of top items per user."""


class _MicrosoftComCatRecallAtKOutput:
    score: Output = None
    """Recall at k (min=0, max=1)."""


class _MicrosoftComCatRecallAtKComponent(Component):
    inputs: _MicrosoftComCatRecallAtKInput
    outputs: _MicrosoftComCatRecallAtKOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_recall_at_k = None


def microsoft_com_cat_recall_at_k(
    rating_true: Path = None,
    rating_pred: Path = None,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    rating_column: str = 'Rating',
    prediction_column: str = 'prediction',
    relevancy_method: str = 'top_k',
    top_k: int = 10,
    threshold: float = 10.0,
) -> _MicrosoftComCatRecallAtKComponent:
    """Recall at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param rating_true: True DataFrame.
    :type rating_true: Path
    :param rating_pred: Predicted DataFrame.
    :type rating_pred: Path
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param rating_column: Column name of ratings.
    :type rating_column: str
    :param prediction_column: Column name of predictions.
    :type prediction_column: str
    :param relevancy_method: method for determining relevancy ['top_k', 'by_threshold'].
    :type relevancy_method: str
    :param top_k: Number of top k items per user.
    :type top_k: int
    :param threshold: Threshold of top items per user.
    :type threshold: float
    :output score: Recall at k (min=0, max=1).
    :type: score: Output
    """
    global _microsoft_com_cat_recall_at_k
    if _microsoft_com_cat_recall_at_k is None:
        _microsoft_com_cat_recall_at_k = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_recall_at_k/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/recall_at_k.yaml")
    return _microsoft_com_cat_recall_at_k(
            rating_true=rating_true,
            rating_pred=rating_pred,
            user_column=user_column,
            item_column=item_column,
            rating_column=rating_column,
            prediction_column=prediction_column,
            relevancy_method=relevancy_method,
            top_k=top_k,
            threshold=threshold,)


class _MicrosoftComCatSarScoringScoreTypeEnum(Enum):
    rating_prediction = 'Rating prediction'
    item_recommendation = 'Item recommendation'


class _MicrosoftComCatSarScoringItemsToPredictEnum(Enum):
    items_in_training_set = 'Items in training set'
    items_in_score_set = 'Items in score set'


class _MicrosoftComCatSarScoringRankingMetricEnum(Enum):
    rating = 'Rating'
    similarity = 'Similarity'
    popularity = 'Popularity'


class _MicrosoftComCatSarScoringInput:
    trained_model: Input = None
    """The directory contains SAR model."""
    dataset_to_score: Input = None
    """Dataset to score"""
    score_type: _MicrosoftComCatSarScoringScoreTypeEnum = _MicrosoftComCatSarScoringScoreTypeEnum.item_recommendation
    """The type of score which the recommender should output (enum: ['Rating prediction', 'Item recommendation'])"""
    items_to_predict: _MicrosoftComCatSarScoringItemsToPredictEnum = _MicrosoftComCatSarScoringItemsToPredictEnum.items_in_score_set
    """The set of items to predict for test users (optional, enum: ['Items in training set', 'Items in score set'])"""
    ranking_metric: _MicrosoftComCatSarScoringRankingMetricEnum = _MicrosoftComCatSarScoringRankingMetricEnum.rating
    """The metric of ranking used in item recommendation (optional, enum: ['Rating', 'Similarity', 'Popularity'])"""
    remove_seen_items: bool = False
    """Flag to remove items seen in training from recommendation (optional)"""
    top_k: int = 10
    """The number of top items to recommend. (optional, min: 1)"""
    sort_top_k: bool = True
    """Flag to sort top k results. (optional)"""
    normalize: bool = False
    """Flag to normalize predictions to scale of original ratings"""


class _MicrosoftComCatSarScoringOutput:
    score_result: Output = None
    """Ratings or items to output"""


class _MicrosoftComCatSarScoringComponent(Component):
    inputs: _MicrosoftComCatSarScoringInput
    outputs: _MicrosoftComCatSarScoringOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_sar_scoring = None


def microsoft_com_cat_sar_scoring(
    trained_model: Path = None,
    dataset_to_score: Path = None,
    score_type: _MicrosoftComCatSarScoringScoreTypeEnum = _MicrosoftComCatSarScoringScoreTypeEnum.item_recommendation,
    items_to_predict: _MicrosoftComCatSarScoringItemsToPredictEnum = _MicrosoftComCatSarScoringItemsToPredictEnum.items_in_score_set,
    ranking_metric: _MicrosoftComCatSarScoringRankingMetricEnum = _MicrosoftComCatSarScoringRankingMetricEnum.rating,
    remove_seen_items: bool = False,
    top_k: int = 10,
    sort_top_k: bool = True,
    normalize: bool = False,
) -> _MicrosoftComCatSarScoringComponent:
    """Python SAR Recommenders
repo: https://github.com/Microsoft/Recommenders

    
    :param trained_model: The directory contains SAR model.
    :type trained_model: Path
    :param dataset_to_score: Dataset to score
    :type dataset_to_score: Path
    :param score_type: The type of score which the recommender should output (enum: ['Rating prediction', 'Item recommendation'])
    :type score_type: _MicrosoftComCatSarScoringScoreTypeEnum
    :param items_to_predict: The set of items to predict for test users (optional, enum: ['Items in training set', 'Items in score set'])
    :type items_to_predict: _MicrosoftComCatSarScoringItemsToPredictEnum
    :param ranking_metric: The metric of ranking used in item recommendation (optional, enum: ['Rating', 'Similarity', 'Popularity'])
    :type ranking_metric: _MicrosoftComCatSarScoringRankingMetricEnum
    :param remove_seen_items: Flag to remove items seen in training from recommendation (optional)
    :type remove_seen_items: bool
    :param top_k: The number of top items to recommend. (optional, min: 1)
    :type top_k: int
    :param sort_top_k: Flag to sort top k results. (optional)
    :type sort_top_k: bool
    :param normalize: Flag to normalize predictions to scale of original ratings
    :type normalize: bool
    :output score_result: Ratings or items to output
    :type: score_result: Output
    """
    global _microsoft_com_cat_sar_scoring
    if _microsoft_com_cat_sar_scoring is None:
        _microsoft_com_cat_sar_scoring = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_sar_scoring/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/sar_score.yaml")
    return _microsoft_com_cat_sar_scoring(
            trained_model=trained_model,
            dataset_to_score=dataset_to_score,
            score_type=score_type,
            items_to_predict=items_to_predict,
            ranking_metric=ranking_metric,
            remove_seen_items=remove_seen_items,
            top_k=top_k,
            sort_top_k=sort_top_k,
            normalize=normalize,)


class _MicrosoftComCatSarTrainingInput:
    input_path: Input = None
    """The directory contains dataframe."""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    rating_column: str = 'Rating'
    """Column name of rating."""
    timestamp_column: str = 'Timestamp'
    """Column name of timestamp."""
    normalize: bool = False
    """Flag to normalize predictions to scale of original ratings"""
    time_decay: bool = False
    """Flag to apply time decay"""


class _MicrosoftComCatSarTrainingOutput:
    output_model: Output = None
    """The output directory contains a trained model"""


class _MicrosoftComCatSarTrainingComponent(Component):
    inputs: _MicrosoftComCatSarTrainingInput
    outputs: _MicrosoftComCatSarTrainingOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_sar_training = None


def microsoft_com_cat_sar_training(
    input_path: Path = None,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    rating_column: str = 'Rating',
    timestamp_column: str = 'Timestamp',
    normalize: bool = False,
    time_decay: bool = False,
) -> _MicrosoftComCatSarTrainingComponent:
    """SAR Train from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param rating_column: Column name of rating.
    :type rating_column: str
    :param timestamp_column: Column name of timestamp.
    :type timestamp_column: str
    :param normalize: Flag to normalize predictions to scale of original ratings
    :type normalize: bool
    :param time_decay: Flag to apply time decay
    :type time_decay: bool
    :output output_model: The output directory contains a trained model
    :type: output_model: Output
    """
    global _microsoft_com_cat_sar_training
    if _microsoft_com_cat_sar_training is None:
        _microsoft_com_cat_sar_training = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_sar_training/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/sar_train.yaml")
    return _microsoft_com_cat_sar_training(
            input_path=input_path,
            user_column=user_column,
            item_column=item_column,
            rating_column=rating_column,
            timestamp_column=timestamp_column,
            normalize=normalize,
            time_decay=time_decay,)


class _MicrosoftComCatStratifiedSplitterInput:
    input_path: Input = None
    """The directory contains dataframe."""
    ratio: float = 0.75
    """Ratio for splitting data. If it is a single float number, it splits data into two halves and the ratio argument indicates the ratio of  training data set; if it is a list of float numbers, the splitter splits  data into several portions corresponding to the split ratios. If a list is  provided and the ratios are not summed to 1, they will be normalized.
 (max: 1.0)"""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    seed: int = 42
    """Seed."""


class _MicrosoftComCatStratifiedSplitterOutput:
    output_train_data: Output = None
    """The output directory contains a training dataframe."""
    output_test_data: Output = None
    """The output directory contains a test dataframe."""


class _MicrosoftComCatStratifiedSplitterComponent(Component):
    inputs: _MicrosoftComCatStratifiedSplitterInput
    outputs: _MicrosoftComCatStratifiedSplitterOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_stratified_splitter = None


def microsoft_com_cat_stratified_splitter(
    input_path: Path = None,
    ratio: float = 0.75,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    seed: int = 42,
) -> _MicrosoftComCatStratifiedSplitterComponent:
    """Python stratified splitter from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param ratio: Ratio for splitting data. If it is a single float number, it splits data into two halves and the ratio argument indicates the ratio of  training data set; if it is a list of float numbers, the splitter splits  data into several portions corresponding to the split ratios. If a list is  provided and the ratios are not summed to 1, they will be normalized.
 (max: 1.0)
    :type ratio: float
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param seed: Seed.
    :type seed: int
    :output output_train_data: The output directory contains a training dataframe.
    :type: output_train_data: Output
    :output output_test_data: The output directory contains a test dataframe.
    :type: output_test_data: Output
    """
    global _microsoft_com_cat_stratified_splitter
    if _microsoft_com_cat_stratified_splitter is None:
        _microsoft_com_cat_stratified_splitter = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_stratified_splitter/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/stratified_splitter.yaml")
    return _microsoft_com_cat_stratified_splitter(
            input_path=input_path,
            ratio=ratio,
            user_column=user_column,
            item_column=item_column,
            seed=seed,)


class _MicrosoftComCatNdcgInput:
    rating_true: Input = None
    """True DataFrame."""
    rating_pred: Input = None
    """Predicted DataFrame."""
    user_column: str = 'UserId'
    """Column name of user IDs."""
    item_column: str = 'MovieId'
    """Column name of item IDs."""
    rating_column: str = 'Rating'
    """Column name of ratings."""
    prediction_column: str = 'prediction'
    """Column name of predictions."""
    relevancy_method: str = 'top_k'
    """method for determining relevancy ['top_k', 'by_threshold']."""
    top_k: int = 10
    """Number of top k items per user."""
    threshold: float = 10.0
    """Threshold of top items per user."""


class _MicrosoftComCatNdcgOutput:
    score: Output = None
    """nDCG at k (min=0, max=1)."""


class _MicrosoftComCatNdcgComponent(Component):
    inputs: _MicrosoftComCatNdcgInput
    outputs: _MicrosoftComCatNdcgOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_cat_ndcg = None


def microsoft_com_cat_ndcg(
    rating_true: Path = None,
    rating_pred: Path = None,
    user_column: str = 'UserId',
    item_column: str = 'MovieId',
    rating_column: str = 'Rating',
    prediction_column: str = 'prediction',
    relevancy_method: str = 'top_k',
    top_k: int = 10,
    threshold: float = 10.0,
) -> _MicrosoftComCatNdcgComponent:
    """Normalized Discounted Cumulative Gain (nDCG) at K metric from Recommenders repo: https://github.com/Microsoft/Recommenders.
    
    :param rating_true: True DataFrame.
    :type rating_true: Path
    :param rating_pred: Predicted DataFrame.
    :type rating_pred: Path
    :param user_column: Column name of user IDs.
    :type user_column: str
    :param item_column: Column name of item IDs.
    :type item_column: str
    :param rating_column: Column name of ratings.
    :type rating_column: str
    :param prediction_column: Column name of predictions.
    :type prediction_column: str
    :param relevancy_method: method for determining relevancy ['top_k', 'by_threshold'].
    :type relevancy_method: str
    :param top_k: Number of top k items per user.
    :type top_k: int
    :param threshold: Threshold of top items per user.
    :type threshold: float
    :output score: nDCG at k (min=0, max=1).
    :type: score: Output
    """
    global _microsoft_com_cat_ndcg
    if _microsoft_com_cat_ndcg is None:
        _microsoft_com_cat_ndcg = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_cat_ndcg/1.1.1/https:/github.com/microsoft/recommenders/blob/master/reco_utils/azureml/azureml_designer_modules/module_specs/ndcg.yaml")
    return _microsoft_com_cat_ndcg(
            rating_true=rating_true,
            rating_pred=rating_pred,
            user_column=user_column,
            item_column=item_column,
            rating_column=rating_column,
            prediction_column=prediction_column,
            relevancy_method=relevancy_method,
            top_k=top_k,
            threshold=threshold,)


class _MicrosoftComOfficeMpiModuleParameter2Enum(Enum):
    red = 'Red'
    green = 'Green'
    blue = 'Blue'


class _MicrosoftComOfficeMpiModuleInput:
    input_port: Input = None
    """['AnyFile', 'AnyDirectory']"""
    parameter_1: str = 'hello'
    """Input a greeting message."""
    parameter_2: _MicrosoftComOfficeMpiModuleParameter2Enum = _MicrosoftComOfficeMpiModuleParameter2Enum.red
    """Choose your favorite color. (enum: ['Red', 'Green', 'Blue'])"""
    parameter_3: int = 1
    """The Integer parameter which has a range validation. (max: 10)"""


class _MicrosoftComOfficeMpiModuleOutput:
    output_port: Output = None
    """AnyDirectory"""


class _MicrosoftComOfficeMpiModuleComponent(Component):
    inputs: _MicrosoftComOfficeMpiModuleInput
    outputs: _MicrosoftComOfficeMpiModuleOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_office_mpi_module = None


def microsoft_com_office_mpi_module(
    input_port: Path = None,
    parameter_1: str = 'hello',
    parameter_2: _MicrosoftComOfficeMpiModuleParameter2Enum = _MicrosoftComOfficeMpiModuleParameter2Enum.red,
    parameter_3: int = 1,
) -> _MicrosoftComOfficeMpiModuleComponent:
    """Mpi module for demo.
    
    :param input_port: ['AnyFile', 'AnyDirectory']
    :type input_port: Path
    :param parameter_1: Input a greeting message.
    :type parameter_1: str
    :param parameter_2: Choose your favorite color. (enum: ['Red', 'Green', 'Blue'])
    :type parameter_2: _MicrosoftComOfficeMpiModuleParameter2Enum
    :param parameter_3: The Integer parameter which has a range validation. (max: 10)
    :type parameter_3: int
    :output output_port: AnyDirectory
    :type: output_port: Output
    """
    global _microsoft_com_office_mpi_module
    if _microsoft_com_office_mpi_module is None:
        _microsoft_com_office_mpi_module = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_office_mpi_module/0.0.1/https:/github.com/zzn2/sample_modules/blob/master/4_mpi_module/mpi_module.yaml")
    return _microsoft_com_office_mpi_module(
            input_port=input_port,
            parameter_1=parameter_1,
            parameter_2=parameter_2,
            parameter_3=parameter_3,)


class _MicrosoftComOfficeSampleModuleInput:
    input_port: Input = None
    """AnyDirectory"""
    parameter_1: str = 'hello'
    """string"""
    parameter_2: int = 1
    """integer"""


class _MicrosoftComOfficeSampleModuleOutput:
    output_port: Output = None
    """AnyDirectory"""


class _MicrosoftComOfficeSampleModuleComponent(Component):
    inputs: _MicrosoftComOfficeSampleModuleInput
    outputs: _MicrosoftComOfficeSampleModuleOutput
    runsettings: _CommandComponentRunsetting


_microsoft_com_office_sample_module = None


def microsoft_com_office_sample_module(
    input_port: Path = None,
    parameter_1: str = 'hello',
    parameter_2: int = 1,
) -> _MicrosoftComOfficeSampleModuleComponent:
    """Basic module for demo.
    
    :param input_port: AnyDirectory
    :type input_port: Path
    :param parameter_1: string
    :type parameter_1: str
    :param parameter_2: integer
    :type parameter_2: int
    :output output_port: AnyDirectory
    :type: output_port: Output
    """
    global _microsoft_com_office_sample_module
    if _microsoft_com_office_sample_module is None:
        _microsoft_com_office_sample_module = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_office_sample_module/0.1.0/module_spec.yaml")
    return _microsoft_com_office_sample_module(
            input_port=input_port,
            parameter_1=parameter_1,
            parameter_2=parameter_2,)


class _ScopemultijoinInput:
    a: Input = None
    """path"""
    b: Input = None
    """path"""
    c: Input = None
    """path"""
    select1: str = 'SELECT *'
    """string (optional)"""
    select2: str = 'SELECT *'
    """string (optional)"""
    select3: str = 'SELECT *'
    """string (optional)"""
    select4: str = 'SELECT *'
    """string (optional)"""
    select5: str = 'SELECT *'
    """string (optional)"""
    select6: str = 'SELECT *'
    """string (optional)"""
    select7: str = 'SELECT *'
    """string (optional)"""
    select8: str = 'SELECT *'
    """string (optional)"""
    select9: str = 'SELECT *'
    """string (optional)"""
    select10: str = 'SELECT *'
    """string (optional)"""
    clustered: str = 'foo'
    """string (optional)"""
    sorted: str = 'bar'
    """string (optional)"""
    code: str = '//  Add code'
    """string (optional)"""
    vc: str = 'cosmos09/relevance'
    """string (optional)"""


class _ScopemultijoinOutput:
    output: Output = None
    """path"""


class _ScopemultijoinComponent(Component):
    inputs: _ScopemultijoinInput
    outputs: _ScopemultijoinOutput
    runsettings: _CommandComponentRunsetting


_scopemultijoin = None


def scopemultijoin(
    a: Path = None,
    b: Path = None,
    c: Path = None,
    select1: str = 'SELECT *',
    select2: str = 'SELECT *',
    select3: str = 'SELECT *',
    select4: str = 'SELECT *',
    select5: str = 'SELECT *',
    select6: str = 'SELECT *',
    select7: str = 'SELECT *',
    select8: str = 'SELECT *',
    select9: str = 'SELECT *',
    select10: str = 'SELECT *',
    clustered: str = 'foo',
    sorted: str = 'bar',
    code: str = '//  Add code',
    vc: str = 'cosmos09/relevance',
) -> _ScopemultijoinComponent:
    """scopemultijoin
    
    :param a: path
    :type a: Path
    :param b: path
    :type b: Path
    :param c: path
    :type c: Path
    :param select1: string (optional)
    :type select1: str
    :param select2: string (optional)
    :type select2: str
    :param select3: string (optional)
    :type select3: str
    :param select4: string (optional)
    :type select4: str
    :param select5: string (optional)
    :type select5: str
    :param select6: string (optional)
    :type select6: str
    :param select7: string (optional)
    :type select7: str
    :param select8: string (optional)
    :type select8: str
    :param select9: string (optional)
    :type select9: str
    :param select10: string (optional)
    :type select10: str
    :param clustered: string (optional)
    :type clustered: str
    :param sorted: string (optional)
    :type sorted: str
    :param code: string (optional)
    :type code: str
    :param vc: string (optional)
    :type vc: str
    :output output: path
    :type: output: Output
    """
    global _scopemultijoin
    if _scopemultijoin is None:
        _scopemultijoin = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/scopemultijoin/0.0.2/entry.spec.yaml")
    return _scopemultijoin(
            a=a,
            b=b,
            c=c,
            select1=select1,
            select2=select2,
            select3=select3,
            select4=select4,
            select5=select5,
            select6=select6,
            select7=select7,
            select8=select8,
            select9=select9,
            select10=select10,
            clustered=clustered,
            sorted=sorted,
            code=code,
            vc=vc,)


class _TrainInput:
    input: Input = None
    """['AnyFile', 'AnyDirectory']"""
    modulename: str = 'train'
    """string"""
    sourcezipfilename: str = 'mysteps.zip'
    """string"""


class _TrainOutput:
    output: Output = None
    """AnyFile"""


class _TrainComponent(Component):
    inputs: _TrainInput
    outputs: _TrainOutput
    runsettings: _CommandComponentRunsetting


_train = None


def train(
    input: Path = None,
    modulename: str = 'train',
    sourcezipfilename: str = 'mysteps.zip',
) -> _TrainComponent:
    """train
    
    :param input: ['AnyFile', 'AnyDirectory']
    :type input: Path
    :param modulename: string
    :type modulename: str
    :param sourcezipfilename: string
    :type sourcezipfilename: str
    :output output: AnyFile
    :type: output: Output
    """
    global _train
    if _train is None:
        _train = Component.load(
            _workspace.lisal_amlservice(),
            name='train', version='0.1.0')
    return _train(
            input=input,
            modulename=modulename,
            sourcezipfilename=sourcezipfilename,)


class _XslapperInput:
    start: str = '"2019-05-01"'
    """string (optional)"""
    end: str = '"2019-05-01"'
    """string (optional)"""
    dataset: str = '"Bing.com"'
    """string (optional)"""
    traffic: str = '"Normal"'
    """string (optional)"""
    select1: str = 'SELECT ClientId'
    """string (optional)"""
    select2: str = 'SELECT *'
    """string (optional)"""
    select3: str = 'SELECT *'
    """string (optional)"""
    select4: str = 'SELECT *'
    """string (optional)"""
    select5: str = 'SELECT *'
    """string (optional)"""
    select6: str = 'SELECT *'
    """string (optional)"""
    select7: str = 'SELECT *'
    """string (optional)"""
    select8: str = 'SELECT *'
    """string (optional)"""
    select9: str = 'SELECT *'
    """string (optional)"""
    select10: str = 'SELECT *'
    """string (optional)"""
    clustered: str = 'ClientId'
    """string (optional)"""
    sorted: str = 'ClientId'
    """string (optional)"""
    vc: str = 'cosmos09/relevance'
    """string (optional)"""
    scopeparams: str = None
    """string (optional)"""


class _XslapperOutput:
    output: Output = None
    """path"""


class _XslapperComponent(Component):
    inputs: _XslapperInput
    outputs: _XslapperOutput
    runsettings: _CommandComponentRunsetting


_xslapper = None


def xslapper(
    start: str = '"2019-05-01"',
    end: str = '"2019-05-01"',
    dataset: str = '"Bing.com"',
    traffic: str = '"Normal"',
    select1: str = 'SELECT ClientId',
    select2: str = 'SELECT *',
    select3: str = 'SELECT *',
    select4: str = 'SELECT *',
    select5: str = 'SELECT *',
    select6: str = 'SELECT *',
    select7: str = 'SELECT *',
    select8: str = 'SELECT *',
    select9: str = 'SELECT *',
    select10: str = 'SELECT *',
    clustered: str = 'ClientId',
    sorted: str = 'ClientId',
    vc: str = 'cosmos09/relevance',
    scopeparams: str = None,
) -> _XslapperComponent:
    """xslapper
    
    :param start: string (optional)
    :type start: str
    :param end: string (optional)
    :type end: str
    :param dataset: string (optional)
    :type dataset: str
    :param traffic: string (optional)
    :type traffic: str
    :param select1: string (optional)
    :type select1: str
    :param select2: string (optional)
    :type select2: str
    :param select3: string (optional)
    :type select3: str
    :param select4: string (optional)
    :type select4: str
    :param select5: string (optional)
    :type select5: str
    :param select6: string (optional)
    :type select6: str
    :param select7: string (optional)
    :type select7: str
    :param select8: string (optional)
    :type select8: str
    :param select9: string (optional)
    :type select9: str
    :param select10: string (optional)
    :type select10: str
    :param clustered: string (optional)
    :type clustered: str
    :param sorted: string (optional)
    :type sorted: str
    :param vc: string (optional)
    :type vc: str
    :param scopeparams: string (optional)
    :type scopeparams: str
    :output output: path
    :type: output: Output
    """
    global _xslapper
    if _xslapper is None:
        _xslapper = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/xslapper/0.0.1/entry.spec.yaml")
    return _xslapper(
            start=start,
            end=end,
            dataset=dataset,
            traffic=traffic,
            select1=select1,
            select2=select2,
            select3=select3,
            select4=select4,
            select5=select5,
            select6=select6,
            select7=select7,
            select8=select8,
            select9=select9,
            select10=select10,
            clustered=clustered,
            sorted=sorted,
            vc=vc,
            scopeparams=scopeparams,)


# +===================================================+
#                    datasets
# +===================================================+


class Datasets:

    @property
    @lru_cache(maxsize=1)
    def notebook_component_output_as_dataset(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='notebook_component_output_as_dataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def ss_labeldata(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SS_LabelData', version='1')

    @property
    @lru_cache(maxsize=1)
    def labeldata(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='LabelData', version='1')

    @property
    @lru_cache(maxsize=1)
    def result_dataset(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Result dataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def awk_generate_classifier_from_tlc_ml_net(self):
        """[AWK] Generate Classifier from TLC / ML.Net"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='[AWK] Generate Classifier from TLC / ML.Net', version='1')

    @property
    @lru_cache(maxsize=1)
    def sr_2x4_binary_classification_l_clicked_next_day(self):
        """SR_2x4 Binary Classification (L=clicked next day)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SR_2x4 Binary Classification (L=clicked next day)', version='1')

    @property
    @lru_cache(maxsize=1)
    def sr_2x4_binary_classification_original(self):
        """SR_2x4 Binary Classification (original)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SR_2x4 Binary Classification (original)', version='1')

    @property
    @lru_cache(maxsize=1)
    def sr_2x4_ranking_training_with_g_and_b_sampling(self):
        """SR_2x4 Ranking Training (with G and B sampling)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SR_2x4 Ranking Training (with G and B sampling)', version='1')

    @property
    @lru_cache(maxsize=1)
    def sr_2x4_ranking_training_big(self):
        """SR 2x4 Ranking Training (big)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SR 2x4 Ranking Training (big)', version='1')

    @property
    @lru_cache(maxsize=1)
    def sr_2x4_ranking_training_small(self):
        """SR_2x4 Ranking Training (small)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='SR_2x4 Ranking Training (small)', version='1')

    @property
    @lru_cache(maxsize=1)
    def aml_component_test_data(self):
        """Test data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='aml_component_test_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def aml_component_training_data(self):
        """Training data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='aml_component_training_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def test_data(self):
        """Test data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='test_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def training_data(self):
        """Training data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='training_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def imdb_dataset_samples(self):
        """Training data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='IMDB_Dataset_Samples', version='1')

    @property
    @lru_cache(maxsize=1)
    def automobile_price_data(self):
        """Automobile_price_data"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Automobile_price_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def automobile_price_data_raw(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Automobile_price_data_(Raw)', version='1')

    @property
    @lru_cache(maxsize=1)
    def titanic(self):
        """Training data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Titanic', version='1')

    @property
    @lru_cache(maxsize=1)
    def movie_ratings(self):
        """movie rating data"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Movie_Ratings', version='1')

    @property
    @lru_cache(maxsize=1)
    def movie_rating_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Movie-rating-data', version='1')

    @property
    @lru_cache(maxsize=1)
    def company(self):
        """profile of technique company"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Company', version='1')

    @property
    @lru_cache(maxsize=1)
    def my_automobile_price_data(self):
        """Automobile_price_data (convert to ws dataset)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='My_Automobile_price_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def aml_module_test_data(self):
        """Test data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='aml_module_test_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def aml_module_training_data(self):
        """Training data (just for illustrative purpose)"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='aml_module_training_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def iris_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='iris_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def mnist_sample_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='mnist_sample_data', version='1')

    @property
    @lru_cache(maxsize=1)
    def testcsvconvert(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='TestCsvConvert', version='1')

    @property
    @lru_cache(maxsize=1)
    def mnist_opendataset(self):
        """training and test dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='mnist_opendataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def compareresults_wcus3_95percentile(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CompareResults_WCUS3_95Percentile', version='1')

    @property
    @lru_cache(maxsize=1)
    def intel_image_2019_11_29_09_30_20(self):
        """LabeledDs_Intel Image Of Type ImageClassificationMultiClass, Sourced From 9507e333-6171-470a-a6c6-9074789e4409"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Intel Image-2019-11-29 09:30:20', version='1')

    @property
    @lru_cache(maxsize=1)
    def partialintelimage(self):
        """Partial Intel Image"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='PartialIntelImage', version='1')

    @property
    @lru_cache(maxsize=1)
    def dog_and_cat_2019_11_29_09_16_16(self):
        """LabeledDs_Dog and Cat Of Type ImageClassificationMultiClass, Sourced From 014c2a91-a7b7-45fd-8488-ed56021c99cb"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Dog and Cat-2019-11-29 09:16:16', version='1')

    @property
    @lru_cache(maxsize=1)
    def dog_and_cat(self):
        """Dog and Cat"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Dog and Cat', version='1')

    @property
    @lru_cache(maxsize=1)
    def intelimage(self):
        """Intel Image"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='IntelImage', version='1')

    @property
    @lru_cache(maxsize=1)
    def md_sample_3_classification_credit_risk_prediction_basic_train_model_trained_model_4a279ede(self):
        """This is a dataset promoted by inference graph generation automatically on 11/7/2019 4:14:04 AM. 
 Training pipeline draft:Sample 3 - Classification: Credit Risk Prediction(Basic)  
Training pipeline draftId:15fa65c7-edf0-4bcf-8b0d-e994cb7c6cc5 
Module Name:Train Model 
ModuleId:b98d4405-aee8-5703-af5e-45e9b6597305 
Port:Trained_model"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='MD-Sample_3_-_Classification:_Credit_Risk_Prediction(Basic)_-Train_Model-Trained_model-4a279ede', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_appetency_labels_shared_copy(self):
        """CRM Appetency Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Appetency Labels Shared - Copy', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_dataset_shared_copy(self):
        """CRM Dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Dataset Shared - Copy', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_upselling_labels_shared_copy(self):
        """CRM Upselling Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Upselling Labels Shared - Copy', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_churn_labels_shared_copy(self):
        """CRM Churn Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Churn Labels Shared - Copy', version='1')

    @property
    @lru_cache(maxsize=1)
    def bill_gates_rgb_image(self):
        """Bill Gates RGB Image"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Bill Gates RGB Image', version='1')

    @property
    @lru_cache(maxsize=1)
    def adult_census_income_binary_classification_dataset(self):
        """Census Income dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Adult Census Income Binary Classification dataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def v2_sample_regression_predict_automobile_price_basic_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='V2 Sample - Regression Predict Automobile Price (Basic) [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def v2_sample_regression_predict_automobile_price_basic_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='V2 Sample - Regression Predict Automobile Price (Basic) [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def bing_bot_detection_4gb_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Bing bot detection - 4GB [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def trained_model_logistic_regression(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Trained model (Logistic Regression)', version='1')

    @property
    @lru_cache(maxsize=1)
    def bot_detection_small_data_multiple_models_2_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='bot detection small data multiple models 2 [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def bot_detection_small_data_multiple_models_2_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='bot detection small data multiple models 2 [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def top_10_botdetectiondata(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Top 10 BotDetectionData', version='1')

    @property
    @lru_cache(maxsize=1)
    def cleaning_transformation_6m(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Cleaning transformation (6M)', version='1')

    @property
    @lru_cache(maxsize=1)
    def bot_detection_small_data_multiple_models_2_normalize_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='bot detection small data multiple models 2 [Normalize Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def trained_model_boosted_decision_tree(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Trained model (Boosted Decision Tree)', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_appetency_labels_shared(self):
        """CRM Appetency Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Appetency Labels Shared', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_upselling_labels_shared(self):
        """CRM Upselling Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Upselling Labels Shared', version='3')

    @property
    @lru_cache(maxsize=1)
    def sample_5_classification_customer_relationship_prediction_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 5 - Classification Customer Relationship Prediction [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_dataset_shared(self):
        """CRM Dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Dataset Shared', version='3')

    @property
    @lru_cache(maxsize=1)
    def botdetection_small_data_0415_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BotDetection - small data - 0415 [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def load_images_zip(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='load_images.zip', version='1')

    @property
    @lru_cache(maxsize=1)
    def sample_3_classification_credit_risk_prediction_basic_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 3 - Classification Credit Risk Prediction(Basic) [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def crm_churn_labels_shared(self):
        """CRM Churn Labels"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='CRM Churn Labels Shared', version='3')

    @property
    @lru_cache(maxsize=1)
    def airport_codes_dataset(self):
        """Airport Codes Dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Airport Codes Dataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def sample_5_classification_customer_relationship_prediction_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 5 - Classification Customer Relationship Prediction [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def botdetection_small_data_0417_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BotDetection - small data - 0417 [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def botdetection_small_data_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BotDetection - small data [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def buildtest_sample_2_regression_automobile_price_prediction_compare_algorithms_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BuildTest-Sample 2 - Regression Automobile Price Prediction (Compare Algorithms) [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def german_credit_card_uci_dataset(self):
        """German Credit Card UCI dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='German Credit Card UCI dataset', version='2')

    @property
    @lru_cache(maxsize=1)
    def buildtest_sample_2_regression_automobile_price_prediction_compare_algorithms_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BuildTest-Sample 2 - Regression Automobile Price Prediction (Compare Algorithms) [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def bot_detection_6m_input_0417_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='bot detection - 6M input - 0417 [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def sample_4_classification_credit_risk_prediction_cost_sensitive_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 4 - Classification Credit Risk Prediction(Cost Sensitive) [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def bot_detection_6m_input_0417_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='bot detection - 6M input - 0417 [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def sample_1_regression_automobile_price_prediction_basic_clean_missing_data(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 1 - Regression Automobile Price Prediction(Basic) [Clean Missing Data]', version='1')

    @property
    @lru_cache(maxsize=1)
    def sample_1_regression_automobile_price_prediction_basic_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Sample 1 - Regression Automobile Price Prediction(Basic) [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def botdetection_small_data_trained_model(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BotDetection - small data [trained model]', version='1')

    @property
    @lru_cache(maxsize=1)
    def botdetectionsimple_csv(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='BotDetectionSimple.csv', version='1')

    @property
    @lru_cache(maxsize=1)
    def mydatasettest(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='mydatasettest', version='1')

    @property
    @lru_cache(maxsize=1)
    def td_sample_1_regression_automobile_price_prediction_basic_clean_missing_data_cleaning_transformation_f6dc0eb1(self):
        """This is a dataset promoted by inference graph generation automatically on 08/04/2020 10:18:04. 
 Training pipeline draft:Sample 1: Regression - Automobile Price Prediction (Basic) 
Training pipeline draftId:6fef1f06-578f-4a1e-956e-3716b8794670 
Module Name:Clean Missing Data 
ModuleId:69f583b3-803f-5e0d-9362-11e8b83bca5b 
Port:Cleaning_transformation"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='TD-Sample_1:_Regression_-_Automobile_Price_Prediction_(Basic)-Clean_Missing_Data-Cleaning_transformation-f6dc0eb1', version='3')

    @property
    @lru_cache(maxsize=1)
    def md_sample_1_regression_automobile_price_prediction_basic_train_model_trained_model_fb404f70(self):
        """No description for this dataset."""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='MD-Sample_1:_Regression_-_Automobile_Price_Prediction_(Basic)-Train_Model-Trained_model-fb404f70', version='5')

    @property
    @lru_cache(maxsize=1)
    def dfd_bot_detection_training_with_4g_data_score_model_scored_dataset(self):
        """This is a dataset promoted by inference graph generation automatically on 10/18/2019 9:20:55 AM. 
 Training pipeline draft:Bot Detection Training with 4G data 
Module Name:Score Model, ModuleId:d6e9e132-7103-5729-80c9-55dc481942de 
Port:Scored_dataset"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='DFD-Bot_Detection_Training_with_4G_data-Score_Model-Scored_dataset', version='1')

    @property
    @lru_cache(maxsize=1)
    def td_bot_detection_training_with_4g_data_clean_missing_data_cleaning_transformation(self):
        """This is a dataset promoted by inference graph generation automatically on 10/18/2019 9:20:19 AM. 
 Training pipeline draft:Bot Detection Training with 4G data 
Module Name:Clean Missing Data, ModuleId:ca612efb-d298-5001-a821-25eebbd0a17f 
Port:Cleaning_transformation"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='TD-Bot_Detection_Training_with_4G_data-Clean_Missing_Data-Cleaning_transformation', version='1')

    @property
    @lru_cache(maxsize=1)
    def md_bot_detection_training_with_4g_data_train_model_trained_model(self):
        """This is a dataset promoted by inference graph generation automatically on 10/18/2019 9:20:07 AM. 
 Training pipeline draft:Bot Detection Training with 4G data 
Module Name:Train Model, ModuleId:2dd6beef-8022-524e-b1bf-f1acb284927d 
Port:Trained_model"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='MD-Bot_Detection_Training_with_4G_data-Train_Model-Trained_model', version='1')

    @property
    @lru_cache(maxsize=1)
    def trainingdata(self):
        """bot detection training data 4G"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='trainingdata', version='1')

    @property
    @lru_cache(maxsize=1)
    def missing_data_cleaning_transformation(self):
        """This is a dataset promoted by inference graph generation automatically on 10/16/2019 1:35:25 AM. 
 Training pipeline draft:Sample1-Automobile Price Prediction 
Module Name:Clean Missing Data, ModuleId:cf3e003a-7a7f-5dfb-9d95-24a7fc8931fa 
Port:Cleaning_transformation"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Missing_Data-Cleaning_transformation', version='1')

    @property
    @lru_cache(maxsize=1)
    def prediction_train_model_trained_model(self):
        """This is a dataset promoted by inference graph generation automatically on 10/16/2019 1:35:03 AM. 
 Training pipeline draft:Sample1-Automobile Price Prediction 
Module Name:Train Model, ModuleId:e768c3b1-83cc-55b5-8584-728740f547a4 
Port:Trained_model"""
        return Dataset.get_by_name(
            _workspace.lisal_amlservice(),
            name='Prediction-Train_Model-Trained_model', version='1')


datasets = Datasets()
