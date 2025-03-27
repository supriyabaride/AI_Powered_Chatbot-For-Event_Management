# AI_Powered_Chatbot-For-Event_Management
Developed an NLP-based chatbot to automate event-related queries and registration processes.  Implemented database connectivity for dynamic event management and enhanced user experience.  Integrated sentiment analysis to classify user queries and provide relevant event recommendations.
Developed an intelligent ChatBot using NLP and Machine Learning to automate event-related queries and registration. Integrated with a database 
for event management. 
* Admin Panel : allow organizers to add events along with their details, 
* User interface : enables to view a list of upcoming events with relevant details ,enhancing accessibility and engagement.

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

