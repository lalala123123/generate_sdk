# THIS IS AN AUTO GENERATED FILE.
# PLEASE DO NOT MODIFY MANUALLY.
# Components included in this generated file:
#  - microsoft.com.azureml.samples.hello_world_with_cpu_image::0.0.1
#  - microsoft.com.azureml.samples.parallel_copy_files_v1::0.0.2
#  - microsoft.com.azureml.samples.train-in-spark::0.0.1
#  - bing.relevance.convert2ss::0.0.4
#  - microsoft.com.azureml.samples.tune::0.0.4
from pathlib import Path
from typing import Union

from azure.ml.component import Component
from azure.ml.component.component import Input, Output


SOURCE_DIRECTORY = Path(__file__).parent / ".."


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
    partition_keys: Union[str, list]
    """The keys used to partition dataset into mini-batches. If specified, the data with the same key will be partitioned into the same mini-batch. If both \"Partition keys\" and \"Mini batch size\" are specified, \"Mini batch size\" will be ignored. It should be a list of str element each being a key used to partition the input dataset."""
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


class _HDInsightComponentRunsettingHdinsight:
    """_HDInsightComponentRunsettingHdinsight"""
    conf: Union[str, dict]
    """Spark configuration properties"""
    driver_cores: int
    """Number of cores to use for the driver process"""
    driver_memory: str
    """Amount of memory to use for the driver process.It's the same format as JVM memory strings. Use lower-case suffixes, e.g. k, m, g, t, and p, for kibi-, mebi-, gibi-, tebi-, and pebibytes, respectively."""
    executor_cores: int
    """Number of cores to use for each executor"""
    executor_memory: str
    """Amount of memory to use per executor process. It's the same format as JVM memory strings. Use lower-case suffixes, e.g. k, m, g, t, and p, for kibi-, mebi-, gibi-, tebi-, and pebibytes, respectively."""
    name: str
    """The name of this session"""
    number_executors: int
    """Number of executors to launch for this session"""
    queue: str
    """The name of the YARN queue to which submitted"""


class _HDInsightComponentRunsetting:
    """Run setting configuration for HDInsightComponent"""
    target: str
    """Hdi Compute name that is attached to AML"""
    hdinsight: _HDInsightComponentRunsettingHdinsight
    """_HDInsightComponentRunsettingHdinsight"""


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


class _SweepComponentRunsettingDockerConfiguration:
    """Docker configuration section specify the docker runtime properties for the Run.."""
    arguments: Union[str, list]
    """Extra arguments to the Docker run command. The extra docker container options like --cpus=2, --memory=1024"""
    shared_volumes: bool
    """Indicates whether to use shared volumes. Set to False if necessary to work around shared volume bugs on Windows. The default is True."""
    shm_size: str
    """The size of the Docker container's shared memory block. If not set, the default 2g is used."""
    use_docker: bool
    """Specifies whether the environment to run the experiment should be Docker-based. Amlcompute linux clusters require that jobs running inside Docker containers. The backend will override the value to be true for Amlcompute linux clusters."""


class _SweepComponentRunsettingEnvironment:
    """Environment section set runtime environment."""
    conda: str
    """Defines conda dependencies"""
    docker: str
    """Defines settings to customize the Docker image built to the environment's specifications."""
    os: str
    """Defines the operating system the component running on. Could be Windows or Linux. Defaults to Linux if not specified. (enum: ['Windows', 'Linux'])"""


class _SweepComponentRunsettingResourceLayout:
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    instance_count: int
    """Number of instances in the compute target used for training. (min: 1)"""
    instance_type: str
    """Instance type used for training."""
    node_count: int
    """Number of nodes in the compute target used for training. (min: 1)"""


class _SweepComponentRunsettingEarlyTermination:
    """This section contains specific early termination settings for sweep component."""
    delay_evaluation: int
    """delays the first policy evaluation for a specified number of intervals."""
    evaluation_interval: int
    """the frequency for applying the policy."""
    policy_type: str
    """The early termination policy type. Current default means no termination policy. (enum: ['default', 'bandit', 'median_stopping', 'truncation_selection'])"""
    slack_amount: float
    """the slack amount allowed with respect to the best performing training run."""
    slack_factor: float
    """the slack ratio allowed with respect to the best performing training run."""
    truncation_percentage: int
    """the percentage of lowest performing runs to terminate at each evaluation interval. An integer value between 1 and 99. (min: 1, max: 99)"""


class _SweepComponentRunsettingLimits:
    """This section contains specific limits settings for sweep component."""
    max_concurrent_trials: int
    """Maximum number of runs that can run concurrently. If not specified, all runs launch in parallel. If specified, must be an integer between 1 and 100. (min: 1, max: 100)"""
    max_total_trials: int
    """Maximum number of training runs. Must be an integer between 1 and 1000. (min: 1, max: 1000)"""
    timeout_minutes: int
    """Maximum duration, in minutes, of the hyperparameter tuning experiment. Runs after this duration are canceled. (min: 0)"""


class _SweepComponentRunsettingObjective:
    """This section contains specific objective settings for sweep component."""
    goal: str
    """Whether the primary metric will be maximized or minimized when evaluating the runs. (enum: ['minimize', 'maximize'])"""
    primary_metric: str
    """The name of the primary metric needs to exactly match the name of the metric logged by the training script."""


class _SweepComponentRunsettingSweep:
    """_SweepComponentRunsettingSweep"""
    early_termination: _SweepComponentRunsettingEarlyTermination
    """This section contains specific early termination settings for sweep component."""
    limits: _SweepComponentRunsettingLimits
    """This section contains specific limits settings for sweep component."""
    objective: _SweepComponentRunsettingObjective
    """This section contains specific objective settings for sweep component."""


class _SweepComponentRunsettingTargetSelector:
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


class _SweepComponentRunsetting:
    """Run setting configuration for SweepComponent"""
    environment_variables: Union[str, dict]
    """Environment variables can be used to specify environment variables to be passed. It is a dictionary of environment name to environment value mapping. User can use this to adjust some component runtime behavior which is not exposed as component parameter, e.g. enable some debug switch."""
    priority: int
    """The priority of a job which is a integer. For AmlK8s Compute, User can set it to 100~200. Any value larger than 200 or less than 100 will be treated as 200. For Aml Compute, User can set it to 1~1000. Any value larger than 1000 or less than 1 will be treated as 1000."""
    target: str
    """The compute target to use"""
    docker_configuration: _SweepComponentRunsettingDockerConfiguration
    """Docker configuration section specify the docker runtime properties for the Run.."""
    environment: _SweepComponentRunsettingEnvironment
    """Environment section set runtime environment."""
    resource_layout: _SweepComponentRunsettingResourceLayout
    """resource section controls the number of nodes, cpus, gpus the job will consume."""
    sweep: _SweepComponentRunsettingSweep
    """_SweepComponentRunsettingSweep"""
    target_selector: _SweepComponentRunsettingTargetSelector
    """Specify desired target properties, instead of specifying a cluster name. When target is set, target_selector will be ignored."""


class _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageInput:
    input_path: Input = None
    """The directory contains dataframe."""
    string_parameter: str = None
    """A parameter accepts a string value. (optional)"""


class _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageOutput:
    output_path: Output = None
    """The directory contains a dataframe."""


class _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageInput
    outputs: _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageOutput
    runsettings: _DistributedComponentRunsetting


_microsoft_com_azureml_samples_hello_world_with_cpu_image = None


def microsoft_com_azureml_samples_hello_world_with_cpu_image(
    input_path: Path = None,
    string_parameter: str = None,
) -> _MicrosoftComAzuremlSamplesHelloWorldWithCpuImageComponent:
    """A hello world tutorial to create a module for ml.azure.com.
    
    :param input_path: The directory contains dataframe.
    :type input_path: Path
    :param string_parameter: A parameter accepts a string value. (optional)
    :type string_parameter: str
    :output output_path: The directory contains a dataframe.
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples_hello_world_with_cpu_image
    if _microsoft_com_azureml_samples_hello_world_with_cpu_image is None:
        _microsoft_com_azureml_samples_hello_world_with_cpu_image = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_hello_world_with_cpu_image/0.0.1/component.yaml")
    return _microsoft_com_azureml_samples_hello_world_with_cpu_image(
            input_path=input_path,
            string_parameter=string_parameter,)


class _MicrosoftComAzuremlSamplesParallelCopyFilesV1Input:
    input_folder: Input = None
    """AnyDirectory"""


class _MicrosoftComAzuremlSamplesParallelCopyFilesV1Output:
    output_folder: Output = None
    """Output images"""


class _MicrosoftComAzuremlSamplesParallelCopyFilesV1Component(Component):
    inputs: _MicrosoftComAzuremlSamplesParallelCopyFilesV1Input
    outputs: _MicrosoftComAzuremlSamplesParallelCopyFilesV1Output
    runsettings: _ParallelComponentRunsetting


_microsoft_com_azureml_samples_parallel_copy_files_v1 = None


def microsoft_com_azureml_samples_parallel_copy_files_v1(
    input_folder: Path = None,
) -> _MicrosoftComAzuremlSamplesParallelCopyFilesV1Component:
    """A sample Parallel module to copy files.
    
    :param input_folder: AnyDirectory
    :type input_folder: Path
    :output output_folder: Output images
    :type: output_folder: Output
    """
    global _microsoft_com_azureml_samples_parallel_copy_files_v1
    if _microsoft_com_azureml_samples_parallel_copy_files_v1 is None:
        _microsoft_com_azureml_samples_parallel_copy_files_v1 = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_parallel_copy_files_v1/0.0.2/component.yaml")
    return _microsoft_com_azureml_samples_parallel_copy_files_v1(
            input_folder=input_folder,)


class _MicrosoftComAzuremlSamplesTrainInSparkInput:
    input_path: Input = None
    """Iris csv file"""
    regularization_rate: float = 0.01
    """Regularization rate when training with logistic regression (optional)"""


class _MicrosoftComAzuremlSamplesTrainInSparkOutput:
    output_path: Output = None
    """The output path to save the trained model to"""


class _MicrosoftComAzuremlSamplesTrainInSparkComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesTrainInSparkInput
    outputs: _MicrosoftComAzuremlSamplesTrainInSparkOutput
    runsettings: _HDInsightComponentRunsetting


_microsoft_com_azureml_samples_train_in_spark = None


def microsoft_com_azureml_samples_train_in_spark(
    input_path: Path = None,
    regularization_rate: float = 0.01,
) -> _MicrosoftComAzuremlSamplesTrainInSparkComponent:
    """Train a Spark ML model using an HDInsight Spark cluster
    
    :param input_path: Iris csv file
    :type input_path: Path
    :param regularization_rate: Regularization rate when training with logistic regression (optional)
    :type regularization_rate: float
    :output output_path: The output path to save the trained model to
    :type: output_path: Output
    """
    global _microsoft_com_azureml_samples_train_in_spark
    if _microsoft_com_azureml_samples_train_in_spark is None:
        _microsoft_com_azureml_samples_train_in_spark = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_train_in_spark/0.0.1/component_spec.yaml")
    return _microsoft_com_azureml_samples_train_in_spark(
            input_path=input_path,
            regularization_rate=regularization_rate,)


class _BingRelevanceConvert2SsInput:
    TextData: Input = None
    """relative path on ADLS storage"""
    ExtractionClause: str = None
    """the extraction clause, something like \"column1:string, column2:int\""""


class _BingRelevanceConvert2SsOutput:
    SSPath: Output = None
    """output path of ss"""


class _BingRelevanceConvert2SsComponent(Component):
    inputs: _BingRelevanceConvert2SsInput
    outputs: _BingRelevanceConvert2SsOutput
    runsettings: _ScopeComponentRunsetting


_bing_relevance_convert2ss = None


def bing_relevance_convert2ss(
    TextData: Path = None,
    ExtractionClause: str = None,
) -> _BingRelevanceConvert2SsComponent:
    """Convert ADLS test data to SS format
    
    :param TextData: relative path on ADLS storage
    :type TextData: Path
    :param ExtractionClause: the extraction clause, something like \"column1:string, column2:int\"
    :type ExtractionClause: str
    :output SSPath: output path of ss
    :type: SSPath: Output
    """
    global _bing_relevance_convert2ss
    if _bing_relevance_convert2ss is None:
        _bing_relevance_convert2ss = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/bing_relevance_convert2ss/0.0.4/component_spec.yaml")
    return _bing_relevance_convert2ss(
            TextData=TextData,
            ExtractionClause=ExtractionClause,)


class _MicrosoftComAzuremlSamplesTuneInput:
    training_data: Input = None
    """Training data organized in the torchvision format/structure"""
    max_epochs: int = None
    """Maximum number of epochs for the training"""
    learning_rate: float = None
    """learning_rate (min: 0.001, max: 0.1)"""
    subsample: float = None
    """learning_rate (min: 0.1, max: 0.5)"""


class _MicrosoftComAzuremlSamplesTuneOutput:
    best_model: Output = None
    """model"""
    saved_model: Output = None
    """path"""
    other_output: Output = None
    """path"""


class _MicrosoftComAzuremlSamplesTuneComponent(Component):
    inputs: _MicrosoftComAzuremlSamplesTuneInput
    outputs: _MicrosoftComAzuremlSamplesTuneOutput
    runsettings: _SweepComponentRunsetting


_microsoft_com_azureml_samples_tune = None


def microsoft_com_azureml_samples_tune(
    training_data: Path = None,
    max_epochs: int = None,
    learning_rate: float = None,
    subsample: float = None,
) -> _MicrosoftComAzuremlSamplesTuneComponent:
    """A dummy hyperparameter tuning component
    
    :param training_data: Training data organized in the torchvision format/structure
    :type training_data: Path
    :param max_epochs: Maximum number of epochs for the training
    :type max_epochs: int
    :param learning_rate: learning_rate (min: 0.001, max: 0.1)
    :type learning_rate: float
    :param subsample: learning_rate (min: 0.1, max: 0.5)
    :type subsample: float
    :output best_model: model
    :type: best_model: Output
    :output saved_model: path
    :type: saved_model: Output
    :output other_output: path
    :type: other_output: Output
    """
    global _microsoft_com_azureml_samples_tune
    if _microsoft_com_azureml_samples_tune is None:
        _microsoft_com_azureml_samples_tune = Component.from_yaml(yaml_file=SOURCE_DIRECTORY / "components/microsoft_com_azureml_samples_tune/0.0.4/sweep.spec.yaml")
    return _microsoft_com_azureml_samples_tune(
            training_data=training_data,
            max_epochs=max_epochs,
            learning_rate=learning_rate,
            subsample=subsample,)


# No datasets class is generated.
