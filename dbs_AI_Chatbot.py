import nltk
import re
import random
import mysql.connector
from nltk.chat.util import Chat, reflections

# Initialize the NLTK chatbot
responses = [
    (r"hi|hello|hey", ["Hello!", "Hey there!", "Hi!"]),
    (r"department events", ["Our department events include workshops, seminars, and guest lectures."]),
    (r"sports events", ["We have various sports events like cricket, football, and basketball."]),
    (r"cultural events", ["Our cultural events feature music concerts, dance performances, and art exhibitions."]),
    (r"exit|quit", ["Goodbye!", "Bye!", "See you later!"]),
    (r".*", ["I'm not sure I understand.", "Could you please rephrase that?", "I'm sorry, I didn't get that."]),
]

# Passwords
developer_password = "developer123"
customer_password = "customer123"

def fetch_events(event_type):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT description, link FROM events WHERE event_type=%s", (event_type,))
    events = cursor.fetchall()
    conn.close()
    return events

def add_event(event_type, description, link):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (event_type, description, link) VALUES (%s, %s, %s)", (event_type, description, link))
    conn.commit()
    conn.close()

def update_event(event_id, description, link):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET description=%s, link=%s WHERE id=%s", (description, link, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE id=%s", (event_id,))
    conn.commit()
    conn.close()
def add_event_from_developer():
    print("Adding a new event...")
    password = input("Enter developer password: ")
    if password != developer_password:
        print("Incorrect password! Access denied.")
        return
    event_type = input("Enter event type (department events/sports events/cultural events): ")
    description = input("Enter event description: ")
    link = input("Enter event link: ")
    
    # Add the event
    add_event(event_type, description, link)
    
    # Prompt to add location
    add_location_option = input("Do you want to add a location to this event? (yes/no): ")
    if add_location_option.lower() == 'yes':
        location_name = input("Enter location name: ")
        address = input("Enter location address: ")
        
        # Add the location
        location_id = add_location(location_name, address)
        
        # Get the ID of the last inserted event
        event_id = get_last_inserted_event_id()
        
        # Associate the location with the event
        associate_location_with_event(event_id, location_id)
        
        print("Location added successfully!")
    
    print("Event added successfully!")

def get_last_inserted_event_id():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT LAST_INSERT_ID()")
    event_id = cursor.fetchone()[0]
    conn.close()
    return event_id

def associate_location_with_event(event_id, location_name):
    conn = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_username",
        password="your_mysql_password",
        database="your_mysql_database"
    )
    cursor = conn.cursor()

    # Get the location ID based on the location name
    cursor.execute("SELECT id FROM locations WHERE location_name = %s", (location_name,))
    location_result = cursor.fetchone()
    if location_result:
        location_id = location_result[0]
    else:
        print("Location not found.")
        return

    # Update the event record with the location ID
    cursor.execute("UPDATE events SET location_id = %s WHERE event_id = %s", (location_id, event_id))
    conn.commit()
    conn.close()


def add_location(location_name, address):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET location_id=%s WHERE event_id=%s", (id, event_id))

    conn.commit()
    location_id = cursor.lastrowid
    conn.close()
    return location_id


def update_event_from_developer():
    print("Updating an existing event...")
    password = input("Enter developer password: ")
    if password != developer_password:
        print("Incorrect password! Access denied.")
        return
    event_type = input("Enter event type to update (department events/sports events/cultural events): ")
    if event_type.lower() not in ['department events', 'sports events', 'cultural events']:
        print("Invalid event type.")
        return
    event_id = input("Enter event ID: ")
    description = input("Enter updated event description: ")
    link = input("Enter updated event link: ")
    update_event(event_id, description, link)
    print("Event updated successfully!")


def delete_event_from_developer():
    print("Deleting an existing event...")
    password = input("Enter developer password: ")
    if password != developer_password:
        print("Incorrect password! Access denied.")
        return
    event_type = input("Enter event type to delete (department events/sports events/cultural events): ")
    if event_type.lower() not in ['department events', 'sports events', 'cultural events']:
        print("Invalid event type.")
        return
    event_id = input("Enter event ID: ")
    delete_event(event_id)
    print("Event deleted successfully!")

def add_attendee(event_id, attendee_name, attendee_email, location_id=None):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql2024!",
        database="your_mysql_database"
    )
    cursor = conn.cursor()
    if location_id is not None:
        cursor.execute("INSERT INTO attendees (event_id, attendee_name, attendee_email, location_id) VALUES (%s, %s, %s, %s)", (event_id, attendee_name, attendee_email, location_id))
    else:
        cursor.execute("INSERT INTO attendees (event_id, attendee_name, attendee_email) VALUES (%s, %s, %s)", (event_id, attendee_name, attendee_email))
    conn.commit()
    conn.close()



def event_chatbot():
    print("Hi! I'm the Event Management Chatbot. How can I help you today?")
    chatbot = Chat(responses, reflections)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print(random.choice(responses[-2][1]))  # Randomly select from exit responses
            break
        elif user_input.lower() in ['department events', 'sports events', 'cultural events']:
            event_type = user_input.lower()
            events = fetch_events(event_type)
            if events:
                print("Bot: Here are the", event_type, ":")
                for event in events:
                    print("-", event[0], "Link:", event[1])
                
                interested_event = input("Which event are you interested in? Enter the event ID: ")
                attendee_name = input("Enter your name: ")
                attendee_email = input("Enter your email: ")
                add_attendee(interested_event, attendee_name, attendee_email)
                print("You have been added as an attendee to the event!")
            else:
                print("Bot: Sorry, I couldn't find any events of that type.")
        elif user_input.lower() == 'add event':
            add_event_from_developer()
        elif user_input.lower() == 'update event':
            update_event_from_developer()
        elif user_input.lower() == 'delete event':
            delete_event_from_developer()
        else:
            print("Bot:", chatbot.respond(user_input))


if __name__ == "__main__":
    event_chatbot()
