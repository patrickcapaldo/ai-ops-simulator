# src/tutorial_manager.py
import json
import random
import re
import os
import importlib.util
from enum import Enum
from typing import Dict, List, Optional, Any

# Simplified data structures for tutorials
class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class JobType(Enum):
    PYTORCH_TRAINING = "pytorch_training"
    INFERENCE = "inference"
    ONNX = "onnx"
    ONNX_INFERENCE = "onnx_inference" # Added for clarity

class Node:
    def __init__(self, name: str, cpu: int, gpu: int, ram: int, pytorch_version: str, unmanaged: bool = False):
        self.id = name
        self.resources = {"cpu": cpu, "gpu": gpu, "ram": ram}
        self.available_resources = {"cpu": cpu, "gpu": gpu, "ram": ram}
        self.pytorch_version = pytorch_version
        self.running_jobs: List[Job] = []
        self.unmanaged = unmanaged

    def can_run_job(self, job: 'Job') -> bool:
        if job.pytorch_version and job.pytorch_version != self.pytorch_version:
            return False
        return (self.available_resources["cpu"] >= job.requirements.get("cpu", 0) and
                self.available_resources["gpu"] >= job.requirements.get("gpu", 0) and
                self.available_resources["ram"] >= job.requirements.get("ram", 0))

    def assign_job(self, job: 'Job'):
        if not self.can_run_job(job):
            raise ValueError("Insufficient resources or version mismatch to assign job.")
        self.available_resources["cpu"] -= job.requirements.get("cpu", 0)
        self.available_resources["gpu"] -= job.requirements.get("gpu", 0)
        self.available_resources["ram"] -= job.requirements.get("ram", 0)
        job.status = JobStatus.RUNNING
        job.assigned_node = self.id
        self.running_jobs.append(job)

    def release_job(self, job: 'Job'):
        if job in self.running_jobs:
            self.available_resources["cpu"] += job.requirements.get("cpu", 0)
            self.available_resources["gpu"] += job.requirements.get("gpu", 0)
            self.available_resources["ram"] += job.requirements.get("ram", 0)
            self.running_jobs.remove(job)

class Job:
    _job_id_counter = 0

    def __init__(self, job_type: JobType, requirements: Dict[str, int], deadline: int, pytorch_version: Optional[str] = None):
        Job._job_id_counter += 1
        self.id = f"job-{Job._job_id_counter}"
        self.type = job_type
        self.requirements = requirements
        self.deadline = deadline
        self.pytorch_version = pytorch_version
        self.status = JobStatus.PENDING
        self.assigned_node: Optional[str] = None
        self.progress = 0
        self.error_message: Optional[str] = None
        self.submission_time: Optional[int] = None
        self.completion_time: Optional[int] = None

class TutorialManager:
    def __init__(self):
        self.cluster: Dict[str, Node] = {}
        self.job_queue: List[Job] = []
        self.completed_jobs: List[Job] = []
        self.failed_jobs: List[Job] = []
        self.active_tutorial: Optional[Dict] = None
        self.active_tutorial_id: Optional[str] = None
        self.tutorial_step = 0
        self.completed_tutorials: List[str] = []
        self.time = 0 # Simplified time for tutorials
        self.terraform_config = """
resource "cluster_node" "default" {
  count           = 1
  cpu             = 8
  gpu             = 2
  ram             = 64
  pytorch_version = "2.0"
}
"""
        self.prometheus_config = """
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
"""
        self.tutorials: Dict[str, Dict[str, Any]] = {}
        self._load_tutorials()

    def _load_tutorials(self):
        self.tutorials = {}
        tutorial_dir = "src/tutorials"
        for filename in os.listdir(tutorial_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(tutorial_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, 'TUTORIAL_CATEGORY') and hasattr(module, 'TUTORIALS'):
                    try:
                        category = getattr(module, 'TUTORIAL_CATEGORY')
                        tutorials_data = getattr(module, 'TUTORIALS')

                        if category not in self.tutorials:
                            self.tutorials[category] = {}

                        for tutorial_id, tutorial_info in tutorials_data.items():
                            # Copy all existing info and then add the module
                            tutorial_entry = tutorial_info.copy()
                            tutorial_entry["module"] = module
                            self.tutorials[category][tutorial_id] = tutorial_entry
                    except (AttributeError, KeyError, TypeError) as e:
                        print(f"Warning: Error loading tutorial from {filename}: {e}. Skipping this tutorial.")
                else:
                    print(f"Warning: Tutorial file {filename} is missing TUTORIAL_CATEGORY or TUTORIALS variable.")

    def get_all_tutorials(self):
        return self.tutorials

    def get_terraform_config(self) -> str:
        return self.terraform_config

    def set_terraform_config(self, config: str):
        self.terraform_config = config

    def get_prometheus_config(self) -> str:
        return self.prometheus_config

    def set_prometheus_config(self, config: str):
        self.prometheus_config = config

    def setup_tutorial_state(self, jobs: int = 0, nodes: int = 0, custom_setup: str = None, clear_terraform_config: bool = False):
        """Sets up a clean state for a tutorial scenario."""
        self.job_queue.clear()
        self.completed_jobs.clear()
        self.failed_jobs.clear()
        self.cluster.clear() # Clear existing nodes

        if clear_terraform_config:
            self.terraform_config = """
resource "cluster_node" "default" {
  count           = 1
  cpu             = 8
  gpu             = 2
  ram             = 64
  pytorch_version = "2.0"
}
"""

        for i in range(nodes):
            node = Node(f"node-{i}", 8, 2, 64, "2.0")
            self.cluster[node.id] = node

        for _ in range(jobs):
            job_type = random.choice([JobType.PYTORCH_TRAINING, JobType.INFERENCE])
            requirements = {"cpu": random.randint(1, 2), "gpu": random.randint(0, 1), "ram": random.randint(4, 8)}
            new_job = Job(job_type, requirements, self.time + 50, "2.0" if job_type == JobType.PYTORCH_TRAINING else None)
            self.job_queue.append(new_job)
        
        if custom_setup:
            # This is a security risk in a real application, but for a local CLI tutorial, it's acceptable.
            # The custom_setup string comes from the trusted tutorials.py file.
            exec(custom_setup, {'game': self, 'Node': Node, 'Job': Job, 'JobType': JobType, 'TERRAFORM_CONFIG': self.terraform_config, 'PROMETHEUS_CONFIG': self.prometheus_config, 're': re})


    def start_tutorial(self, tutorial_id: str, tutorials_data: Dict) -> bool:
        """Starts an interactive tutorial by searching through categories."""
        for category, tutorials in tutorials_data.items():
            if tutorial_id in tutorials:
                self.active_tutorial = tutorials[tutorial_id]
                self.active_tutorial_id = tutorial_id
                self.tutorial_step = 0
                first_step = self.active_tutorial["steps"][0]
                if "trigger" in first_step and callable(first_step["trigger"]):
                    first_step["trigger"](self)
                return True
        return False

    def end_tutorial(self):
        """Ends the current tutorial and marks it as complete."""
        if self.active_tutorial:
            tutorial_id = self.active_tutorial_id
            
            if tutorial_id and tutorial_id not in self.completed_tutorials:
                self.completed_tutorials.append(tutorial_id)
            
            self.active_tutorial = None
            self.active_tutorial_id = None
            self.tutorial_step = 0
            # self.log_event(f"Tutorial '{tutorials_data[cat][tutorial_id]['name']}\' completed!") # No event log in simplified version
            # Reset to a default state
            self.setup_tutorial_state(jobs=0, nodes=0) # Start with a clean slate after tutorial

    def get_tutorial_prompt(self) -> str:
        """Gets the instructional text for the current tutorial step."""
        if not self.active_tutorial:
            return ""
        return self.active_tutorial["steps"][self.tutorial_step]["text"]

    def check_tutorial_input(self, user_input: str) -> bool:
        """Checks if the user input matches the expectation for the current tutorial step."""
        if not self.active_tutorial:
            return False

        step = self.active_tutorial["steps"][self.tutorial_step]
        expected = step["expected_command"]
        
        if expected is None: # End of tutorial
            return True

        # For dynamic commands like \'submit\', just check the command itself
        if step.get("is_dynamic"):
            return user_input.strip().startswith(expected)
        
        return user_input.strip() == expected

    def advance_tutorial(self):
        """Moves to the next step in the tutorial."""
        if not self.active_tutorial:
            return

        self.tutorial_step += 1
        if self.tutorial_step >= len(self.active_tutorial["steps"]):
            self.end_tutorial()
        else:
            # Trigger action for the new step
            next_step = self.active_tutorial["steps"][self.tutorial_step]
            if "trigger" in next_step and callable(next_step["trigger"]):
                next_step["trigger"](self)

    # --- Mocked Game-like functions for tutorials ---
    def get_job(self, job_id: str) -> Optional[Job]:
        """Finds a job by its ID across all lists."""
        for job_list in [self.job_queue, self.completed_jobs, self.failed_jobs]:
            for job in job_list:
                if job.id == job_id:
                    return job
        for node in self.cluster.values():
            for job in node.running_jobs:
                if job.id == job_id:
                    return job
        return None

    def submit_job(self, job_id: str, node_id: str) -> str:
        """Submits a job to a specific node."""
        job = self.get_job(job_id)
        node = self.cluster.get(node_id)

        if not job:
            return "Job not found."
        if not node:
            return "Node not found."
        if job.status != JobStatus.PENDING:
            return "Job is not pending."

        if node.can_run_job(job):
            try:
                node.assign_job(job)
                self.job_queue.remove(job)
                job.submission_time = self.time
                return f"Job '{job_id}' submitted successfully."
            except ValueError as e:
                return str(e)
        else:
            if job.pytorch_version and job.pytorch_version != node.pytorch_version:
                job.status = JobStatus.FAILED
                job.error_message = f"PyTorch version mismatch: Job needs {job.pytorch_version}, node has {node.pytorch_version}"
                self.failed_jobs.append(job)
                if job in self.job_queue: self.job_queue.remove(job)
                return f"Failed to submit job '{job_id}': PyTorch version mismatch."
            else:
                job.status = JobStatus.FAILED
                job.error_message = "Insufficient resources"
                self.failed_jobs.append(job)
                if job in self.job_queue: self.job_queue.remove(job)
                return f"Failed to submit job '{job_id}': Resource mismatch."

    def complete_job(self, job: Job, node: Node):
        """Marks a job as complete and awards points."""
        node.release_job(job)
        job.status = JobStatus.COMPLETED
        job.completion_time = self.time
        self.completed_jobs.append(job)

    def fail_job(self, job: Job, node: Optional[Node], reason: str):
        """Marks a job as failed and logs the reason."""
        if node and job in node.running_jobs:
            node.release_job(job)
        if job in self.job_queue:
            self.job_queue.remove(job)

        job.status = JobStatus.FAILED
        job.error_message = reason
        self.failed_jobs.append(job)

    def terraform_plan(self) -> str:
        """Generates a plan for provisioning resources from the mock config."""
        match = re.search(r'count = (\d+)', self.terraform_config)
        count = int(match.group(1)) if match else 0
        self.terraform_plan_preview = f"Terraform will create {count} new nodes."
        return self.terraform_plan_preview

    def terraform_apply(self, target: Optional[str] = None) -> str:
        """Applies the terraform plan to provision new nodes."""
        match_count = re.search(r'count = (\d+)', self.terraform_config)
        match_cpu = re.search(r'cpu = (\d+)', self.terraform_config)
        match_gpu = re.search(r'gpu = (\d+)', self.terraform_config)
        match_ram = re.search(r'ram = (\d+)', self.terraform_config)
        match_version = re.search(r'pytorch_version = "([\d.]+)"', self.terraform_config)

        if not all([match_count, match_cpu, match_gpu, match_ram, match_version]):
            return "Error parsing Terraform config."

        if target:
            node = self.cluster.get(target)
            if not node:
                return f"Target node '{target}' not found."
            node.resources["cpu"] = int(match_cpu.group(1))
            node.resources["gpu"] = int(match_gpu.group(1))
            node.resources["ram"] = int(match_ram.group(1))
            node.available_resources = node.resources.copy() # Reset available resources
            return f"Node '{target}' has been updated."

        count = int(match_count.group(1))
        for i in range(count):
            node_name = f"node-{len(self.cluster) + i}"
            new_node = Node(
                name=node_name,
                cpu=int(match_cpu.group(1)),
                gpu=int(match_gpu.group(1)),
                ram=int(match_ram.group(1)),
                pytorch_version=match_version.group(1)
            )
            self.cluster[new_node.id] = new_node
        return f"{count} nodes have been provisioned."

    def terraform_destroy(self, node_id: str) -> str:
        """Removes a node from the cluster."""
        node = self.cluster.get(node_id)
        if not node:
            return f"Node '{node_id}' not found."

        if node.running_jobs:
            return f"Cannot destroy node '{node_id}': it has running jobs."

        del self.cluster[node_id]
        return f"Node '{node_id}' destroyed."

    def terraform_show(self) -> str:
        """Displays a simplified view of the Terraform state."""
        output = "# Terraform State:\n"
        for node_id, node in self.cluster.items():
            if node.unmanaged:
                continue
            output += f"""resource \"cluster_node\" \"{node_id}\" {{
  cpu             = {node.resources["cpu"]}
  gpu             = {node.resources["gpu"]}
  ram             = {node.resources["ram"]}
  pytorch_version = \"{node.pytorch_version}\" 
}}
"""
        return output

    def terraform_import(self, node_id: str) -> str:
        """Imports an unmanaged node into the Terraform state."""
        node = self.cluster.get(node_id)
        if not node:
            return f"Node '{node_id}' not found to import."
        if not node.unmanaged:
            return f"Node '{node_id}' is already managed by Terraform."
        
        node.unmanaged = False
        return f"Successfully imported '{node_id}' into Terraform state."

    def terraform_state_list(self) -> str:
        """Lists all resources in the Terraform state."""
        output = ""
        for node_id, node in self.cluster.items():
            if not node.unmanaged:
                output += f"{node_id}\n"
        return output

    def convert_to_onnx(self, job_id: str) -> str:
        """Converts a completed PyTorch job to an ONNX job for optimization."""
        job = self.get_job(job_id)
        if not job or job.type != JobType.PYTORCH_TRAINING or job.status != JobStatus.COMPLETED:
            return "Job must be a completed PyTorch training job."

        onnx_job = Job(
            job_type=JobType.ONNX_INFERENCE, # Changed to ONNX_INFERENCE for clarity
            requirements={k: v // 2 for k, v in job.requirements.items()},  # Reduced requirements
            deadline=self.time + 30,
        )
        self.job_queue.append(onnx_job)
        return f"Created new ONNX job '{onnx_job.id}' with reduced resource needs."

    # Helper functions for commands that need to inspect state
    def ls_jobs(self) -> List[Job]:
        return self.job_queue

    def get_cluster_status(self) -> Dict[str, Node]:
        return self.cluster

    def get_completed_jobs(self) -> List[Job]:
        return self.completed_jobs

    def get_failed_jobs(self) -> List[Job]:
        return self.failed_jobs

    def get_active_tutorial_id(self) -> Optional[str]:
        return self.active_tutorial_id

    def get_completed_tutorials(self) -> List[str]:
        return self.completed_tutorials

    def create_node_trigger(self, node_id, cpu, gpu, ram, pytorch_version, unmanaged=False):
        """A trigger to create a specific node for a tutorial step."""
        new_node = Node(node_id, cpu, gpu, ram, pytorch_version, unmanaged=unmanaged)
        self.cluster[new_node.id] = new_node

    def create_job_trigger(self, job_type, requirements, deadline, pytorch_version=None):
        """A trigger to create a specific job for a tutorial step."""
        new_job = Job(job_type, requirements, deadline, pytorch_version)
        self.job_queue.append(new_job)

# This import needs to be at the bottom to avoid circular dependencies
# as TUTORIALS uses TutorialManager methods in its triggers.

