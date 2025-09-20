# src/main.py
"""
The main entry point for the AI Ops Simulator tutorials.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from src.commands.base_command import CommandExecutor, BaseCommand
from src.commands import get_command_handlers
from src.tutorial_manager import TutorialManager

console = Console()

def main():
    """Initializes the tutorial system and starts the main loop."""
    console.print("[bold green]Welcome to the AI Ops Simulator Tutorials![/bold green]")
    console.print("Learn about AI Ops concepts through interactive command-line exercises.")
    console.print("Type [bold yellow]tutorial list[/bold yellow] to see available tutorials, or [bold yellow]help[/bold yellow] for a list of all commands.")

    tutorial_manager = TutorialManager()
    command_executor = CommandExecutor(tutorial_manager, get_command_handlers(tutorial_manager))
    history = InMemoryHistory()

    while True:
        try:
            if tutorial_manager.active_tutorial:
                tutorial_id = tutorial_manager.get_active_tutorial_id()
                prompt_parts = [('bold cyan', f'\n({tutorial_id}) '), ('', 'Enter command: ')]
                step_data = tutorial_manager.active_tutorial["steps"][tutorial_manager.tutorial_step]

                if step_data.get("type") == "mcq":
                    console.print(f"\n[bold cyan]QUESTION:[/bold cyan] {step_data['text']}")
                    for answer in step_data['answers']:
                        console.print(answer)
                    
                    answer_input = prompt("Enter your answer (a, b, c, etc.): ").strip().lower()
                    if answer_input == step_data['correct_answer']:
                        console.print("[bold green]Correct![/bold green]")
                        tutorial_manager.advance_tutorial()
                    else:
                        console.print("[bold red]Incorrect. Try again.[/bold red]")
                    continue

                prompt_text = step_data["text"]
                console.print(f"\n[bold cyan]TUTORIAL:[/bold cyan] {prompt_text}")
                
                doc_prompt = ""
                if step_data.get("doc_link"):
                    doc_prompt += f"[dim]For more info, see:[/dim] [link={step_data['doc_link']}]{step_data['doc_link']}[/link]"
                if step_data.get("doc_quote"):
                    doc_prompt += " [dim](Type [bold]docs[/bold] to see a quote)[/dim]"
                if doc_prompt:
                    console.print(doc_prompt)

                if step_data.get("type") == "mcq":
                    console.print(f"\n[bold cyan]QUESTION:[/bold cyan] {step_data['text']}")
                    for answer in step_data['answers']:
                        console.print(answer)
                    
                    answer_input = prompt("Enter your answer (a, b, c, etc.): ").strip().lower()
                    if answer_input == step_data['correct_answer']:
                        console.print("[bold green]Correct![/bold green]")
                        if step_data.get("final_step"):
                            console.print(f"[bold green]{step_data.get('final_message', '')}[/bold green]")
                            tutorial_manager.end_tutorial()
                            console.print("[bold green]Tutorial complete! Select another tutorial to continue learning.[/bold green]")
                        else:
                            tutorial_manager.advance_tutorial()
                    else:
                        console.print("[bold red]Incorrect. Try again.[/bold red]")
                    continue

                command_input = prompt(prompt_parts, history=history)
                command_executor.execute(command_input)

                if tutorial_manager.active_tutorial and step_data.get("final_step"):
                    console.print(f"[bold green]{step_data.get('final_message', '')}[/bold green]")
                    tutorial_manager.end_tutorial()
                    console.print("[bold green]Tutorial complete! Select another tutorial to continue learning.[/bold green]")
                    continue
                
                tutorial_manager.advance_tutorial()
            else:
                command_input = prompt("\nEnter command: ", history=history)
                command_executor.execute(command_input)

        except EOFError:
            console.print("\n[bold blue]Exiting tutorials. Goodbye![/bold blue]")
            break
        except KeyboardInterrupt:
            console.print("\n[bold yellow]Operation cancelled. Returning to prompt. To quit, type `exit`.[/bold yellow]")
            continue
        except SystemExit:
            console.print("\n[bold blue]Exiting tutorials. Goodbye![/bold blue]")
            break

if __name__ == "__main__":
    main()