
# src/commands/__init__.py

from .general_commands import GeneralCommands, ExitCommand
from .tutorial_commands import TutorialCommands
from .job_commands import JobCommands
from .terraform_commands import TerraformCommands
from .kubernetes_commands import KubernetesCommands
from .kubeflow_commands import KubeflowCommands
from .jax_commands import JAXCommands
from .onnx_commands import ONNXCommands
from .pytorch_commands import PyTorchCommands
from .cuda_commands import CUDACommands
from .prometheus_commands import PrometheusCommands

def get_command_handlers(tutorial_manager):
    return [
        GeneralCommands(tutorial_manager),
        ExitCommand(tutorial_manager),
        TutorialCommands(tutorial_manager),
        JobCommands(tutorial_manager),
        TerraformCommands(tutorial_manager),
        KubernetesCommands(tutorial_manager),
        KubeflowCommands(tutorial_manager),
        JAXCommands(tutorial_manager),
        ONNXCommands(tutorial_manager),
        PyTorchCommands(tutorial_manager),
        CUDACommands(tutorial_manager),
        PrometheusCommands(tutorial_manager),
    ]
