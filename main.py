"""
The main entry point for the AI Ops Simulator game.
"""
import time

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

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
                step_data = game.active_tutorial["steps"][game.tutorial_step]
                prompt_text = step_data["text"]
                console.print(f"\n[bold cyan]TUTORIAL:[/bold cyan] {prompt_text}")
                
                doc_prompt = ""
                if step_data.get("doc_link"):
                    doc_prompt += f"[dim]For more info, see:[/dim] [link={step_data['doc_link']}]{step_data['doc_link']}[/link]"
                if step_data.get("doc_quote"):
                    doc_prompt += " [dim](Type [bold]docs[/bold] to see a quote)[/dim]"
                if doc_prompt:
                    console.print(doc_prompt)

                command_input = Prompt.ask("\nEnter command")

                if command_input.strip().lower() == "docs" and step_data.get("doc_quote"):
                    console.print(Panel(step_data["doc_quote"], title="Documentation Quote", border_style="grey70"))
                    continue # Re-prompt for the actual command

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
