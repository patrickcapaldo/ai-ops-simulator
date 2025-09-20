# src/commands/terraform_commands.py

from rich.console import Console
from rich.prompt import Prompt
from .base_command import BaseCommand

console = Console()

class TerraformCommands(BaseCommand):
    def __init__(self, tutorial_manager):
        super().__init__("terraform", "Simulated Terraform commands")
        self.tutorial_manager = tutorial_manager
        self.add_subcommand("terraform", "Handles terraform commands (plan, apply, destroy, show, import).", self._terraform)
        self.add_subcommand("edit-terraform-config", "Allows direct editing of the mock Terraform configuration.", self._edit_terraform_config)

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

    def _terraform(self, args):
        """Handles terraform commands (plan, apply, destroy, show, import)."""
        if not args:
            console.print("[bold red]Usage: terraform <plan|apply|destroy|show|import|state> [args][/bold red]")
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
        elif subcommand == "state":
            if len(args) > 1 and args[1] == "list":
                result = self.tutorial_manager.terraform_state_list()
                console.print(result)
            else:
                console.print("[bold red]Usage: terraform state list[/bold red]")
        else:
            console.print(f"[bold red]Unknown terraform subcommand: '{subcommand}'[/bold red]")

    def _edit_terraform_config(self, args):
        """Allows direct editing of the mock Terraform configuration."""
        current_config = self.tutorial_manager.get_terraform_config()
        console.print("[bold yellow]Current TERRAFORM_CONFIG:[/bold yellow]")
        console.print(current_config)
        console.print("\n[bold yellow]Enter new TERRAFORM_CONFIG (type 'END' on a new line to finish):[/bold yellow]")
        new_config_lines = []
        while True:
            line = Prompt.ask("")
            if line.strip().upper() == "END":
                break
            new_config_lines.append(line)
        self.tutorial_manager.set_terraform_config("\n".join(new_config_lines))
        console.print("[bold green]TERRAFORM_CONFIG updated.[/bold green]")
