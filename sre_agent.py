import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from functions.check_disk_usage import check_disk_usage
from functions.read_system_log import read_system_log
from functions.list_docker_containers import list_docker_containers

# --- CONFIGURATION & SETUP ---
load_dotenv()
console = Console()

# 1. SAFETY CHECK: Ensure we have an API Key
if not os.getenv("GEMINI_API_KEY"):
    console.print("[bold red]❌ Error:[/bold red] GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# --- AGENT SETUP ---

tools_list = [read_system_log, check_disk_usage, list_docker_containers]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash', 
    tools=tools_list,
    system_instruction=(
        "You are a Senior Linux SRE. "
        "When you analyze logs, be concise and look for 'ERROR' or 'WARN'. "
        "If the user asks for a fix, provide a bash command wrapped in backticks."
    )
)

# --- MAIN LOOP (The "UI") ---

def run_agent():
    console.print(Panel.fit("[bold cyan]Auto-SRE Agent[/bold cyan] v2.0", border_style="cyan"))
    
    chat = model.start_chat(enable_automatic_function_calling=True)

    while True:
        try:
            user_input = console.input("\n[bold green]User (You):[/bold green] ")
            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Shutting down...[/yellow]")
                break
            
            # Show a spinner while the agent thinks
            with console.status("[bold yellow]Agent is diagnosing...[/bold yellow]", spinner="dots"):
                response = chat.send_message(user_input)
            
            # Print the response nicely formatted
            console.print("\n[bold purple]🤖 Agent Report:[/bold purple]")
            console.print(Markdown(response.text))
            
        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    # Check for sudo only if we really need it, but warn the user
    if os.geteuid() != 0:
        console.print("[dim italic]Note: Run with 'sudo' if you need deep system logs.[/dim italic]")
    
    run_agent()