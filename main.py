"""
The main entry point for the AI Ops Simulator game.
"""
import time

from rich.console import Console
from rich.prompt import Prompt

from commands import CommandHandler
from game import Game

console = Console()

def main():
    """Initializes the game and starts the main loop."""
    console.print("[bold green]Welcome to the AI Ops Simulator![/bold green]")
    console.print("Your job is to manage a cluster of servers to process AI jobs efficiently.")
    console.print("\nType [bold yellow]tutorial[/bold yellow] for a step-by-step guide, or [bold yellow]help[/bold yellow] for a list of all commands.")

    game = Game()
    command_handler = CommandHandler(game)

    # Initial terraform apply to set up the cluster
    console.print("\n[bold yellow]Applying initial infrastructure setup...[/bold yellow]")
    command_handler.execute("terraform apply")

    try:
        while True:
            if game.active_tutorial:
                # Tutorial Mode
                prompt_text = game.get_tutorial_prompt()
                console.print(f"\n[bold cyan]TUTORIAL:[/bold cyan] {prompt_text}")
                command_input = Prompt.ask("\nEnter command")

                if game.check_tutorial_input(command_input):
                    command_handler.execute(command_input)
                    game.advance_tutorial()
                    if not game.active_tutorial: # Tutorial just ended
                        console.print("[bold green]Tutorial complete! Returning to normal game mode.[/bold green]")
                else:
                    console.print("[bold red]That's not the right command. Try following the instructions carefully.[/bold red]")
            else:
                # Normal Game Mode
                game.update()
                command_input = Prompt.ask("\nEnter command")
                command_handler.execute(command_input)
                time.sleep(1)  # Slow down game loop for playability

    except (KeyboardInterrupt, SystemExit):
        console.print("\n[bold blue]Game over. Thanks for playing![/bold blue]")

if __name__ == "__main__":
    main()
