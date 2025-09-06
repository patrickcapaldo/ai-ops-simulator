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
    console.print("Type 'help' to see available commands.")

    game = Game()
    command_handler = CommandHandler(game)

    # Initial terraform apply to set up the cluster
    console.print("\n[bold yellow]Applying initial infrastructure setup...[/bold yellow]")
    command_handler.execute("terraform apply")

    try:
        while True:
            game.update()
            command_input = Prompt.ask("\nEnter command")
            command_handler.execute(command_input)
            time.sleep(1)  # Slow down game loop for playability

    except (KeyboardInterrupt, SystemExit):
        console.print("\n[bold blue]Game over. Thanks for playing![/bold blue]")

if __name__ == "__main__":
    main()
