from decimal import Decimal
import os
from tkinter import commondialog
from xmlrpc.client import Boolean
from rich import print
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, update, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from turtle import window_height
from datetime import date

# rich console
console = Console()

# # # ###########################################
# # Do not touch!
# # Database Connection stuff!
# Erzeugen einer neuen Datenbank Engine
database = create_engine("sqlite:///ToDo.db")
# Basisklasse für Klassen
Base = declarative_base()

# Öffne Verbindung zur Datenbank
Session = sessionmaker(bind=database)
# Offene Verbindung zur Datenbank
session = Session()
# # # ###########################################


class ToDo(Base):
    __tablename__ = "ToDos"

    id = Column(Integer, primary_key=True)
    todo = Column(String)
    todo_detail = Column(String)
    due_date = Column(String)
    done = Column(Boolean)


def initialize_database():
    """
    Initializes the database and creates all tables.

    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Base.metadata.create_all(database)


def add_todo():

    print('''
    Add a new ToDo
    ''')
    
    new_todo = ToDo()
    new_todo.todo = input("ToDo - Name \t: ")
    new_todo.todo_detail = input("Details (single line) \t:")
    new_todo.due_date = input("Due-Date (YYYYMMDD) \t:")
    new_todo.done = False
    # new_todo.done = 0

    db_add_todo(new_todo)   


def del_todo():

    print('''
    select and delete todo
    ''')

    delId = ""
    delId = input("Which id do you want to delete? \n(Leave blank for none) : ")
    if delId:
        db_del_todo(str(delId))


def mark_done():

    print('''
    check one todo - mark done
    ''')

    print_table(session.query(ToDo).filter_by(done=False))
    todo_id = input("Which ID do you want to mark as done? :")

    db_mark_done(todo_id)

def list_todo_today():

    print('''
    ToDos that are due today
    ''')

    db_list_today()

def list_todo_due():

    print('''
    list ToDos that are open
    ''')

    db_list_due()

def print_table(items: list):
    '''
    print table (items)
    '''

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("id", style='dim')
    table.add_column("ToDo")
    table.add_column("ToDo-Details")
    table.add_column("Due-Date")
    table.add_column("Done")

    for item in items:
        table.add_row(str(item.id),item.todo,item.todo_detail,item.due_date,str(item.done))
    console.print(table)

    # return(table)


def db_add_todo(todo: ToDo):
    """
    Database command to add a new ToDo.
    """
    session.add(todo)
    # ORM - Object Relational Mapper 
    session.commit()


def db_del_todo(id: int):
    """
    DB list all and delete record
    """

    delItem = session.get(ToDo, id)
    session.delete(delItem)
    session.commit()
    # session.query.filter(User.id == 123).delete()

def db_mark_done(todo_id: int):
    '''
    mark ToDo as done
    '''
    my_todo = session.query(ToDo).filter(ToDo.id == todo_id).one()
    my_todo.done = 1
    session.commit()

def db_list_todos():
    """
    Database list all todos.
    """
    print_table(session.query(ToDo).all())
    

def db_list_today():
    """
    Database command to list todos due today.
    """
    today = date.today().strftime('%Y%m%d')

    print_table(session.query(ToDo).filter_by(due_date=today,done=False))

def db_list_due():
    """
    Database command to list open todos.
    """
    print_table(session.query(ToDo).filter_by(done=False).all())
    
def getUserInput():
    print('''
    What do you want to do ?

    (a)dd ToDo
    (d)elete ToDo
    (m)ark ToDo as done
    List (o)pen ToDos
    List ToDos due (t)oday
    (e)xit    
    
    ''')

    userInput = input()
    userInput = userInput.lower()

    return(userInput)

# # # ###########################################
# # # Main
# # # ###########################################
if __name__ == "__main__":

    initialize_database()
    os.system('cls||clear')

    while True:

        userInput = getUserInput()

        match userInput:
            case 'e':
                exit(1)

            case 'a':
                os.system('cls||clear')
                add_todo() 

            case 'd':
                os.system('cls||clear')
                db_list_todos()
                del_todo()
            
            case 'm':
                os.system('cls||clear')
                mark_done()

            case 'o':
                os.system('cls||clear')
                list_todo_due()
            
            case 't':
                os.system('cls||clear')
                list_todo_today()
