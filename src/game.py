"""
Core game logic for the AI Ops Simulator.
"""
import json
import random
import re
from typing import Dict, List, Optional

from src.data import (TERRAFORM_CONFIG, Cluster, Job, JobStatus, JobType, Node)
from src.tutorials import TUTORIALS

class Game:
    """
    Manages the game state, including the cluster, jobs, score, and events.
    """
    def __init__(self):
        self.cluster = Cluster()
        self.job_queue: List[Job] = []
        self.completed_jobs: List[Job] = []
        self.failed_jobs: List[Job] = []
        self.score = 0
        self.time = 0
        self.cost = 0
        self.autoscaling_enabled = False
        self.event_log: List[str] = []
        self.terraform_plan_preview = ""
        # Tutorial state
        self.active_tutorial: Optional[Dict] = None
        self.active_tutorial_id: Optional[str] = None
        self.tutorial_step = 0
        self.completed_tutorials: List[str] = []

    def update(self):
        """Main game loop update function."""
        # Do not update game state if a tutorial is active
        if self.active_tutorial:
            return
        self.time += 1
        self.cost += self._calculate_cost()
        self._generate_jobs()
        self._process_running_jobs()
        self._handle_events()
        if self.autoscaling_enabled:
            self._autoscale_resources()

    def setup_tutorial_state(self, jobs: int = 0, nodes: int = 0, custom_setup: str = None):
        """Sets up a clean state for a tutorial scenario."""
        self.job_queue.clear()
        self.completed_jobs.clear()
        self.failed_jobs.clear()
        self.cluster = Cluster()

        for i in range(nodes):
            node = Node(f"node-{i}", 8, 2, 64, "2.0")
            self.cluster.add_node(node)

        for _ in range(jobs):
            job_type = random.choice([JobType.PYTORCH_TRAINING, JobType.INFERENCE])
            requirements = {"cpu": random.randint(1, 2), "gpu": random.randint(0, 1), "ram": random.randint(4, 8)}
            new_job = Job(job_type, requirements, self.time + 50, "2.0" if job_type == JobType.PYTORCH_TRAINING else None)
            self.job_queue.append(new_job)
        
        if custom_setup:
            exec(custom_setup)

    def start_tutorial(self, tutorial_id: str) -> bool:
        """Starts an interactive tutorial by searching through categories."""
        for category, tutorials in TUTORIALS.items():
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
            # Need to get category for log message
            cat = None
            for c, tutorials_in_cat in TUTORIALS.items():
                if tutorial_id in tutorials_in_cat:
                    cat = c
                    break
            self.log_event(f"Tutorial '{TUTORIALS[cat][tutorial_id]['name']}' completed!")
            # Reset to a default state
            self.setup_tutorial_state(jobs=2, nodes=2)


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

        # For dynamic commands like 'submit', just check the command itself
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

    def _calculate_cost(self) -> float:
        """Calculates the resource cost for the current time step."""
        cost = 0
        for node in self.cluster.nodes.values():
            cost += node.resources["cpu"] * 0.1 + node.resources["gpu"] * 0.5 + node.resources["ram"] * 0.05
        return cost

    def _generate_jobs(self):
        """Randomly generates new jobs."""
        if random.random() < 0.3:  # 30% chance to generate a new job
            job_type = random.choice([JobType.PYTORCH_TRAINING, JobType.INFERENCE])
            requirements = {
                "cpu": random.randint(1, 4),
                "gpu": random.randint(0, 2),
                "ram": random.randint(4, 32),
            }
            deadline = self.time + random.randint(20, 50)
            pytorch_version = "2.0" if job_type == JobType.PYTORCH_TRAINING else None
            new_job = Job(job_type, requirements, deadline, pytorch_version)
            self.job_queue.append(new_job)
            self.log_event(f"New job '{new_job.id}' arrived: {new_job.type.value}")

    def _process_running_jobs(self):
        """Processes all jobs currently running on nodes."""
        for node in self.cluster.nodes.values():
            for job in list(node.running_jobs):
                job.progress += 10  # Simulate work being done
                if job.progress >= 100:
                    self.complete_job(job, node)
                elif self.time > job.deadline:
                    self.fail_job(job, node, "Deadline missed")

    def _handle_events(self):
        """Handles random game events."""
        if random.random() < 0.05:  # 5% chance of a random event
            event_type = random.choice(["hardware_failure", "urgent_job"])
            if event_type == "hardware_failure" and self.cluster.nodes:
                node_id = random.choice(list(self.cluster.nodes.keys()))
                node = self.cluster.get_node(node_id)
                if node:
                    for job in list(node.running_jobs):
                        self.fail_job(job, node, "Hardware failure")
                    self.cluster.remove_node(node_id)
                    self.log_event(f"Hardware failure on node '{node_id}'! Node removed.")
            elif event_type == "urgent_job":
                urgent_job = Job(JobType.INFERENCE, {"cpu": 2, "gpu": 1, "ram": 8}, self.time + 15)
                self.job_queue.insert(0, urgent_job)
                self.log_event(f"Urgent job '{urgent_job.id}' arrived with a tight deadline!")

    def _autoscale_resources(self):
        """Automatically scales resources based on job queue size."""
        if len(self.job_queue) > 5 and len(self.cluster.nodes) < 10:
            self.terraform_apply()
            self.log_event("Autoscaling triggered: Added new nodes.")
        elif len(self.job_queue) < 2 and len(self.cluster.nodes) > 2:
            node_to_remove = random.choice(list(self.cluster.nodes.keys()))
            if not self.cluster.nodes[node_to_remove].running_jobs:
                self.cluster.remove_node(node_to_remove)
                self.log_event(f"Autoscaling triggered: Removed idle node '{node_to_remove}'.")

    def submit_job(self, job_id: str, node_id: str) -> str:
        """Submits a job to a specific node."""
        job = self.get_job(job_id)
        node = self.cluster.get_node(node_id)

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
                job.submission_time = self.time # Set submission time
                self.log_event(f"Job '{job_id}' submitted to node '{node_id}'.")
                return f"Job '{job_id}' submitted successfully."
            except ValueError as e:
                return str(e)
        else:
            if job.pytorch_version and job.pytorch_version != node.pytorch_version:
                self.fail_job(job, node, f"PyTorch version mismatch: Job needs {job.pytorch_version}, node has {node.pytorch_version}")
            else:
                self.fail_job(job, node, "Insufficient resources")
            return f"Failed to submit job '{job_id}': Resource or version mismatch."

    def cancel_job(self, job_id: str) -> str:
        """Cancels a running job."""
        job = self.get_job(job_id)
        if not job or job.status != JobStatus.RUNNING:
            return "Cannot cancel job: Not found or not running."

        node = self.cluster.get_node(job.assigned_node)
        if node:
            node.release_job(job)
            job.status = JobStatus.PENDING
            self.job_queue.append(job)
            self.log_event(f"Job '{job_id}' cancelled and returned to queue.")
            return f"Job '{job_id}' cancelled."
        return "Error cancelling job."

    def complete_job(self, job: Job, node: Node):
        """Marks a job as complete and awards points."""
        node.release_job(job)
        job.status = JobStatus.COMPLETED
        job.completion_time = self.time # Set completion time
        self.completed_jobs.append(job)
        self.score += 100
        self.log_event(f"Job '{job.id}' completed successfully on node '{node.id}'.")

    def fail_job(self, job: Job, node: Optional[Node], reason: str):
        """Marks a job as failed and logs the reason."""
        if node and job in node.running_jobs:
            node.release_job(job)
        if job in self.job_queue:
            self.job_queue.remove(job)

        job.status = JobStatus.FAILED
        job.error_message = reason
        self.failed_jobs.append(job)
        self.score -= 50
        self.log_event(f"Job '{job.id}' failed: {reason}")

    def terraform_plan(self) -> str:
        """Generates a plan for provisioning resources from the mock config."""
        match = re.search(r'count = (\d+)', TERRAFORM_CONFIG)
        count = int(match.group(1)) if match else 0
        self.terraform_plan_preview = f"Terraform will create {count} new nodes."
        return self.terraform_plan_preview

    def terraform_apply(self, target: Optional[str] = None) -> str:
        """Applies the terraform plan to provision new nodes."""
        match_count = re.search(r'count = (\d+)', TERRAFORM_CONFIG)
        match_cpu = re.search(r'cpu = (\d+)', TERRAFORM_CONFIG)
        match_gpu = re.search(r'gpu = (\d+)', TERRAFORM_CONFIG)
        match_ram = re.search(r'ram = (\d+)', TERRAFORM_CONFIG)
        match_version = re.search(r'pytorch_version = "([\d.]+)"', TERRAFORM_CONFIG)

        if not all([match_count, match_cpu, match_gpu, match_ram, match_version]):
            return "Error parsing Terraform config."

        if target:
            node = self.cluster.get_node(target)
            if not node:
                return f"Target node '{target}' not found."
            node.resources["cpu"] = int(match_cpu.group(1))
            node.resources["gpu"] = int(match_gpu.group(1))
            node.resources["ram"] = int(match_ram.group(1))
            self.log_event(f"Terraform applied: Targeted update for node '{target}'.")
            return f"Node '{target}' has been updated."

        count = int(match_count.group(1))
        for i in range(count):
            node_name = f"node-{len(self.cluster.nodes) + i}"
            new_node = Node(
                name=node_name,
                cpu=int(match_cpu.group(1)),
                gpu=int(match_gpu.group(1)),
                ram=int(match_ram.group(1)),
                pytorch_version=match_version.group(1)
            )
            self.cluster.add_node(new_node)
        self.log_event(f"Terraform applied: {count} nodes provisioned.")
        return f"{count} nodes have been provisioned."

    def terraform_destroy(self, node_id: str) -> str:
        """Removes a node from the cluster."""
        node = self.cluster.get_node(node_id)
        if not node:
            return f"Node '{node_id}' not found."

        if node.running_jobs:
            return f"Cannot destroy node '{node_id}': it has running jobs."

        self.cluster.remove_node(node_id)
        self.log_event(f"Terraform destroyed node '{node_id}'.")
        return f"Node '{node_id}' destroyed."

    def terraform_show(self) -> str:
        """Displays a simplified view of the Terraform state."""
        output = "# Terraform State:\n"
        for node_id, node in self.cluster.nodes.items():
            if node.unmanaged:
                continue
            output += f'''resource "cluster_node" "{node_id}" {{
  cpu             = {node.resources["cpu"]}
  gpu             = {node.resources["gpu"]}
  ram             = {node.resources["ram"]}
  pytorch_version = "{node.pytorch_version}"
}}
'''
        return output

    def terraform_import(self, node_id: str) -> str:
        """Imports an unmanaged node into the Terraform state."""
        node = self.cluster.get_node(node_id)
        if not node:
            return f"Node '{node_id}' not found to import."
        if not node.unmanaged:
            return f"Node '{node_id}' is already managed by Terraform."
        
        node.unmanaged = False
        self.log_event(f"Terraform imported node '{node_id}' into state.")
        return f"Successfully imported '{node_id}' into Terraform state."

    def convert_to_onnx(self, job_id: str) -> str:
        """Converts a completed PyTorch job to an ONNX job for optimization."""
        job = self.get_job(job_id)
        if not job or job.type != JobType.PYTORCH_TRAINING or job.status != JobStatus.COMPLETED:
            return "Job must be a completed PyTorch training job."

        onnx_job = Job(
            job_type=JobType.ONNX,
            requirements={k: v // 2 for k, v in job.requirements.items()},  # Reduced requirements
            deadline=self.time + 30,
        )
        self.job_queue.append(onnx_job)
        self.log_event(f"Job '{job.id}' converted to ONNX job '{onnx_job.id}'.")
        return f"Created new ONNX job '{onnx_job.id}' with reduced resource needs."

    def get_job(self, job_id: str) -> Optional[Job]:
        """Finds a job by its ID across all lists."""
        for job_list in [self.job_queue, self.completed_jobs, self.failed_jobs]:
            for job in job_list:
                if job.id == job_id:
                    return job
        for node in self.cluster.nodes.values():
            for job in node.running_jobs:
                if job.id == job_id:
                    return job
        return None

    def get_metrics(self) -> Dict[str, float]:
        """Calculates and returns key performance metrics."""
        total_completed_jobs = len(self.completed_jobs)
        total_failed_jobs = len(self.failed_jobs)

        total_completion_time = 0
        for job in self.completed_jobs:
            if job.submission_time is not None and job.completion_time is not None:
                total_completion_time += (job.completion_time - job.submission_time)

        avg_completion_time = total_completion_time / total_completed_jobs if total_completed_jobs > 0 else 0

        return {
            "total_time": self.time,
            "completed_jobs": total_completed_jobs,
            "failed_jobs": total_failed_jobs,
            "avg_completion_time": avg_completion_time,
            "total_cost": self.cost,
        }

    def log_event(self, message: str):
        """Adds an event to the game log."""
        self.event_log.insert(0, f"[Time: {self.time}] {message}")

    def save_game(self, filename: str = "savegame.json") -> str:
        """Saves the current game state to a JSON file."""
        all_jobs = self.job_queue + self.completed_jobs + self.failed_jobs
        for node in self.cluster.nodes.values():
            all_jobs.extend(node.running_jobs)

        state = {
            "time": self.time,
            "score": self.score,
            "cost": self.cost,
            "autoscaling_enabled": self.autoscaling_enabled,
            "event_log": self.event_log,
            "jobs": {job.id: job.to_dict() for job in all_jobs},
            "cluster": self.cluster.to_dict(),
            "completed_tutorials": self.completed_tutorials,
        }
        try:
            with open(filename, "w") as f:
                json.dump(state, f, indent=4)
            self.log_event("Game saved.")
            return f"Game saved to {filename}."
        except IOError as e:
            return f"Error saving game: {e}"

    def load_game(self, filename: str = "savegame.json") -> str:
        """Loads the game state from a JSON file."""
        try:
            with open(filename, "r") as f:
                state = json.load(f)

            jobs_map = {job_id: Job.from_dict(job_data) for job_id, job_data in state["jobs"].items()}

            self.time = state["time"]
            self.score = state["score"]
            self.cost = state["cost"]
            self.autoscaling_enabled = state["autoscaling_enabled"]
            self.event_log = state["event_log"]
            self.cluster = Cluster.from_dict(state["cluster"], jobs_map)
            self.completed_tutorials = state.get("completed_tutorials", [])

            self.job_queue = [j for j in jobs_map.values() if j.status == JobStatus.PENDING]
            self.completed_jobs = [j for j in jobs_map.values() if j.status == JobStatus.COMPLETED]
            self.failed_jobs = [j for j in jobs_map.values() if j.status == JobStatus.FAILED]

            self.log_event("Game loaded.")
            return f"Game loaded from {filename}."
        except (IOError, json.JSONDecodeError) as e:
            return f"Error loading game: {e}"
