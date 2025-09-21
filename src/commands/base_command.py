
# src/commands/base_command.py

from rich.console import Console
from src.tutorial_manager import TutorialManager
from typing import List

console = Console()

class CommandExecutor:
    def __init__(self, tutorial_manager: TutorialManager, command_handlers: List['BaseCommand'] = None):
        self.tutorial_manager = tutorial_manager
        self.commands = {}
        if command_handlers:
            self.set_command_handlers(command_handlers)

    def set_command_handlers(self, command_handlers: List['BaseCommand']):
        for handler in command_handlers:
            self.commands[handler.name] = handler

    def execute(self, command_input: str):
        parts = command_input.strip().split()
        if not parts:
            return
        command = parts[0]
        args = parts[1:]

        if command in self.commands:
            self.commands[command].execute(*args)
        else:
            console.print(f"[bold red]Unknown command: '{command}'[/bold red]")

class BaseCommand:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.subcommands = {}

    def add_subcommand(self, name: str, description: str, handler):
        self.subcommands[name] = {"description": description, "handler": handler}

    def show_help(self):
        console.print(f"[bold green]{self.name}[/bold green]: {self.description}")
        if self.subcommands:
            console.print("[bold yellow]Subcommands:[/bold yellow]")
            for name, info in self.subcommands.items():
                console.print(f"  [bold cyan]{name}[/bold cyan]: {info['description']}")

    def execute(self, *args):
        raise NotImplementedError("Subclasses must implement the execute method")

