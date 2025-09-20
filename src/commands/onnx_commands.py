# src/commands/onnx_commands.py

from rich.console import Console
from .base_command import BaseCommand

console = Console()

class ONNXCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("onnx", "Simulated ONNX commands")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("convert-onnx", "Converts a completed job to ONNX format", self._convert_onnx)

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

    def _convert_onnx(self, args):
        """Converts a completed job to ONNX format."""
        if len(args) != 1:
            console.print("[bold red]Usage: convert-onnx <job_id>[/bold red]")
            return
        result = self.tutorial_manager.convert_to_onnx(args[0])
        console.print(result)
