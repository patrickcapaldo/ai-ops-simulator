# src/commands/job_commands.py

from rich.console import Console
from rich.table import Table
from .base_command import BaseCommand
from src.tutorial_manager import JobStatus

console = Console()

class JobCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("job", "Manage simulated jobs")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("ls-jobs", "Lists all pending jobs", self._ls_jobs)
        self.add_subcommand("submit", "Submits a job to a node", self._submit)
        self.add_subcommand("show-job", "Shows detailed information about a job", self._show_job)
        self.add_subcommand("debug", "Shows the error log for a failed job", self._debug)

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
                f'{req.get("ram", 0)} GB',
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
        table.add_row("RAM Req", f'{job.requirements.get("ram", 0)} GB')
        table.add_row("Deadline", str(job.deadline))
        if job.pytorch_version:
            table.add_row("PyTorch Version", job.pytorch_version)
        if job.status == JobStatus.RUNNING:
            table.add_row("Assigned Node", job.assigned_node)
            table.add_row("Progress", f"{job.progress}%")
        if job.status == JobStatus.FAILED:
            table.add_row("Error", job.error_message)
        console.print(table)

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
