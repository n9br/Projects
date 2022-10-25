from decimal import Decimal
from turtle import window_height
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker


# # # ###########################################
# # Do not touch!
# # Database Connection stuff!
# Erzeugen einer neuen Datenbank Engine
database = create_engine("sqlite:///Friends.db")
# Basisklasse für Klassen
Base = declarative_base()

# Öffne Verbindung zur Datenbank
Session = sessionmaker(bind=database)
# Offene Verbindung zur Datenbank
session = Session()
# # # ###########################################


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_nr = Column(String)
    nick_name = Column(String)
    address = Column(String)
    birthday = Column(String)
    email = Column(String)

    # Foreignkeys
    language_id = Column(Integer, ForeignKey("languages.id"))
    bike_id = Column(Integer, ForeignKey("bikes.id"))

class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    tyre_width = Column(Integer)
    weight = Column(Integer)
    gears = Column(Integer)
    brand = Column(String)
    model = Column(String)

def initialize_database():
    """
    Initializes the database and creates all tables.

    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Base.metadata.create_all(database)


def database_add_friend(friend: Friend):
    """
    Database command to add a new friend.
    """
    session.add(friend)
    session.commit()

def database_get_all_friends():
    """
    Database command to get all friends.
    """
    all_friends = session.query(Friend).all()
    print(all_friends)

def add_friends():
    """
    Freunde eingeben
    """
    addingFriends = True

    while addingFriends:
        new_friend = Friend()

        new_friend.first_name = input("Name \t: ")
        new_friend.last_name = input("Surname \t:")
        new_friend.phone_nr = input("Phone# \t:")
        new_friend.nick_name = input("Nick \t:")
        new_friend.address = input("Address \t:")
        new_friend.birthday = input("BDay \t:")
        new_friend.email = input("Email \t:")
        addingFriends = input("Add more friends? Leave blank to not.")

    # new_friend = Friend(first_name = "Robert", last_name = "Kozljanic", phone_nr = "0157 24 88 357", nick_name = "Roberto", 
    #    address = "MUC", birthday = "30.3.1970", email = "roberto@gmail.com")

    database_add_friend(new_friend)
    


# # # ###########################################
# # # Main
# # # ###########################################
if __name__ == "__main__":
    initialize_database()

    # add friens
    add_friends() 

    # Example to list all friends
    database_get_all_friends()