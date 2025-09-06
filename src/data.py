"""
Defines the data models for the game, including Job, Node, and Cluster.
"""
import enum
import uuid
from typing import Dict, List, Optional

# Mock Terraform configuration
TERRAFORM_CONFIG = """
resource "cluster_node" "main" {
  count = 4
  cpu = 8
  gpu = 2
  ram = 64
  pytorch_version = "2.0"
}
"""

class JobType(enum.Enum):
    """Enumeration for job types."""
    PYTORCH_TRAINING = "PyTorch Training"
    INFERENCE = "Inference"
    ONNX = "ONNX Inference"

class JobStatus(enum.Enum):
    """Enumeration for job statuses."""
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Job:
    """
    Represents a single job with its resource requirements and status.
    """
    def __init__(self, job_type: JobType, requirements: Dict[str, int], deadline: int, pytorch_version: Optional[str] = None):
        self.id = str(uuid.uuid4())[:8]
        self.type = job_type
        self.requirements = requirements
        self.deadline = deadline
        self.status = JobStatus.PENDING
        self.pytorch_version = pytorch_version
        self.assigned_node: Optional[str] = None
        self.progress = 0
        self.error_message: Optional[str] = None
        self.submission_time: Optional[int] = None  # New attribute
        self.completion_time: Optional[int] = None  # New attribute

    def to_dict(self):
        """Serializes the Job object to a dictionary."""
        return {
            "id": self.id,
            "type": self.type.value,
            "requirements": self.requirements,
            "deadline": self.deadline,
            "status": self.status.value,
            "pytorch_version": self.pytorch_version,
            "assigned_node": self.assigned_node,
            "progress": self.progress,
            "error_message": self.error_message,
            "submission_time": self.submission_time,
            "completion_time": self.completion_time,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        """Deserializes a dictionary back to a Job object."""
        job_type = JobType(data["type"])
        job = cls(job_type, data["requirements"], data["deadline"], data["pytorch_version"])
        job.id = data["id"]
        job.status = JobStatus(data["status"])
        job.assigned_node = data["assigned_node"]
        job.progress = data["progress"]
        job.error_message = data["error_message"]
        job.submission_time = data.get("submission_time")
        job.completion_time = data.get("completion_time")
        return job

class Node:
    """
    Represents a single node in the cluster with its own resources.
    """
    def __init__(self, name: str, cpu: int, gpu: int, ram: int, pytorch_version: str, unmanaged: bool = False):
        self.id = name
        self.resources = {"cpu": cpu, "gpu": gpu, "ram": ram}
        self.available_resources = self.resources.copy()
        self.pytorch_version = pytorch_version
        self.running_jobs: List[Job] = []
        self.unmanaged = unmanaged

    def can_run_job(self, job: Job) -> bool:
        """Checks if the node has enough resources and the correct PyTorch version for a job."""
        if job.pytorch_version and job.pytorch_version != self.pytorch_version:
            return False
        for resource, required in job.requirements.items():
            if self.available_resources.get(resource, 0) < required:
                return False
        return True

    def assign_job(self, job: Job):
        """Assigns a job to the node and allocates resources."""
        if self.can_run_job(job):
            self.running_jobs.append(job)
            job.status = JobStatus.RUNNING
            job.assigned_node = self.id
            for resource, required in job.requirements.items():
                self.available_resources[resource] -= required
        else:
            raise ValueError("Node cannot run the specified job.")

    def release_job(self, job: Job):
        """Releases a job from the node and deallocates resources."""
        if job in self.running_jobs:
            self.running_jobs.remove(job)
            for resource, required in job.requirements.items():
                self.available_resources[resource] += required

    def to_dict(self):
        """Serializes the Node object to a dictionary."""
        return {
            "id": self.id,
            "resources": self.resources,
            "available_resources": self.available_resources,
            "pytorch_version": self.pytorch_version,
            "running_jobs": [job.id for job in self.running_jobs],
            "unmanaged": self.unmanaged,
        }

    @classmethod
    def from_dict(cls, data: Dict, jobs_map: Dict[str, Job]):
        """Deserializes a dictionary back to a Node object."""
        node = cls(data["id"], data["resources"]["cpu"], data["resources"]["gpu"], data["resources"]["ram"], data["pytorch_version"])
        node.available_resources = data["available_resources"]
        node.running_jobs = [jobs_map[job_id] for job_id in data["running_jobs"]]
        node.unmanaged = data.get("unmanaged", False)
        return node

class Cluster:
    """
    Manages the collection of nodes in the cluster.
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}

    def add_node(self, node: Node):
        """Adds a node to the cluster."""
        self.nodes[node.id] = node

    def remove_node(self, node_id: str):
        """Removes a node from the cluster."""
        if node_id in self.nodes:
            del self.nodes[node_id]

    def get_node(self, node_id: str) -> Optional[Node]:
        """Retrieves a node by its ID."""
        return self.nodes.get(node_id)

    def to_dict(self):
        """Serializes the Cluster object to a dictionary."""
        return {"nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()}}

    @classmethod
    def from_dict(cls, data: Dict, jobs_map: Dict[str, Job]):
        """Deserializes a dictionary back to a Cluster object."""
        cluster = cls()
        for node_id, node_data in data["nodes"].items():
            cluster.add_node(Node.from_dict(node_data, jobs_map))
        return cluster
