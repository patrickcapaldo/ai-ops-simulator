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

    def _clear(self, *args):
        """Clears the console."""
        os.system('cls' if os.name == 'nt' else 'clear')

class HelpCommand(BaseCommand):
    def __init__(self, tutorial_manager, command_executor):
        super().__init__("help", "Show available commands and their descriptions")
        self.tutorial_manager = tutorial_manager
        self.command_executor = command_executor

    def execute(self, *args):
        console.print("[bold]Available Commands:[/bold]")
        for command_name, command_instance in self.command_executor.commands.items():
            console.print(f"\n[bold blue]{command_instance.name}[/bold blue]: {command_instance.description}")
            if command_instance.subcommands:
                table = Table(show_header=True, header_style="bold cyan")
                table.add_column("Subcommand", style="dim", width=30)
                table.add_column("Description")
                for sub_name, sub_info in command_instance.subcommands.items():
                    table.add_row(sub_name, sub_info["description"])
                console.print(table)

class ExitCommand(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("exit", "Exit the simulator")
        self.tutorial_manager = tutorial_manager

    def execute(self, *args):
        raise SystemExit
