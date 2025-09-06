# src/main.py
"""
The main entry point for the AI Ops Simulator tutorials.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.panel import Panel

# Import prompt_toolkit components
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory


from src.commands import CommandHandler
from src.tutorial_manager import TutorialManager # Import the new TutorialManager

console = Console()

def main():
    """Initializes the tutorial system and starts the main loop."""
    console.print("[bold green]Welcome to the AI Ops Simulator Tutorials![/bold green]")
    console.print("Learn about AI Ops concepts through interactive command-line exercises.")
    console.print("\nType [bold yellow]tutorial[/bold yellow] to see available tutorials, or [bold yellow]help[/bold yellow] for a list of all commands.")

    tutorial_manager = TutorialManager() # Initialize TutorialManager
    command_handler = CommandHandler(tutorial_manager) # Pass it to CommandHandler

    history = InMemoryHistory() # Initialize command history

    while True:
        try:
            if tutorial_manager.active_tutorial:
                step_data = tutorial_manager.active_tutorial["steps"][tutorial_manager.tutorial_step]
                prompt_text = step_data["text"]
                console.print(f"\n[bold cyan]TUTORIAL:[/bold cyan] {prompt_text}")
                
                doc_prompt = ""
                if step_data.get("doc_link"):
                    doc_prompt += f"[dim]For more info, see:[/dim] [link={step_data['doc_link']}]{step_data['doc_link']}[/link]"
                if step_data.get("doc_quote"):
                    doc_prompt += " [dim](Type [bold]docs[/bold] to see a quote)[/dim]"
                if doc_prompt:
                    console.print(doc_prompt)

                command_input = prompt("\nEnter command: ", history=history)

                if command_input.strip().lower() == "docs" and step_data.get("doc_quote"):
                    console.print(Panel(step_data["doc_quote"], title="Documentation Quote", border_style="grey70"))
                    continue # Re-prompt for the actual command

                if tutorial_manager.check_tutorial_input(command_input):
                    command_handler.execute(command_input)
                    tutorial_manager.advance_tutorial()
                    if not tutorial_manager.active_tutorial: # Tutorial just ended
                        console.print("[bold green]Tutorial complete! Select another tutorial to continue learning.[/bold green]")
                else:
                    console.print("[bold red]That's not the right command. Try following the instructions carefully.[/bold red]")
            else:
                # If no tutorial is active, just prompt for commands
                command_input = prompt("\nEnter command: ", history=history)
                command_handler.execute(command_input)

        except EOFError: # Ctrl+D or end of input stream
            console.print("\n[bold blue]Exiting tutorials. Goodbye![/bold blue]")
            break
        except KeyboardInterrupt: # Ctrl+C
            console.print("\n[bold yellow]Operation cancelled. Returning to prompt.[/bold yellow]")
            # If a tutorial is active, we might want to reset the step or just stay at the current step.
            # For now, just return to the prompt.
            continue # Continue the loop to show the prompt again
        except SystemExit: # For the 'exit' command
            break

if __name__ == "__main__":
    main()
