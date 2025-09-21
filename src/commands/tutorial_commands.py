# src/commands/tutorial_commands.py

from rich.console import Console
from rich.table import Table
from .base_command import BaseCommand


console = Console()

class TutorialCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("tutorial", "Manage and list tutorials")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("list", "List all available tutorials", self._list_tutorials)
        self.add_subcommand("show", "Show details of a tutorial by its ID", self._show_tutorial)
        self.add_subcommand("start", "Start a tutorial by its ID", self._start_tutorial)

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

    def _list_tutorials(self, *args):
        tutorials = self.tutorial_manager.get_all_tutorials()
        if not tutorials:
            console.print("No tutorials available.")
            return

        console.print("\nAvailable Tutorials\n")
        for category, category_tutorials in tutorials.items():
            console.print(f"Category: {category}")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("ID", style="dim", width=15)
            table.add_column("Name", width=50)
            table.add_column("Status")
            for tid, t in category_tutorials.items():
                completed = self.tutorial_manager.get_completed_tutorials()
                active_id = self.tutorial_manager.get_active_tutorial_id()

                if tid in completed:
                    status = "[bold green]Completed[/bold green]"
                elif active_id and active_id == tid:
                    status = "[bold yellow]In Progress[/bold yellow]"
                else:
                    status = "Not Started"
                table.add_row(tid, t["name"], status)
            console.print(table)
        console.print("\nTo see skills taught in a tutorial, type: `tutorial show <ID>`")
        console.print("To start a tutorial, type: `tutorial start <ID>`")

    def _show_tutorial(self, *args):
        if not args or len(args) < 1:
            console.print("[bold red]Usage: tutorial show <ID>[/bold red]")
            return
        tutorial_id = args[0]
        found_tutorial = None
        tutorials = self.tutorial_manager.get_all_tutorials()
        for category, category_tutorials in tutorials.items():
            if tutorial_id in category_tutorials:
                found_tutorial = category_tutorials[tutorial_id]
                break
            
        if found_tutorial:
            console.print(f"\n[bold]Skills for tutorial:[/bold]")
            console.print(f"- {found_tutorial['name']}")
            if "skills_learned" in found_tutorial:
                for skill in found_tutorial["skills_learned"]:
                    console.print(f"- {skill}")
            else:
                console.print("[bold yellow]No specific skills listed for this tutorial.[/bold yellow]")
        else:
            console.print("[bold red]Tutorial not found.[/bold red]")

    def _start_tutorial(self, *args):
        if not args or len(args) < 1:
            console.print("[bold red]Usage: tutorial start <ID>[/bold red]")
            return
        tutorial_id = args[0]
        if self.tutorial_manager.start_tutorial(tutorial_id):
            # Find name for confirmation message
            tutorials = self.tutorial_manager.get_all_tutorials()
            for category, category_tutorials in tutorials.items():
                if tutorial_id in category_tutorials:
                    name = category_tutorials[tutorial_id]["name"]
                    console.print(f"[bold green]Starting tutorial: '{name}'...[/bold green]")
                    break
        else:
            console.print("[bold red]Tutorial not found.[/bold red]")

    def _quit_tutorial(self, *args):
        """Exits the current tutorial and returns to the main prompt."""
        self.tutorial_manager.end_tutorial()
        console.print("[bold green]Exited tutorial. Returning to main prompt.[/bold green]")

class NextCommand(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("next", "Advances to the next step in a tutorial")
        self.tutorial_manager = tutorial_manager

    def execute(self, *args):
        self.tutorial_manager.advance_tutorial()
