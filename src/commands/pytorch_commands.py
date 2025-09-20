# src/commands/pytorch_commands.py

from rich.console import Console
from rich.table import Table
from .base_command import BaseCommand

console = Console()

class PyTorchCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("pytorch", "Simulated PyTorch commands")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("status", "Shows the current state of the cluster", self._status)

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
