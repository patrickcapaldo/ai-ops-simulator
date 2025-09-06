# src/commands.py
"""
Handles command-line parsing and execution for the tutorials.
"""
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from src.tutorial_manager import TutorialManager, JobStatus, Node, Job, TERRAFORM_CONFIG
from src.tutorials import TUTORIALS # Import the TUTORIALS dictionary

console = Console()

class CommandHandler:
    """
    Parses user input and calls the appropriate methods on the TutorialManager instance.
    """
    def __init__(self, tutorial_manager: TutorialManager):
        self.tutorial_manager = tutorial_manager
        self.commands = {
            "help": self._help,
            "tutorial": self._tutorial,
            "ls-jobs": self._ls_jobs,
            "submit": self._submit,
            "show-job": self._show_job,
            "status": self._status,
            "terraform": self._terraform,
            "convert-onnx": self._convert_onnx,
            "debug": self._debug, # Keep debug for failed jobs in tutorials
            "edit-terraform-config": self._edit_terraform_config, # New command
            "exit": self._exit, # Added exit command
        }

    def execute(self, command_input: str):
        """Parses and executes a command."""
        parts = command_input.strip().split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]

        if command in self.commands:
            try:
                self.commands[command](args)
            except TypeError:
                console.print(f"[bold red]Invalid arguments for command '{command}'.[/bold red]")
        else:
            console.print(f"[bold red]Unknown command: '{command}'[/bold red]")

    def _help(self, args):
        """Displays a list of available commands, categorized by tool."""
        console.print("[bold]Available Commands:[/bold]")

        # General Commands
        console.print("\n[bold blue]General Commands:[/bold blue]")
        table_general = Table(show_header=True, header_style="bold cyan")
        table_general.add_column("Command", style="dim", width=30)
        table_general.add_column("Description")
        table_general.add_row("help", "Displays this help message.")
        table_general.add_row("tutorial [list|show|start <id>]", "Lists tutorials, shows skills for one, or starts one. This is the main way to learn about different tools.")
        table_general.add_row("exit", "Quits the application.") # Added exit to help
        console.print(table_general)

        # Simulated Kubernetes Commands
        console.print("\n[bold blue]Simulated Kubernetes Commands:[/bold blue]")
        table_k8s = Table(show_header=True, header_style="bold cyan")
        table_k8s.add_column("Command", style="dim", width=30)
        table_k8s.add_column("Description")
        table_k8s.add_row("kubectl apply -f <file>", "Simulates applying a Kubernetes manifest to deploy resources.")
        console.print(table_k8s)

        # Simulated Kubeflow Commands
        console.print("\n[bold blue]Simulated Kubeflow Commands:[/bold blue]")
        table_kf = Table(show_header=True, header_style="bold cyan")
        table_kf.add_column("Command", style="dim", width=30)
        table_kf.add_column("Description")
        table_kf.add_row("kfctl apply -V -f <file>", "Simulates deploying Kubeflow components.")
        table_kf.add_row("kfp run submit <file>", "Simulates submitting a Kubeflow pipeline.")
        console.print(table_kf)

        # Simulated Terraform Commands
        console.print("\n[bold blue]Simulated Terraform Commands:[/bold blue]")
        table_terraform = Table(show_header=True, header_style="bold cyan")
        table_terraform.add_column("Command", style="dim", width=30)
        table_terraform.add_column("Description")
        table_terraform.add_row("terraform plan", "Previews changes from the simulated cluster configuration.")
        table_terraform.add_row("terraform apply [ -target=<node_id> ]", "Provisions resources based on the configuration in the simulated cluster, optionally targeting a specific node.")
        table_terraform.add_row("terraform destroy <node_id>", "Destroys a specific node in the simulated cluster.")
        table_terraform.add_row("terraform show", "Displays the current simulated Terraform state.")
        table_terraform.add_row("terraform import <node_id>", "Imports an unmanaged node into the simulated Terraform state.")
        table_terraform.add_row("terraform init", "Initializes a simulated Terraform working directory.")
        table_terraform.add_row("terraform validate", "Checks simulated Terraform configuration files for syntax and consistency.")
        table_terraform.add_row("terraform fmt", "Rewrites simulated Terraform configuration files to a canonical format.")
        table_terraform.add_row("edit-terraform-config", "Allows direct editing of the mock Terraform configuration used in tutorials.")
        console.print(table_terraform)

        # Simulated JAX Commands
        console.print("\n[bold blue]Simulated JAX Commands:[/bold blue]")
        table_jax = Table(show_header=True, header_style="bold cyan")
        table_jax.add_column("Command", style="dim", width=30)
        table_jax.add_column("Description")
        table_jax.add_row("jax.jit(<function>)", "Simulates JIT compiling a function for performance with JAX.")
        console.print(table_jax)

        # Simulated PyTorch Commands
        console.print("\n[bold blue]Simulated PyTorch Commands:[/bold blue]")
        table_pytorch = Table(show_header=True, header_style="bold cyan")
        table_pytorch.add_column("Command", style="dim", width=30)
        table_pytorch.add_column("Description")
        table_pytorch.add_row("status", "Shows the current state of the simulated cluster and resource utilization.")
        table_pytorch.add_row("ls-jobs", "Lists all incoming jobs in the simulated queue.")
        table_pytorch.add_row("submit <job_id> <node_id>", "Submits a job to a specific node in the simulated cluster.")
        table_pytorch.add_row("show-job <job_id>", "Provides detailed information about a simulated job.")
        table_pytorch.add_row("debug <job_id>", "Shows an error log for a failed simulated job.")
        console.print(table_pytorch)

        # Simulated ONNX Commands
        console.print("\n[bold blue]Simulated ONNX Commands:[/bold blue]")
        table_onnx = Table(show_header=True, header_style="bold cyan")
        table_onnx.add_column("Command", style="dim", width=30)
        table_onnx.add_column("Description")
        table_onnx.add_row("convert-onnx <job_id>", "Converts a completed simulated model to ONNX format for optimization.")
        console.print(table_onnx)

    def _tutorial(self, args):
        """Lists tutorials, shows details, or starts one."""
        if not args or args[0] == "list":
            console.print("[bold]Available Tutorials[/bold]")
            for category, tutorials in TUTORIALS.items():
                console.print(f"\n[bold blue]Category: {category}[/bold blue]")
                table = Table(show_header=True, header_style="bold cyan")
                table.add_column("ID", style="dim", width=15)
                table.add_column("Name")
                table.add_column("Status")
                for tid, t in tutorials.items():
                    if tid in self.tutorial_manager.get_completed_tutorials():
                        status = "[bold green]Completed[/bold green]"
                    elif self.tutorial_manager.get_active_tutorial_id() and self.tutorial_manager.get_active_tutorial_id() == tid:
                        status = "[bold yellow]In Progress[/bold yellow]"
                    else:
                        status = "Not Started"
                    table.add_row(tid, t["name"], status)
                console.print(table)
            console.print("\nTo see skills taught in a tutorial, type: `tutorial show <ID>`")
            console.print("To start a tutorial, type: `tutorial start <ID>`")

        elif args[0] == "show":
            if len(args) < 2:
                console.print("[bold red]Usage: tutorial show <ID>[/bold red]")
                return
            tutorial_id = args[1]
            found_tutorial = None
            for category, tutorials in TUTORIALS.items():
                if tutorial_id in tutorials:
                    found_tutorial = tutorials[tutorial_id]
                    break
            
            if found_tutorial:
                console.print(f"\n[bold]Skills for tutorial: {found_tutorial['name']}[/bold]")
                for skill in found_tutorial["skills_learned"]:
                    console.print(f"- {skill}")
            else:
                console.print("[bold red]Tutorial not found.[/bold red]")

        elif args[0] == "start":
            if len(args) < 2:
                console.print("[bold red]Usage: tutorial start <ID>[/bold red]")
                return
            tutorial_id = args[1]
            if self.tutorial_manager.start_tutorial(tutorial_id, TUTORIALS):
                # Find name for confirmation message
                for category, tutorials in TUTORIALS.items():
                    if tutorial_id in tutorials:
                        name = tutorials[tutorial_id]["name"]
                        console.print(f"[bold green]Starting tutorial: '{name}'...'[/bold green]")
                        break
            else:
                console.print("[bold red]Tutorial not found.[/bold red]")
        else:
            console.print("[bold red]Usage: tutorial [list|show|start <ID>][/bold red]")

    def _ls_jobs(self, args):
        """Lists all pending jobs."""
        job_queue = self.tutorial_manager.ls_jobs()
        if not job_queue:
            console.print("[bold yellow]No pending jobs.[/bold yellow]")
            return

        table = Table(title="Pending Jobs", show_header=True, header_style="bold yellow")
        table.add_column("Job ID")
        table.add_column("Type")
        table.add_column("CPU")
        table.add_column("GPU")
        table.add_column("RAM")
        table.add_column("Deadline")

        for job in job_queue:
            req = job.requirements
            table.add_row(
                job.id,
                job.type.value,
                str(req.get("cpu", 0)),
                str(req.get("gpu", 0)),
                f"{req.get('ram', 0)} GB",
                str(job.deadline)
            )
        console.print(table)

    def _submit(self, args):
        """Submits a job to a node."""
        if len(args) != 2:
            console.print("[bold red]Usage: submit <job_id> <node_id>[/bold red]")
            return
        result = self.tutorial_manager.submit_job(args[0], args[1])
        console.print(result)

    def _show_job(self, args):
        """Shows detailed information about a job."""
        if len(args) != 1:
            console.print("[bold red]Usage: show-job <job_id>[/bold red]")
            return
        job = self.tutorial_manager.get_job(args[0])
        if not job:
            console.print("[bold red]Job not found.[/bold red]")
            return

        table = Table(title=f"Job Details: {job.id}", show_header=False)
        table.add_column("Field", style="bold")
        table.add_column("Value")
        table.add_row("Type", job.type.value)
        table.add_row("Status", job.status.value)
        table.add_row("CPU Req", str(job.requirements.get("cpu", 0)))
        table.add_row("GPU Req", str(job.requirements.get("gpu", 0)))
        table.add_row("RAM Req", f"{job.requirements.get('ram', 0)} GB")
        table.add_row("Deadline", str(job.deadline))
        if job.pytorch_version:
            table.add_row("PyTorch Version", job.pytorch_version)
        if job.status == JobStatus.RUNNING:
            table.add_row("Assigned Node", job.assigned_node)
            table.add_row("Progress", f"{job.progress}%")
        if job.status == JobStatus.FAILED:
            table.add_row("Error", job.error_message)
        console.print(table)

    def _status(self, args):
        """Shows the current state of the cluster."""
        cluster = self.tutorial_manager.get_cluster_status()
        if not cluster:
            console.print("[bold yellow]No nodes in the cluster.[/bold yellow]")
            return

        table = Table(title="Cluster Status", show_header=True, header_style="bold cyan")
        table.add_column("Node ID")
        table.add_column("CPU (Used/Total)")
        table.add_column("GPU (Used/Total)")
        table.add_column("RAM (Used/Total)")
        table.add_column("PyTorch Version")
        table.add_column("Running Jobs")

        for node in cluster.values():
            cpu_total = node.resources["cpu"]
            cpu_used = cpu_total - node.available_resources["cpu"]
            gpu_total = node.resources["gpu"]
            gpu_used = gpu_total - node.available_resources["gpu"]
            ram_total = node.resources["ram"]
            ram_used = ram_total - node.available_resources["ram"]
            jobs = ", ".join([job.id for job in node.running_jobs])
            table.add_row(
                node.id,
                f"{cpu_used}/{cpu_total}",
                f"{gpu_used}/{gpu_total}",
                f"{ram_used}/{ram_total} GB",
                node.pytorch_version,
                jobs
            )
        console.print(table)

    def _terraform(self, args):
        """Handles terraform commands (plan, apply, destroy, show, import)."""
        if not args:
            console.print("[bold red]Usage: terraform <plan|apply|destroy|show|import> [args][/bold red]")
            return

        subcommand = args[0]

        if subcommand == "plan":
            result = self.tutorial_manager.terraform_plan()
            console.print(result)
        elif subcommand == "apply":
            target_node = None
            if len(args) > 1 and args[1].startswith("-target="):
                target_node = args[1].split("=")[1]
            result = self.tutorial_manager.terraform_apply(target=target_node)
            console.print(result)
        elif subcommand == "destroy":
            if len(args) < 2:
                console.print("[bold red]Usage: terraform destroy <node_id>[/bold red]")
                return
            node_id = args[1]
            result = self.tutorial_manager.terraform_destroy(node_id)
            console.print(result)
        elif subcommand == "show":
            result = self.tutorial_manager.terraform_show()
            console.print(result)
        elif subcommand == "import":
            if len(args) < 2:
                console.print("[bold red]Usage: terraform import <node_id>[/bold red]")
                return
            node_id = args[1]
            result = self.tutorial_manager.terraform_import(node_id)
            console.print(result)
        elif subcommand == "init": # Added for tutorial
            console.print("Terraform has been initialized.")
        elif subcommand == "validate": # Added for tutorial
            console.print("Terraform configuration is valid.")
        elif subcommand == "fmt": # Added for tutorial
            console.print("Terraform configuration formatted.")
        else:
            console.print(f"[bold red]Unknown terraform subcommand: '{subcommand}'[/bold red]")

    def _convert_onnx(self, args):
        """Converts a completed job to ONNX format."""
        if len(args) != 1:
            console.print("[bold red]Usage: convert-onnx <job_id>[/bold red]")
            return
        result = self.tutorial_manager.convert_to_onnx(args[0])
        console.print(result)

    def _debug(self, args):
        """Shows the error log for a failed job."""
        if len(args) != 1:
            console.print("[bold red]Usage: debug <job_id>[/bold red]")
            return
        job = self.tutorial_manager.get_job(args[0])
        if job and job.status == JobStatus.FAILED:
            console.print(f"[bold red]Error for job '{job.id}': {job.error_message}[/bold red]")
        else:
            console.print("Job not found or has not failed.")

    def _edit_terraform_config(self, args):
        """Allows direct editing of the mock Terraform configuration."""
        global TERRAFORM_CONFIG
        console.print("[bold yellow]Current TERRAFORM_CONFIG:[/bold yellow]")
        console.print(TERRAFORM_CONFIG)
        console.print("\n[bold yellow]Enter new TERRAFORM_CONFIG (type 'END' on a new line to finish):[/bold yellow]")
        new_config_lines = []
        while True:
            line = Prompt.ask("")
            if line.strip().upper() == "END":
                break
            new_config_lines.append(line)
        TERRAFORM_CONFIG = "\n".join(new_config_lines)
        console.print("[bold green]TERRAFORM_CONFIG updated.[/bold green]")

    def _exit(self, args):
        """Exits the application."""
        console.print("[bold blue]Exiting tutorials. Goodbye![/bold blue]")
        raise SystemExit
