"""
Handles command-line parsing and execution for the game.
"""
from rich.console import Console
from rich.table import Table

from src.data import JobStatus
from src.game import Game
from src.tutorials import TUTORIALS

console = Console()

class CommandHandler:
    """
    Parses user input and calls the appropriate methods on the Game instance.
    """
    def __init__(self, game: Game):
        self.game = game
        self.commands = {
            "help": self._help,
            "tutorial": self._tutorial,
            "status": self._status,
            "ls-jobs": self._ls_jobs,
            "submit": self._submit,
            "cancel": self._cancel,
            "show-job": self._show_job,
            "terraform": self._terraform,
            "cost": self._cost,
            "autoscale": self._autoscale,
            "debug": self._debug,
            "convert-onnx": self._convert_onnx,
            "log": self._log,
            "metrics": self._metrics,
            "save": self._save,
            "load": self._load,
            "exit": self._exit,
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
        """Displays a list of available commands."""
        table = Table(title="Available Commands", show_header=True, header_style="bold magenta")
        table.add_column("Command", style="dim", width=30)
        table.add_column("Description")
        commands_help = {
            "help": "Displays this help message.",
            "tutorial [list|show|start <id>]": "Lists tutorials, shows skills for one, or starts one.",
            "status": "Shows the current state of the cluster and resource utilization.",
            "ls-jobs": "Lists all incoming jobs in the queue.",
            "submit <job_id> <node_id>": "Submits a job to a specific node.",
            "cancel <job_id>": "Cancels a running job.",
            "show-job <job_id>": "Provides detailed information about a job.",
            "terraform plan": "Previews changes from the cluster configuration.",
            "terraform apply [ -target=<node_id> ]": "Provisions resources based on the configuration, optionally targeting a specific node.",
            "terraform destroy <node_id>": "Destroys a specific node in the cluster.",
            "terraform show": "Displays the current Terraform state.",
            "terraform import <node_id>": "Imports an unmanaged node into Terraform state.",
            "cost": "Displays the current resource expenditure.",
            "autoscale <on/off>": "Toggles autoscaling.",
            "debug <job_id>": "Shows an error log for a failed job.",
            "convert-onnx <job_id>": "Converts a completed model for optimization.",
            "log": "Displays a history of game events.",
            "metrics": "Displays key performance metrics and statistics.",
            "save": "Saves the current game state.",
            "load": "Loads a saved game state.",
            "exit": "Quits the game.",
        }
        for cmd, desc in commands_help.items():
            table.add_row(cmd, desc)
        console.print(table)

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
                    if tid in self.game.completed_tutorials:
                        status = "[bold green]Completed[/bold green]"
                    elif self.game.active_tutorial_id and self.game.active_tutorial_id == tid:
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
            if self.game.start_tutorial(tutorial_id):
                # Find name for confirmation message
                for category, tutorials in TUTORIALS.items():
                    if tutorial_id in tutorials:
                        name = tutorials[tutorial_id]["name"]
                        console.print(f"[bold green]Starting tutorial: '{name}'...[/bold green]")
                        break
            else:
                console.print("[bold red]Tutorial not found.[/bold red]")
        else:
            console.print("[bold red]Usage: tutorial [list|show|start <ID>][/bold red]")

    def _status(self, args):
        """Shows the current state of the cluster."""
        console.print(f"[bold]Time: {self.game.time} | Score: {self.game.score} | Cost: ${self.game.cost:.2f}[/bold]")
        table = Table(title="Cluster Status", show_header=True, header_style="bold cyan")
        table.add_column("Node ID")
        table.add_column("CPU (Used/Total)")
        table.add_column("GPU (Used/Total)")
        table.add_column("RAM (Used/Total)")
        table.add_column("PyTorch Version")
        table.add_column("Running Jobs")

        for node in self.game.cluster.nodes.values():
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

    def _ls_jobs(self, args):
        """Lists all pending jobs."""
        table = Table(title="Pending Jobs", show_header=True, header_style="bold yellow")
        table.add_column("Job ID")
        table.add_column("Type")
        table.add_column("CPU")
        table.add_column("GPU")
        table.add_column("RAM")
        table.add_column("Deadline")

        for job in self.game.job_queue:
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
        result = self.game.submit_job(args[0], args[1])
        console.print(result)

    def _cancel(self, args):
        """Cancels a running job."""
        if len(args) != 1:
            console.print("[bold red]Usage: cancel <job_id>[/bold red]")
            return
        result = self.game.cancel_job(args[0])
        console.print(result)

    def _show_job(self, args):
        """Shows detailed information about a job."""
        if len(args) != 1:
            console.print("[bold red]Usage: show-job <job_id>[/bold red]")
            return
        job = self.game.get_job(args[0])
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

    def _terraform(self, args):
        """Handles terraform commands (plan, apply, destroy, show, import)."""
        if not args:
            console.print("[bold red]Usage: terraform <plan|apply|destroy|show|import> [args][/bold red]")
            return

        subcommand = args[0]

        if subcommand == "plan":
            result = self.game.terraform_plan()
            console.print(result)
        elif subcommand == "apply":
            target_node = None
            if len(args) > 1 and args[1].startswith("-target="):
                target_node = args[1].split("=")[1]
            result = self.game.terraform_apply(target=target_node)
            console.print(result)
        elif subcommand == "destroy":
            if len(args) < 2:
                console.print("[bold red]Usage: terraform destroy <node_id>[/bold red]")
                return
            node_id = args[1]
            result = self.game.terraform_destroy(node_id)
            console.print(result)
        elif subcommand == "show":
            result = self.game.terraform_show()
            console.print(result)
        elif subcommand == "import":
            if len(args) < 2:
                console.print("[bold red]Usage: terraform import <node_id>[/bold red]")
                return
            node_id = args[1]
            result = self.game.terraform_import(node_id)
            console.print(result)
        else:
            console.print(f"[bold red]Unknown terraform subcommand: '{subcommand}'[/bold red]")

    def _cost(self, args):
        """Displays the current cost."""
        console.print(f"Total accumulated cost: ${self.game.cost:.2f}")

    def _autoscale(self, args):
        """Toggles autoscaling."""
        if not args or args[0] not in ["on", "off"]:
            console.print("[bold red]Usage: autoscale <on|off>[/bold red]")
            return
        self.game.autoscaling_enabled = args[0] == "on"
        status = "enabled" if self.game.autoscaling_enabled else "disabled"
        console.print(f"Autoscaling is now {status}.")

    def _debug(self, args):
        """Shows the error log for a failed job."""
        if len(args) != 1:
            console.print("[bold red]Usage: debug <job_id>[/bold red]")
            return
        job = self.game.get_job(args[0])
        if job and job.status == JobStatus.FAILED:
            console.print(f"[bold red]Error for job '{job.id}': {job.error_message}[/bold red]")
        else:
            console.print("Job not found or has not failed.")

    def _convert_onnx(self, args):
        """Converts a completed job to ONNX format."""
        if len(args) != 1:
            console.print("[bold red]Usage: convert-onnx <job_id>[/bold red]")
            return
        result = self.game.convert_to_onnx(args[0])
        console.print(result)

    def _log(self, args):
        """Displays the game event log."""
        table = Table(title="Event Log", show_header=True, header_style="bold green")
        table.add_column("Event")
        for event in self.game.event_log[:10]:  # Show last 10 events
            table.add_row(event)
        console.print(table)

    def _metrics(self, args):
        """Displays key performance metrics and statistics."""
        metrics = self.game.get_metrics()
        table = Table(title="Performance Metrics", show_header=True, header_style="bold blue")
        table.add_column("Metric", style="dim", width=30)
        table.add_column("Value")
        table.add_row("Total Time Elapsed", str(metrics["total_time"]))
        table.add_row("Total Completed Jobs", str(metrics["completed_jobs"]))
        table.add_row("Total Failed Jobs", str(metrics["failed_jobs"]))
        table.add_row("Average Job Completion Time", f"{metrics["avg_completion_time"]:.2f} time units")
        table.add_row("Total Cost", f"${metrics["total_cost"]:.2f}")
        console.print(table)

    def _save(self, args):
        """Saves the game state."""
        result = self.game.save_game()
        console.print(result)

    def _load(self, args):
        """Loads the game state."""
        result = self.game.load_game()
        console.print(result)

    def _exit(self, args):
        """Exits the game."""
        console.print("[bold blue]Exiting game. Goodbye![/bold blue]")
        raise SystemExit