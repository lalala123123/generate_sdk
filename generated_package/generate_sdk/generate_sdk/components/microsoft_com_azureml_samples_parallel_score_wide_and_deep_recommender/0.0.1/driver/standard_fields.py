# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Defines Part B of the logging schema, optional keys that have a common meaning across telemetry data."""
from enum import Enum, IntEnum


class AzureMLTelemetryTaskResult(IntEnum):
    Success = 1
    Failure = 2
    Cancelled = 3


class AzureMLTelemetryTaskStage(Enum):
    Queued = 1
    NotStarted = 2
    Preparing = 3
    Provisioning = 4
    Starting = 5
    Running = 6
    Finalizing = 7
    CancelRequested = 50
    Others = 100


class AzureMLTelemetryFailureReason(Enum):
    UserError = 1
    SystemError = 2


class AzureMLWorkspaceSKU(Enum):
    Basic = 1
    Enterprise = 2
    Community = 3


class AzureMLTelemetryFeatureSKU(Enum):
    DNN_FORECASTING = 1
    DNN_NLP = 2
    IMAGE_CLASSIFICATION = 3
    IMAGE_MULTI_LABEL_CLASSIFICATION = 4
    IMAGE_OBJECT_DETECTION = 5
    STREAMING = 6
    FEATURIZATION_CUSTOMIZATION = 7
    GUARDRAILS = 8
    FORECASTING_NEW_LEARNERS = 9
    PARALLEL_FEATURIZATION = 10
    HIERARCHAL_FORECASTING = 11
    GROUPED_FORECASTING = 12
    MANY_MODEL_TRAINING = 13
    RAW_FEATURE_EXPLANATION = 14


class AzureMLTelemetryComputeType(IntEnum):
    AmlcTrain = 1
    AmlcInference = 2
    AmlcDsi = 3
    Remote = 4
    AzureDatabricks = 5
    HdiCluster = 6
    AKS = 7
    ADLA = 8
    ACI = 9
    Arcadia = 10
    SparkOnCosmos = 11
    AzureNotebookVM = 12
    DSVM = 20
    BatchAI = 30
    Local = 50
    Others = 100


class AzureMLTelemetryAuthType(Enum):
    ServicePrincipal = 1
    InteractiveAuth = 2


class AzureMLTelemetryFramework(Enum):
    Python = 1
    PySpark = 2
    TensorFlow = 3
    R = 4
    PyTorch = 5
    CNTK = 6
    Others = 100


class AzureMLTelemetryScalingType(Enum):
    AutoScale = 1
    Manual = 2


class AzureMLTelemetryDatasetType(Enum):
    File = 1
    Tabular = 2
    TimeSeries = 3
    Others = 100


class AzureMLTelemetryDistributedBackend(Enum):
    Mpi = 1
    Horovod = 2
    Others = 100


class AzureMLTelemetryOS(Enum):
    Windows = 1
    Linux = 2
    MacOS = 3
    Android = 4
    iOS = 5
    Others = 100


class AzureMLTelemetryClientType(Enum):
    SDK = 1
    Browser = 2
    Cli = 3
    Others = 100


class StandardFields:
    """Defines Part B of the logging schema, optional keys that have a common meaning across telemetry data."""

    def __init__(
        self,
        Duration=None,
        TaskResult=None,
        FailureReason: AzureMLTelemetryFailureReason = None,
        WorkspaceRegion=None,
        ComputeType: AzureMLTelemetryComputeType = None,
        Attribution=None,
        ClientOS: str = None,
        ClientOSVersion=None,
        RunId=None,
        ParentRunId=None,
        ExperimentId=None,
        NumberOfNodes=None,
        NumberOfCores=None,
        DatasetType: AzureMLTelemetryDatasetType = None,
    ):
        """Initialize a new instance of the StandardFields."""
        self.Duration = Duration
        self.TaskResult = TaskResult
        self.FailureReason = FailureReason
        self.WorkspaceRegion = WorkspaceRegion
        self.ComputeType = ComputeType
        self.Attribution = Attribution
        self.ClientOS = ClientOS
        self.ClientOSVersion = ClientOSVersion
        self.RunId = RunId
        self.ParentRunId = ParentRunId
        self.ExperimentId = ExperimentId
        self.NumberOfNodes = NumberOfNodes
        self.NumberOfCores = NumberOfCores
        self.DatasetType = DatasetType
