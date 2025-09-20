# src/commands/general_commands.py

from rich.console import Console
from rich.table import Table
import os
from .base_command import BaseCommand

console = Console()

class GeneralCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("general", "General commands for the simulator")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("help", "Show available commands and their descriptions", self._help)
        self.add_subcommand("clear", "Clear the console", self._clear)

    def execute(self, *args):
        if not args:
            self.show_help()
            return

        subcommand = args[0]
        if subcommand in self.subcommands:
            handler = self.subcommands[subcommand]["handler"]
            handler(*args[1:])
        else:
            console.print(f"[bold red]Unknown subcommand: {subcommand}[/bold red]")
            self.show_help()

    def _help(self, *args):
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
        table_general.add_row("quit-tutorial", "Exits the current tutorial and returns to the main prompt.")
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
        table_jax.add_row("jax-jit", "Simulates JIT compiling a function for performance with JAX.")
        console.print(table_jax)

        # Simulated PyTorch Commands
        console.print("\n[bold blue]Simulated PyTorch Commands:[/bold blue]")
        table_pytorch = Table(show_header=True, header_style="bold cyan")
        table_pytorch.add_column("Command", style="dim", width=30)
        table_pytorch.add_column("Description", width=50, wrap=True)
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
        table_onnx.add_column("Description", width=50, wrap=True)
        table_onnx.add_row("convert-onnx <job_id>", "Converts a completed simulated model to ONNX format for optimization.")
        console.print(table_onnx)

    def _help(self, *args):
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
        table_general.add_row("quit-tutorial", "Exits the current tutorial and returns to the main prompt.")
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
        table_jax.add_row("jax-jit", "Simulates JIT compiling a function for performance with JAX.")
        console.print(table_jax)

        # Simulated PyTorch Commands
        console.print("\n[bold blue]Simulated PyTorch Commands:[/bold blue]")
        table_pytorch = Table(show_header=True, header_style="bold cyan")
        table_pytorch.add_column("Command", style="dim", width=30)
        table_pytorch.add_column("Description", width=50, wrap=True)
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
        table_onnx.add_column("Description", width=50, wrap=True)
        table_onnx.add_row("convert-onnx <job_id>", "Converts a completed simulated model to ONNX format for optimization.")
        console.print(table_onnx)

    def _clear(self, *args):
        """Clears the console."""
        os.system('cls' if os.name == 'nt' else 'clear')

class ExitCommand(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("exit", "Exit the simulator")
        self.tutorial_manager = tutorial_manager

    def execute(self, *args):
        raise SystemExit
