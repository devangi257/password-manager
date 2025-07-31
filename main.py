import os
import json
import csv
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from rich.table import Table

console = Console()

FOLDER_NAME = "password_data"
FILE_PATH = os.path.join(FOLDER_NAME, "passwords.json")

# ----------------- Greeting -----------------
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "🌅 Good Morning!"
    elif 12 <= hour < 17:
        return "🌞 Good Afternoon!"
    elif 17 <= hour < 21:
        return "🌇 Good Evening!"
    else:
        return "🌙 Good Night!"

# ----------------- File Handling -----------------
def load_data():
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({}, f)
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ----------------- Features -----------------
def add_entry(data):
    console.rule("[bold green]Add New Entry")
    account = Prompt.ask("🔹 Enter account name (e.g., Gmail)")
    username = Prompt.ask("👤 Enter username/email")
    password = Prompt.ask("🔑 Enter password (input visible)")

    data[account] = {
        "username": username,
        "password": password
    }
    save_data(data)
    console.print("✅ [green]Entry added successfully![/green]")

def view_all(data):
    console.rule("[bold cyan]Stored Passwords")
    if not data:
        console.print("[yellow]📭 No entries found.[/yellow]")
        return

    table = Table(title="🔐 Password Vault", show_lines=True)
    table.add_column("Account", style="bold cyan", no_wrap=True)
    table.add_column("Username", style="magenta")
    table.add_column("Password", style="green")

    for acc, info in data.items():
        table.add_row(acc, info['username'], info['password'])

    console.print(table)

def update_entry(data):
    console.rule("[bold yellow]Update Entry")
    acc = Prompt.ask("✏️ Enter account name to update")
    if acc in data:
        new_pass = Prompt.ask("🔁 Enter new password")
        data[acc]["password"] = new_pass
        save_data(data)
        console.print("✅ [green]Password updated![/green]")
    else:
        console.print("❌ [red]Account not found![/red]")

def delete_entry(data):
    console.rule("[bold red]Delete Entry")
    acc = Prompt.ask("🗑️ Enter account to delete")
    if acc in data:
        del data[acc]
        save_data(data)
        console.print("✅ [green]Deleted successfully![/green]")
    else:
        console.print("❌ [red]Account not found![/red]")

def search_entry(data):
    console.rule("[bold blue]Search Entry")
    acc = Prompt.ask("🔍 Enter account to search")
    if acc in data:
        info = data[acc]
        console.print(f"\n[bold]{acc}[/bold]")
        console.print(f"👤 Username: {info['username']}")
        console.print(f"🔑 Password: {info['password']}")
    else:
        console.print("❌ [red]Account not found![/red]")

def export_to_csv(data):
    filename = os.path.join(FOLDER_NAME, "passwords_export.csv")
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Account", "Username", "Password"])
        for acc, info in data.items():
            writer.writerow([acc, info['username'], info['password']])
    console.print(f"✅ [green]Exported to {filename}[/green]")

def get_password_input(prompt):
    return input(prompt)

# ----------------- Main -----------------
def main():
    data = load_data()
    console.clear()

    # Greeting Panel
    greeting = get_greeting()
    welcome_text = f"[bold cyan]{greeting}[/bold cyan]\n\n[bold white]🔐 Welcome to Password Manager[/bold white]\n[green]By Devangi Khatri[/green]"
    panel = Panel(
        Align.center(welcome_text, vertical="middle"),
        title="[bold magenta]👋 Hello![/bold magenta]",
        border_style="magenta",
        padding=(1, 4),
        expand=False
    )
    console.print(panel, justify="center")

    # Password Authentication
    master = get_password_input("🔑 Enter Master Password: ")
    if master != "admin123":
        console.print("❌ [red]Incorrect master password![/red]")
        return

    # Menu Loop
    while True:
        console.rule("[bold cyan]Main Menu")
        console.print("[bold]1.[/bold] Add Password")
        console.print("[bold]2.[/bold] View All Passwords")
        console.print("[bold]3.[/bold] Update Password")
        console.print("[bold]4.[/bold] Delete Account")
        console.print("[bold]5.[/bold] Search Account")
        console.print("[bold]6.[/bold] Export to CSV")
        console.print("[bold]7.[/bold] Exit")

        choice = Prompt.ask("➡️ Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"])

        if choice == "1":
            add_entry(data)
        elif choice == "2":
            view_all(data)
        elif choice == "3":
            update_entry(data)
        elif choice == "4":
            delete_entry(data)
        elif choice == "5":
            search_entry(data)
        elif choice == "6":
            export_to_csv(data)
        elif choice == "7":
            console.print("👋 [green]Thank you for using Password Manager![/green]")
            break

# ----------------- Run -----------------
if __name__ == "__main__":
    main()
