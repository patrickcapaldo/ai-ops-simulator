# src/commands/prometheus_commands.py

from rich.console import Console
from rich.prompt import Prompt
from .base_command import BaseCommand

console = Console()

class PrometheusCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("prometheus", "Simulated Prometheus commands")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("cat", "Simulates the cat command for prometheus.yml", self._cat)
        self.add_subcommand("edit-prometheus-config", "Allows direct editing of the mock Prometheus configuration.", self._edit_prometheus_config)
        self.add_subcommand("restart-prometheus", "Simulates restarting Prometheus.", self._restart_prometheus)

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

    def _cat(self, args):
        """Simulates the cat command for prometheus.yml."""
        if len(args) == 1 and args[0] == "prometheus.yml":
            console.print(self.tutorial_manager.get_prometheus_config())
        else:
            console.print("[bold red]Usage: cat prometheus.yml[/bold red]")

    def _edit_prometheus_config(self, args):
        """Allows direct editing of the mock Prometheus configuration."""
        current_config = self.tutorial_manager.get_prometheus_config()
        console.print("[bold yellow]Current prometheus.yml:[/bold yellow]")
        console.print(current_config)
        console.print("\n[bold yellow]Enter new prometheus.yml (type 'END' on a new line to finish):[/bold yellow]")
        new_config_lines = []
        while True:
            line = Prompt.ask("")
            if line.strip().upper() == "END":
                break
            new_config_lines.append(line)
        self.tutorial_manager.set_prometheus_config("\n".join(new_config_lines))
        console.print("[bold green]prometheus.yml updated.[/bold green]")

    def _restart_prometheus(self, args):
        """Simulates restarting Prometheus."""
        console.print("Simulated restarting Prometheus.")
