import os
import subprocess

from collections.abc import Sequence

from rich.console import Console
from rich.table import Table

from simple_term_menu import TerminalMenu
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


TEXT_WELCOME_MESSAGE = """

  ______    _                _ _                 _    
 |  ____|  (_)              | | |               | |   
 | |__ _ __ _  ___ _ __   __| | |__   ___   ___ | | __
 |  __| '__| |/ _ \ '_ \ / _` | '_ \ / _ \ / _ \| |/ /
 | |  | |  | |  __/ | | | (_| | |_) | (_) | (_) |   < 
 |_|  |_|  |_|\___|_| |_|\__,_|_.__/ \___/ \___/|_|\_\\
                                                      
######################################################

Welcome to your Friendbook!

You can add new friends and search for them. 

"""

console = Console()

database = create_engine("sqlite:///:memory:",  echo=False)
Base = declarative_base()

Session = sessionmaker(bind=database)
session = Session()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
    def __repr__(self) -> str:
        return f"<User(first_name='{self.first_name}, last_name={self.last_name})>"


def initialize_database():
    """
    Initializes the database and creates all tables.

    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Base.metadata.create_all(database)
    subprocess.run(["clear"])
 

def print_welcome_message(): 
    """
    Welcome message to the user. 
    """
    console.print(TEXT_WELCOME_MESSAGE, style="bold red")


def display_fiends_table(users: Sequence[User]):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("First Name")
    table.add_column("Last Name")

    for user in users:
        table.add_row(str(user.id), user.first_name, user.last_name)

    console.print(table)


def option_add_friend():
    """
    Option (A): Add a new friend. 
    """
    print("\nAdd a new friend:")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    user = User(first_name=first_name, last_name=last_name)
    session.add(user)
    console.print("Friend added!\n", style="bold green")


def option_list_all_friends():
    """
    Option (L): List all friends. 
    """
    all_users = session.query(User).all()
    display_fiends_table(all_users)
    

def option_exit():
    """
    Option (E): The user want's to exit the program. 
    """
    console.print("\nThanks for usage. See you.\n", style="bold red")
    exit(1)


def main():
    """
    Main function where the menu is shown. 
    """
    options_list = [
        "(S)earch for friend", 
        "(A)dd friend", 
        "(L)ist all friends",
        "(E)xit"
    ]
    
    function_map = [
        None, 
        option_add_friend, 
        option_list_all_friends, 
        option_exit
    ] 

    # Show the menu and ask for entry
    terminal_menu = TerminalMenu(options_list)
    print("")
    menu_entry_index = terminal_menu.show()
    print("")

    # Run the function from function_map
    function_map[menu_entry_index]()


if __name__ == "__main__":
    initialize_database()
    print_welcome_message()

    while True:
        main()