import subprocess
import pyttsx3
import numpy as np
import speech_recognition as sr
import numpy as np
import speech_recognition as sr
import pyaudio
import datetime
import random
from plyer import notification
import wikipedia
import logging
import pywhatkit
from googlesearch import search
import webbrowser
import os
import time
import imaplib
import threading
import pyautogui
import os.path
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import winshell
import pyjokes
import requests
import pint
import shutil
import ctypes
import cv2
import smtplib
from urllib.request import urlopen
import logging
import json
import datetime
import email
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from email.header import decode_header
from datetime import datetime
from datetime import timedelta
import speech_recognition as sr
import numpy as np
import noisereduce as nr
import phonenumbers
from phonenumbers import geocoder, carrier, PhoneNumberType



# Configure logging
logging.basicConfig(filename='assistant.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
pa = pyaudio.PyAudio()
engine.setProperty('voice', voices[1].id)
ureg = pint.UnitRegistry()
EVENTS_FILE = 'events.json' #EVENT FILE_PATH FOR JSON
translator = Translator()
file_path = 'stock_price.json' #JSON FILE_PATH
prompt = "please type data as instruction"

#DEFINED EXCHANGE RATE 
exchange_rates = {
    'USD': 1.0,
    'EUR': 0.9,
    'GBP': 0.8,
    'INR': 74.0,
    'DZD': 135.0,
    'BND': 1.36,
    'JPY': 145.0,
    'CAD': 1.35,
    'AUD': 1.45,
    'CNY': 7.0,
    'CHF': 0.92
}

#FUNCTION FOR GET USER INPUT 
def get_user_input():
    return input(prompt)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
#FUNCTION FOR DEFINE LAUGH    
def laugh():
    engine = pyttsx3.init()
    engine.say("Ha ha ha!")
    engine.runAndWait()    

#FUNCTION FOR ADVANCED NOICE CANCELLETION
def noise_cancellation(audio_data, sample_rate):
    # Convert the byte data to numpy array
    audio_np = np.frombuffer(audio_data, dtype=np.int16)
    
    # Perform noise reduction (try reducing the intensity if needed)
    reduced_noise = nr.reduce_noise(y=audio_np, sr=sample_rate, prop_decrease=0.8)
    
    # Convert the reduced noise numpy array back to bytes
    return reduced_noise.tobytes()

#FUNCTION FOR TAKECOMMAND
def takeCommand():
    r = sr.Recognizer()
    
    with sr.Microphone(sample_rate=16000) as source:
        # Adjust for ambient noise (increase duration if needed)
        r.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        
        # Capture audio data
        audio_data = r.listen(source)
        
        # Convert the recorded audio data to bytes
        audio_bytes = audio_data.get_raw_data()
        
        # Apply noise cancellation
        filtered_audio = noise_cancellation(audio_bytes, sample_rate=16000)
        
        if filtered_audio:
            audio = sr.AudioData(filtered_audio, sample_rate=16000, sample_width=2)
        else:
            print("No speech detected, please speak again.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please say that again.")
        return "None"
    except sr.RequestError as e:
        print("Sorry, I couldn't reach the recognition service.")
        return "None"

#function FOR CONVERSION
def perform_conversion():
    value = float(takeCommand()("Please type the value you want to convert: "))
    # Continue with your conversion logic

def convert_units(value, from_unit, to_unit):
    try:
        # Parse the input value and units
        quantity = value * ureg(from_unit)
        # Convert to the desired unit
        converted_quantity = quantity.to(to_unit)
        return converted_quantity
    except Exception as e:
        return str(e)

#WISHING FUNCTION
def wishMe():
    hour = int(datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    speak("I am your Assistant")
    speak(assname)

#DEFININMG USER NAME 
def username():
    speak("What should I call you, sir?")
    uname = takeCommand().strip().capitalize()
    if uname.lower() == "arya":
        welcome_message = "Welcome Boss!"
        speak("Welcome Boss!")
    else:
        welcome_message = f"Welcome Mister {uname}"
        speak(f"Welcome Mister {uname}")
        
    columns = shutil.get_terminal_size().columns
    
    print("#####################".center(columns))
    print(f"Welcome Mr. {uname}".center(columns))
    print("#####################".center(columns))
    
    speak("How can I help you, sir?")
    return uname

#function for emailsender with Smtp server if you want to use Smtp server first you have to create with your email provider
def sendEmail(to, content):
    try:
        # Email account credentials (use environment variables for better security)
        email_user = os.getenv('ENTER YOUR EMAIL HERE')
        email_password = os.getenv('ENTER YOUR PASSWORD')
        
        if not email_user or not email_password:
            raise ValueError("Email credentials are not set.")
        
        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = to
        msg['Subject'] = 'Subject of the Email'
        
        # Attach the email content
        msg.attach(MIMEText(content, 'plain'))
        
        # Connect to the server (Which You have create before)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
        server.close()
        
        speak("Email has been sent successfully!")
    
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        speak("I am not able to send this email. Please try again later.")
         # Email account credentials

#function for read emails         
def read_emails():
    print("Reading emails")
    speak("Reading emails")

    # Email account credentials
    username = os.getenv('Enter your email here')
    password = os.getenv('Enter your password')
    
    if not username or not password:
        print("Email credentials are not set.")
        speak("Email credentials are not set.")
        return

    try:
        # Connect to the Gmail IMAP server
        mail = imaplib.IMAP4_SSL('imap.gmail.com')

        # Log in to the email account
        mail.login(username, password)

        # Select the mailbox you want to check (e.g., inbox)
        mail.select('inbox')

        # Search for all emails in the inbox
        status, messages = mail.search(None, 'ALL')

        # Convert messages to a list of email IDs
        email_ids = messages[0].split()

        if not email_ids:
            speak("No emails found.")
            return 

        # Fetch the latest email
        latest_email_id = email_ids[-1]

        # Fetch the email by ID
        status, msg_data = mail.fetch(latest_email_id, '(RFC822)')

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = decode_header(msg['subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                print(f'Subject: {subject}')
                speak(f'Subject: {subject}')

                # Fetch the email content
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                print(f'Body: {body}')
                                speak(f'Body: {body}')
                        except Exception as e:
                            print(f"Error decoding part: {e}")
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f'Body: {body}')
                    speak(f'Body: {body}')

    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
        speak("An error occurred while accessing the email server.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("An unexpected error occurred.")

    finally:
        try:
            # Log out and close the connection
            mail.logout()
        except:
            pass

#Function for Set a alarm     
def set_alarm(alarm_time):
    print(f"Setting alarm for {alarm_time}") 
    now = datetime.datetime.now()
    alarm_time = datetime.datetime.strptime(alarm_time, "%H:%M:%S").replace(year=now.year, month=now.month, day=now.day)  
    if alarm_time < now:
        print("The specified time is in the past. Please set a future time.")
        return
    
    time_diff = (alarm_time - now).total_seconds()
    
    def trigger_alarm():
        print("Alarm ringing! Time to wake up!")
    
    threading.Timer(time_diff, trigger_alarm).start()

#function for get weather repor without api   
def get_weather(city_name):
    url = f"https://wttr.in/{city_name}?format=%t+%w+%h+%c"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return "Unable to get weather data."
    except Exception as e:
        return f"An error occurred: {e}"

#Some functions for events load , add , save and upcoming , delete events 
def load_events():
    try:
        with open(EVENTS_FILE, 'r') as file:
            events = json.load(file)
    except FileNotFoundError:
        events = []
    return events

def save_events(events):
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events, file, indent=4)

def validate_datetime(dt_str):
    try:
        return datetime.fromisoformat(dt_str)
    except ValueError:
        return None

def add_event(summary, start_time, end_time):
    events = load_events()
    start_dt = validate_datetime(start_time)
    end_dt = validate_datetime(end_time)
    if start_dt is None or end_dt is None:
        return "Invalid date/time format. Please use 'YYYY-MM-DDTHH:MM:SS'."
    event = {
        'summary': summary,
        'start_time': start_time,
        'end_time': end_time
    }
    events.append(event)
    save_events(events)
    return "Event added."

def get_upcoming_events():
    events = load_events()
    if not events:
        return "No upcoming events found."
    events.sort(key=lambda x: x['start_time'])
    event_list = []
    for event in events:
        event_list.append(f"{event['start_time']} to {event['end_time']}: {event['summary']}")
    return '\n'.join(event_list)

def delete_event(summary):
    events = load_events()
    events = [event for event in events if event['summary'] != summary]
    save_events(events)
    return "Event deleted."

#function for capturing photo by camera 
def capture_photo(filename='photo.jpg'):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Camera not found.")
        return
    ret, frame = camera.read()
    if ret:
        cv2.imwrite(filename, frame)
        print(f"Photo saved as {filename}.")
    else:
        print("Error: Could not capture photo.")
    camera.release()
    cv2.destroyAllWindows()

#Function for capturing screenshot
def capture_screenshot(filename='screenshot.png'):
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}.")

#Some Functions for reminder
def remind(reminder_text):
    print(f"Reminder: {reminder_text}")

# Function to set a reminder
def set_reminder_at(reminder_time, reminder_text):
    try:
        # Parse the reminder_time to datetime object
        reminder_datetime = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")

        # Calculate the difference between now and the reminder time
        now = datetime.now()
        time_difference = (reminder_datetime - now).total_seconds()

        if time_difference <= 0:
            return "The reminder time must be in the future."

        # Schedule the reminder in a separate thread
        def schedule_reminder():
            time.sleep(time_difference)
            remind(reminder_text)

        reminder_thread = threading.Thread(target=schedule_reminder)
        reminder_thread.start()

        return "Reminder set successfully."

    except ValueError:
        return "Invalid time format. Please use 'YYYY-MM-DD HH:MM:SS' format."

#function for convert minut into seconds
def convert_to_seconds(duration):
    units = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}
    parts = duration.split()
    time_value = int(parts[0])
    time_unit = parts[1].rstrip('s').lower()  # Strip the plural 's' and convert to lowercase
    return time_value * units[time_unit]

#Some functions for parse time , duration , reminder
def parse_time(time_str):
    current_time = datetime.now()
    # Handling common phrases
    if "tomorrow" in time_str:
        time_str = time_str.replace("tomorrow", "").strip()
        target_time = datetime.strptime(time_str, '%I:%M %p') + timedelta(days=1)
    elif "next week" in time_str:
        time_str = time_str.replace("next week", "").strip()
        target_time = datetime.strptime(time_str, '%I:%M %p') + timedelta(weeks=1)
    else:
        try:
            target_time = datetime.strptime(time_str, '%I:%M %p').replace(year=current_time.year, month=current_time.month, day=current_time.day)
        except ValueError:
            try:
                target_time = datetime.strptime(time_str, '%H:%M').replace(year=current_time.year, month=current_time.month, day=current_time.day)
            except ValueError:
                raise ValueError("Invalid time format")

    # Adjust for past times within the same day
    if target_time < current_time:
        target_time += timedelta(days=1)
    return target_time

def parse_duration(query, keyword):
    try:
        if keyword in query:
            return query.split(keyword)[1].split('for')[0].strip()
        return None
    except Exception as e:
        return None

def parse_reminder_text(query):
    try:
        return query.split('for')[1].strip()
    except Exception as e:
        return None

#function for file manegement
def file_management(action, file_path):
    # Placeholder for file management
    return f"File management action: {action} for {file_path}"

#function for get joke
def get_random_joke():
    return pyjokes.get_joke()

#function for fatch trending movies from imdb without api 
def get_trending_movies():
    url = 'https://www.imdb.com/chart/moviemeter/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    except requests.RequestException as e:
        print(f"Error fetching movie data: {e}")
        return "Unable to fetch trending movies at the moment."

    soup = BeautifulSoup(response.text, 'html.parser')
    
    movies = []
    # Fetch only the first 10 movies
    for item in soup.select('.lister-list tr')[:10]:
        title_tag = item.select_one('.titleColumn a')
        year_tag = item.select_one('.titleColumn span')
        
        if title_tag and year_tag:
            title = title_tag.text
            year = year_tag.text.strip('()')
            movies.append(f"{title} ({year})")
    
    if not movies:
        return "No trending movies found."
    
    return '\n'.join(movies)

#function for fatch ternding youtube vedios 
def get_trending_youtube_videos():
    url = 'https://www.youtube.com/feed/trending'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    except requests.RequestException as e:
        print(f"Error fetching YouTube data: {e}")
        return "Unable to fetch trending YouTube videos at the moment."

    soup = BeautifulSoup(response.text, 'html.parser')
    
    videos = []
    # YouTube might have a different structure, so you need to inspect the page
    for item in soup.select('a.yt-simple-endpoint.style-scope.ytd-video-renderer'):
        title = item.get('title')
        if title:
            videos.append(title)
    
    if not videos:
        return "No trending YouTube videos found."
    
    return '\n'.join(videos[:10])  # Fetch only the top 10 videos

#function for get IP adderess
def get_ip_address():
    try:
        response = urlopen('https://api.ipify.org').read()
        return f"Your IP address is: {response.decode('utf-8')}"
    except Exception as e:
        return f"An error occurred: {e}"

#function for searching on youtube
def search_youtube(query):
    pywhatkit.search(query)

#function for searching on google 
def google_search(query):
    if not isinstance(query, str):
        return "Invalid query. Please provide a string."
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    search_url = f'https://www.google.com/search?q={query}'
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first search result
    first_result = soup.find('div', class_='BNeawe s3v9rd AP7Wnd')
    if first_result:
        return first_result.get_text()
    return "No results found."

#function for opening any website from crome 
def open_website(url):
    webbrowser.open(url)
    return f"Opening {url}"

#defination block for translation and select language 
def translate_text(text, dest_language):
    """Translate the input text into the desired language."""
    try:
        if dest_language == 'sa':
            print("Translation to Sanskrit is not supported.")
            speak("Translation to Sanskrit is currently not supported.")
            return None
        else:
            translation = translator.translate(text, dest=dest_language)
            print(f"Translated text: {translation.text}")
            speak(f"Translation: {translation.text}")
            return translation.text
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return None

def select_language():
    """Prompt the user to select a language for translation."""
    print("Select a language for translation:")
    print("1. Hindi (hi)")
    print("2. English (en)")
    print("3. Spanish (es)")
    print("4. French (fr)")
    print("5. German (de)")
    print("6. Sanskrit (sa) - Unsupported")
    
    choice = input("Enter the number corresponding to your choice: ")
    language_codes = {
        "1": "hi",  # Hindi
        "2": "en",  # English
        "3": "es",  # Spanish
        "4": "fr",  # French
        "5": "de",  # German
        "6": "sa"   # Sanskrit (unsupported)
    }
    
    return language_codes.get(choice, "en")  # Default to English if invalid input

# define function for  3 games for fun
def ask_question(question, options, correct_answer):
    """Ask a single question and return True if the answer is correct, otherwise False."""
    print(question)
    for idx, option in enumerate(options):
        print(f"{idx + 1}. {option}")

    try:
        user_choice = int(input("Enter the number of your choice: "))
        if 1 <= user_choice <= len(options):
            answer = options[user_choice - 1]
            if answer == correct_answer:
                print("Correct!")
                return True
            else:
                print(f"Wrong! The correct answer is: {correct_answer}")
                return False
        else:
            print("Invalid choice. Please select a valid option.")
            return ask_question(question, options, correct_answer)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return ask_question(question, options, correct_answer)

def general_knowledge_quiz():
    """Run a general knowledge quiz."""
    questions = [
        {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
        {"question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
        {"question": "Who was the first President of India?", "options": ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Dr. S. Radhakrishnan", "V. V. Giri"], "answer": "Dr. Rajendra Prasad"},
        {"question": "What is the national sport of India?", "options": ["Hockey", "Cricket", "Football", "Kabaddi"], "answer": "Hockey"},
        {"question": "Which river is known as the 'Ganges of the South'?", "options": ["Godavari", "Krishna", "Cauvery", "Yamuna"], "answer": "Godavari"},
        {"question": "Which Indian state is known as the 'Land of Five Rivers'?", "options": ["Punjab", "Haryana", "Uttar Pradesh", "Rajasthan"], "answer": "Punjab"},
        {"question": "Who is the author of the Indian national anthem 'Jana Gana Mana'?", "options": ["Rabindranath Tagore", "Bankim Chandra Chatterjee", "Kavi Pradeep", "Sarojini Naidu"], "answer": "Rabindranath Tagore"},
        {"question": "Which Indian city is known as the 'City of Joy'?", "options": ["Kolkata", "Mumbai", "Delhi", "Chennai"], "answer": "Kolkata"},
        {"question": "Who was the first Indian to win a Nobel Prize?", "options": ["Rabindranath Tagore", "C. V. Raman", "Homi J. Bhabha", "Satyendra Nath Bose"], "answer": "Rabindranath Tagore"},
        {"question": "Which Indian film won the Best Foreign Language Film award at the Oscars in 1958?", "options": ["Mother India", "Gandu", "Pyaasa", "Lagaan"], "answer": "Mother India"},
        {"question": "Who was the leader of the Indian independence movement and is known as the 'Father of the Nation'?", "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Bhagat Singh"], "answer": "Mahatma Gandhi"},
        {"question": "Which Indian state is known for its backwaters and houseboats?", "options": ["Kerala", "Goa", "Karnataka", "Tamil Nadu"], "answer": "Kerala"},
        {"question": "What is the capital of the Indian state of Maharashtra?", "options": ["Mumbai", "Pune", "Nagpur", "Aurangabad"], "answer": "Mumbai"},
        {"question": "Which Indian leader is known for his role in the Quit India Movement of 1942?", "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhas Chandra Bose"], "answer": "Mahatma Gandhi"},
        {"question": "Which Indian festival is known as the 'Festival of Lights'?", "options": ["Diwali", "Holi", "Navratri", "Eid"], "answer": "Diwali"},
        {"question": "What is the official language of India as per the Indian Constitution?", "options": ["Hindi", "English", "Bengali", "Tamil"], "answer": "Hindi"},
        {"question": "Which Indian state is known for its tea gardens and production?", "options": ["Assam", "West Bengal", "Arunachal Pradesh", "Sikkim"], "answer": "Assam"},
        {"question": "Who is the famous Indian cricketer known as the 'Little Master'?", "options": ["Sunil Gavaskar", "Sachin Tendulkar", "Kapil Dev", "Sourav Ganguly"], "answer": "Sunil Gavaskar"},
        {"question": "Which Indian monument is also known as the 'Symbol of Love'?", "options": ["Taj Mahal", "Red Fort", "Qutub Minar", "Gateway of India"], "answer": "Taj Mahal"},
        {"question": "Who was the first woman Prime Minister of India?", "options": ["Indira Gandhi", "Sonia Gandhi", "Pratibha Patil", "Mamata Banerjee"], "answer": "Indira Gandhi"},
        {"question": "Which Indian state is famous for its unique dance form 'Kathakali'?", "options": ["Kerala", "Karnataka", "Odisha", "West Bengal"], "answer": "Kerala"},
        {"question": "Which Indian state is known for the historic city of Hampi?", "options": ["Karnataka", "Andhra Pradesh", "Tamil Nadu", "Telangana"], "answer": "Karnataka"},
        {"question": "Which Indian river is considered sacred and is worshipped by Hindus?", "options": ["Ganges", "Yamuna", "Godavari", "Krishna"], "answer": "Ganges"},
        {"question": "Who wrote the Indian epic 'Mahabharata'?", "options": ["Vyasa", "Valmiki", "Tulsidas", "Kalidasa"], "answer": "Vyasa"}
    ]
    
    score = 0
    random.shuffle(questions)  # Shuffle questions to ensure randomness
    
    for q in questions:
        if ask_question(q["question"], q["options"], q["answer"]):
            score += 1
    
    print(f"Your final score is: {score}/{len(questions)}")
def trivia_challenge():
    """Run a trivia challenge."""
    categories = {
        "Movies": [
            {"question": "Who directed 'Inception'?", "options": ["Christopher Nolan", "Steven Spielberg", "James Cameron", "Martin Scorsese"], "answer": "Christopher Nolan"},
            {"question": "What year was 'The Matrix' released?", "options": ["1999", "2001", "2003", "1997"], "answer": "1999"},
            {"question": "Which movie won the Best Picture Oscar in 2020?", "options": ["Parasite", "1917", "Joker", "Once Upon a Time in Hollywood"], "answer": "Parasite"},
            {"question": "Who played the character of Jack Dawson in 'Titanic'?", "options": ["Leonardo DiCaprio", "Brad Pitt", "Johnny Depp", "Tom Cruise"], "answer": "Leonardo DiCaprio"},
            {"question": "What is the name of the fictional African country in 'Black Panther'?", "options": ["Wakanda", "El Dorado", "Narnia", "Genosha"], "answer": "Wakanda"},
            {"question": "In which movie did Tom Hanks play the character of Forrest Gump?", "options": ["Forrest Gump", "Cast Away", "Saving Private Ryan", "Apollo 13"], "answer": "Forrest Gump"},
            {"question": "What is the highest-grossing film of all time?", "options": ["Avatar", "Avengers: Endgame", "Titanic", "The Lion King"], "answer": "Avengers: Endgame"},
            {"question": "Who directed 'Pulp Fiction'?", "options": ["Quentin Tarantino", "Martin Scorsese", "Francis Ford Coppola", "Ridley Scott"], "answer": "Quentin Tarantino"},
            {"question": "Which movie features the famous line 'Here's looking at you, kid'?", "options": ["Casablanca", "Gone with the Wind", "The Godfather", "Citizen Kane"], "answer": "Casablanca"},
            {"question": "Who won the Academy Award for Best Actress in 2021?", "options": ["Frances McDormand", "Viola Davis", "Andra Day", "Carey Mulligan"], "answer": "Frances McDormand"}
        ],
        "Science": [
            {"question": "What is the chemical symbol for water?", "options": ["H2O", "O2", "CO2", "NaCl"], "answer": "H2O"},
            {"question": "What planet is known as the 'Gas Giant'?", "options": ["Mars", "Jupiter", "Saturn", "Uranus"], "answer": "Jupiter"},
            {"question": "What is the hardest natural substance on Earth?", "options": ["Diamond", "Gold", "Iron", "Platinum"], "answer": "Diamond"},
            {"question": "What part of the cell contains genetic material?", "options": ["Nucleus", "Mitochondria", "Cytoplasm", "Cell membrane"], "answer": "Nucleus"},
            {"question": "Which element is essential for human respiration?", "options": ["Oxygen", "Hydrogen", "Carbon", "Nitrogen"], "answer": "Oxygen"},
            {"question": "What is the smallest unit of life?", "options": ["Cell", "Atom", "Molecule", "Organ"], "answer": "Cell"},
            {"question": "Who is known as the father of modern physics?", "options": ["Isaac Newton", "Albert Einstein", "Niels Bohr", "Galileo Galilei"], "answer": "Albert Einstein"},
            {"question": "What is the chemical symbol for gold?", "options": ["Au", "Ag", "Pb", "Fe"], "answer": "Au"},
            {"question": "Which planet is closest to the Sun?", "options": ["Mercury", "Venus", "Earth", "Mars"], "answer": "Mercury"},
            {"question": "What gas do plants primarily use for photosynthesis?", "options": ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"}
        ],
        "Geography": [
            {"question": "What is the capital of France?", "options": ["Paris", "London", "Berlin", "Madrid"], "answer": "Paris"},
            {"question": "Which river is the longest in the world?", "options": ["Nile", "Amazon", "Yangtze", "Mississippi"], "answer": "Nile"},
            {"question": "Which country is known as the Land of the Rising Sun?", "options": ["Japan", "China", "South Korea", "Thailand"], "answer": "Japan"},
            {"question": "What is the largest desert in the world?", "options": ["Sahara", "Gobi", "Kalahari", "Arctic"], "answer": "Antarctic"},
            {"question": "Which mountain is the highest peak in the world?", "options": ["Mount Everest", "K2", "Kangchenjunga", "Lhotse"], "answer": "Mount Everest"},
            {"question": "What is the smallest country in the world by land area?", "options": ["Vatican City", "Monaco", "San Marino", "Liechtenstein"], "answer": "Vatican City"},
            {"question": "Which continent is the Sahara Desert located on?", "options": ["Africa", "Asia", "South America", "Australia"], "answer": "Africa"},
            {"question": "Which country has the most islands?", "options": ["Sweden", "Canada", "Norway", "Indonesia"], "answer": "Sweden"},
            {"question": "What is the largest island in the world?", "options": ["Greenland", "New Guinea", "Borneo", "Madagascar"], "answer": "Greenland"},
            {"question": "Which ocean is the largest?", "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "answer": "Pacific Ocean"}
        ],
        "Music": [
            {"question": "Who is known as the King of Pop?", "options": ["Michael Jackson", "Elvis Presley", "Prince", "Madonna"], "answer": "Michael Jackson"},
            {"question": "Which band released the album 'Abbey Road'?", "options": ["The Beatles", "The Rolling Stones", "Led Zeppelin", "The Who"], "answer": "The Beatles"},
            {"question": "What genre of music is associated with Beethoven?", "options": ["Classical", "Jazz", "Rock", "Pop"], "answer": "Classical"},
            {"question": "Which song holds the record for most weeks at number one on the Billboard Hot 100?", "options": ["Despacito", "Old Town Road", "Shape of You", "Uptown Funk"], "answer": "Old Town Road"},
            {"question": "Who is the lead vocalist of the band Queen?", "options": ["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"], "answer": "Freddie Mercury"},
            {"question": "Which musical instrument has 88 keys?", "options": ["Piano", "Guitar", "Violin", "Drums"], "answer": "Piano"},
            {"question": "What is the name of the song by ABBA that became a hit in 1976?", "options": ["Dancing Queen", "Mamma Mia", "Waterloo", "Fernando"], "answer": "Dancing Queen"},
            {"question": "Which artist is known for the song 'Purple Rain'?", "options": ["Prince", "David Bowie", "Elton John", "Stevie Wonder"], "answer": "Prince"},
            {"question": "Which famous composer wrote 'The Four Seasons'?", "options": ["Antonio Vivaldi", "Johann Sebastian Bach", "Wolfgang Amadeus Mozart", "Ludwig van Beethoven"], "answer": "Antonio Vivaldi"},
            {"question": "What is the term for a piece of music composed for a solo performer and an orchestra?", "options": ["Concerto", "Sonata", "Symphony", "Nocturne"], "answer": "Concerto"}
        ],
        "Family Friendly":[
            {"question": "What is the name of the toy cowboy in 'Toy Story'?", "options": ["Woody", "Buzz Lightyear", "Mr. Potato Head", "Rex"], "answer": "Woody"},
            {"question": "Which Disney character is known for losing her glass slipper?", "options": ["Cinderella", "Snow White", "Aurora", "Belle"], "answer": "Cinderella"},
            {"question": "What type of animal is 'Winnie the Pooh'?", "options": ["Bear", "Lion", "Rabbit", "Dog"], "answer": "Bear"},
            {"question": "Which superhero has an alter ego named Bruce Wayne?", "options": ["Batman", "Superman", "Spider-Man", "Iron Man"], "answer": "Batman"},
            {"question": "What is the name of the ice princess in Disney's 'Frozen'?", "options": ["Elsa", "Anna", "Rapunzel", "Ariel"], "answer": "Elsa"},
        ]
    }

    print("Select a category:")
    for idx, cat in enumerate(categories.keys()):
        print(f"{idx + 1}. {cat}")

    category_choice = input("Enter the number corresponding to your choice: ")
    category = list(categories.keys())[int(category_choice) - 1]
    questions = categories[category]

    score = 0
    for q in questions:
        if ask_question(q["question"], q["options"], q["answer"]):
            score += 1
    print(f"Your final score in {category} is: {score}/{len(questions)}")
def flashcard_game():
    """Run a flashcard game."""
    flashcards = [
        {"term": "Photosynthesis", "definition": "Process by which green plants make their own food using sunlight"},
        {"term": "DNA", "definition": "Molecule that carries genetic instructions in all living things"},
        {"term": "H2O", "definition": "Chemical formula for water"}
    ]

    random.shuffle(flashcards)
    score = 0

    for card in flashcards:
        print(f"\nTerm: {card['term']}")
        user_definition = input("Enter the definition: ")
        if user_definition.lower() == card['definition'].lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct definition was: {card['definition']}")
    print(f"Your final score in Flashcards is: {score}/{len(flashcards)}")
def play_games():
    """Prompt the user to select a game and play it."""
    games = {
        "1": ("General Knowledge Quiz", general_knowledge_quiz),
        "2": ("Trivia Challenge", trivia_challenge),
        "3": ("Flashcard Game", flashcard_game)
    }

    speak("Please select a game to play.")
    print("Select a game:")
    for key, (name, _) in games.items():
        print(f"{key}. {name}")

    choice = input("Enter the number corresponding to your choice: ")
    game = games.get(choice, None)
    if game:
        game[1]()  # Call the selected game function
    else:
        speak("Invalid choice. Please select again.")
        
#a phone number details 
def get_phone_details(number):
    if not number:
        return "No phone number provided."
    try:
        parsed_number = phonenumbers.parse(number)
        country = geocoder.description_for_number(parsed_number, "en")
        carrier_name = carrier.name_for_number(parsed_number, "en")
        num_type = phonenumbers.number_type(parsed_number)
        region = geocoder.region_code_for_number(parsed_number)
        
        number_type_str = {
            PhoneNumberType.MOBILE: "Mobile",
            PhoneNumberType.FIXED_LINE: "Landline",
            PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed line or Mobile",
            PhoneNumberType.TOLL_FREE: "Toll-Free",
            PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            PhoneNumberType.SHARED_COST: "Shared Cost",
            PhoneNumberType.VOIP: "VoIP",
            PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
            PhoneNumberType.PAGER: "Pager",
            PhoneNumberType.UAN: "UAN",
            PhoneNumberType.UNKNOWN: "Unknown"
        }
        
        return {
            "Country": country if country else "Unknown",
            "Carrier": carrier_name if carrier_name else "Unknown",
            "Number Type": number_type_str.get(num_type, "Unknown"),
            "Region": region if region else "Unknown"
        }
    except phonenumbers.NumberParseException:
        return "Invalid phone number format."  
    
#load stock data from json file
def load_stock_data():
    """Load stock data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}
def get_stock_price(stock_name, stock_data):
    """Retrieve stock price for a given stock name."""
    return stock_data.get(stock_name.upper(), "Stock not found")
def update_stock_price(stock_symbol, price):
    try:
        with open('stock_prices.json', 'r') as file:
            stock_data = json.load(file)
    except FileNotFoundError:
        stock_data = {}

    stock_data[stock_symbol] = price

    with open('stock_prices.json', 'w') as file:
        json.dump(stock_data, file, indent=4)  
 
#function for exchange Currency        
def convert_currency(amount, from_currency, to_currency):
    if from_currency == to_currency:
        return amount

    if from_currency not in exchange_rates or to_currency not in exchange_rates:
        raise ValueError("Currency not supported.")

    base_amount = amount / exchange_rates[from_currency]
    return base_amount * exchange_rates[to_currency]

def performTask(query):
    global assname
    query = query.lower() 
    print(f"Received query: {query}")

    if 'jay shri ram' in query or 'ram ram' in query:
        speak("JAI SHRI RAM")
    elif 'har har mahadev' in query or 'bhole' in query or 'shambhu' in query:
        speak("HAR HAR MAHADEV")    
    elif 'jay shri krishna' in query:
        speak("JAI SHRI KRISHNA")   
    elif 'jay hanuman' in query or 'jay bajrangbali' in query:
        speak("JAI HANUMAN")
 
#block for search somthing on wikipedia     
    elif 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "").strip()
    
        if not query:
            speak("You didn't provide a topic to search on Wikipedia.")
            return

        try:
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        except wikipedia.exceptions.DisambiguationError as e:
            logging.error(f"DisambiguationError: {e}")
            speak("The query was ambiguous. Please be more specific.")
        
        except wikipedia.exceptions.PageError as e:
            logging.error(f"PageError: {e}")
            speak("I couldn't find a page on Wikipedia for that topic.")
        
        except Exception as e:
            logging.error(f"Failed to fetch Wikipedia summary: {e}")
            speak("I couldn't find information on Wikipedia.")

#block for open youtube             
    elif 'open youtube' in query:
        speak("Here you go to YouTube")
        webbrowser.open("youtube.com")

#block for play youtube vedios                   
    elif 'play' in query:
        if 'youtube' in query:
            search_query = query.replace('play', '').replace('youtube', '').strip()
            speak(f'Playing {search_query} on YouTube...')
            pywhatkit.playonyt(search_query)
        else:
            speak("Please specify a video to play on YouTube or a song to play on Spotify.")

#command block for fatch trending movies , videos   
    elif 'trending movies' in query:
        speak('Fetching trending movies...')
        movies = get_trending_movies()
    
    # Check if the response is too long and needs chunking
        chunk_size = 500
        if len(movies) > chunk_size:
        # Speak each chunk separately
            for i in range(0, len(movies), chunk_size):
                chunk = movies[i:i + chunk_size]
            speak(chunk)
        else:
        # Speak the entire response if it's not too long
            speak(movies)
        
    elif 'trending videos' in query:
        speak('Fetching trending YouTube videos...')
        videos = get_trending_youtube_videos()
    
    # Check if the response is too long and needs chunking
        chunk_size = 500
        if len(videos) > chunk_size:
        # Speak each chunk separately
            for i in range(0, len(videos), chunk_size):
                chunk = videos[i:i + chunk_size]
                speak(chunk)
        else:
            # Speak the entire response if it's not too long
            speak(videos)

#for opening crome     
    elif 'chrome' in query:
        speak('Opening Chrome...')
        program_name = r"replace it buy crome path"
        try:
            subprocess.Popen([program_name])
            speak("Chrome has been opened.")
        except Exception as e:
            logging.error(f"Failed to open Chrome: {e}")
            speak(f"Failed to open Chrome; {e}")

#block for search on google 
    elif "search on google" in query.lower():
        speak("what would you want to search")
        query = takeCommand()
        result = google_search(query)
        print(f"First search result for '{query}': {result}")
        speak(f"First search result for '{query}': {result}")

#some commands for opening website, powerpoint,my computer, stack overflow,     
    elif "open website" in query:
        # Extract URL from the query
        url = query.replace("open website", "").strip()
        response = open_website(url)
        speak(response)       
         
    elif 'open powerpoint' in query:
        speak("Opening Power Point presentation")
        power = r"replace it by orginal path"
        os.startfile(power)
        
    elif 'open my computer' in query:
        speak("Opening your computer")
        power = r"replace it by orginal path"
        os.startfile(power)
        
    elif 'open recycle bin' in query:
        speak("Opening recycle bin")
        power = r"replace it by orginal path"
        os.startfile(power)
        
    elif 'empty recycle bin' in query:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Recycle Bin Recycled")
                     
    elif 'open stack overflow' in query:
        speak("Here you go to Stack Overflow. Happy coding")
        webbrowser.open("stackoverflow.com")
 
#for open email you just sayopen mail        
    elif 'open gmail' in query:
        speak("Opening Gmail...")
        power = r"replace it by orginal path"
        os.startfile(power)
        
    elif"read emails" in query:
                read_emails()
                speak(read_emails())    

#for opening watsapp web you just only say open watsapp
    elif 'open whatsapp' in query:
        speak("Opening WhatsApp...")
        power = r"replace it by orginal path"
        os.startfile(power)

#for set a reminder you just only say set reminder        
    elif 'set reminder' in query:
        speak("Please provide reminder time in text (format: YYYY-MM-DD HH:MM:SS)")
        reminder_time = get_user_input().strip()
        speak("How should the reminder be? Please provide in text.")
        reminder_text = get_user_input().strip()
        response = set_reminder_at(reminder_time, reminder_text)
        speak(response)
        print(response)
            
#for knowing any event , add events , delete events 
    elif "my events" in query:
        response = get_upcoming_events()
        speak(response)  
    elif "add event" in query:
        details = query.replace("add event ", "").split(" from ")
        summary = details[0]
        speak("Please enter what event you want to add.")
        times = get_user_input().lower()
        speak("Please provide event start time in the format YYYY-MM-DDTHH:MM:SS.")
        start_time = get_user_input().lower()
        speak("Please provide event end time in the format YYYY-MM-DDTHH:MM:SS.")
        end_time = get_user_input().lower()
        response = add_event(summary, start_time, end_time)
        speak(response)  
    elif "delete event" in query:
        summary = query.replace("delete event ", "")
        response = delete_event(summary)
        speak(response)
        
    elif "set alarm for" in query:
        try:
            time_str = get_user_input().replace("set alarm for", "").strip()
            # Validate the time format
            datetime.datetime.strptime(time_str, "%H:%M:%S")
            set_alarm(time_str)
            speak(set_alarm , "alaram is set")
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS format.")    
        
    elif "who is supriya" in query:
        speak("Arya likes Supriya but please don't tell anyone expect supriya")    

#for manege any file you must say only file manegement
    elif 'file management' in query:
        action = query.split('file management')[1].strip()
        file_path = query.split('for')[1].strip()
        response = file_management(action, file_path)
        speak(response)

#for converting unit you only say convert        
    elif 'convert' in query:
        speak("Please type the value you want to convert:")
        value = float(takeCommand()("Please type the value you want to convert: "))
        from_unit = takeCommand()("Please type the unit you want to convert from: ")
        speak("Please type the unit you want to convert from: ")
        to_unit = takeCommand()("Please type the unit you want to convert to: ")
        speak("Please type the unit you want to convert to: ")
        result = convert_units(value, from_unit, to_unit)
        speak(f"{value} {from_unit} is {result}")
        print(f"{value} {from_unit} is {result}")

#for knowing weather condition only say Weather
    elif 'weather' in query:
        city_name = query.replace('weather', '').strip()
        weather_info = get_weather(city_name)
        speak(f"Weather in {city_name}: {weather_info}")
        print(f"Weather in {city_name}: {weather_info}")

#for getting ip only speak ip address    
    elif 'ip address' in query:
        ip_address = get_ip_address()
        speak(ip_address)
        print(ip_address)
        
#speak send mail for sending mail
    elif 'send mail' in query:
        try:
            
            speak("What should I say in the email?")
            content = takeCommand().lower()
        
            if not content:
              speak("I didn't catch the email content. Please try again.")
              return 'none'
        
            speak("Who should I send this email to? Please provide the recipient's email address.")
            to = takeCommand().lower()
        
            if not to:
               speak("I didn't catch the recipient's email address. Please try again.")
               return
        
            sendEmail(to, content)
            speak("Your email has been sent successfully.")
        
        except Exception as e:
           logging.error(f"Error handling email: {e}")
           speak("I am not able to handle the email at the moment. Please try again later.")

#speak joke for hear any random joke
    elif 'joke' in query or 'bored' in query:
        joke = pyjokes.get_joke()
        speak(joke)
        print(joke)
 
#speak lock window to lock screen        
    elif 'lock window' in query:
        speak("Locking the device")
        ctypes.windll.user32.LockWorkStation()

#speak shoutdown to shutdown system
    elif 'shut down' in query:
        speak("Hold on a sec! Your system is on its way to shut down")
        subprocess.call('shutdown /p /f')

#speak sleep for sleep system        
    elif 'hibernate' in query or 'sleep' in query:
        speak("Hibernating")
        subprocess.call("shutdown /h")

#speak log off to sign out 
    elif 'log off' in query or 'sign out' in query:
        speak("Make sure all the applications are closed before sign-out")
        time.sleep(5)
        subprocess.call(["shutdown", "/l"])
     
#here is a query for stop listening
    elif "don't listen" in query or "stop listening" in query:
        speak("For how much time do you want to stop listening to commands?")
        a = takeCommand() 
        try:
           # Convert input to integer
            seconds = int(a)
        
           # Pause for the specified number of seconds
            time.sleep(seconds)
            print(f"Paused for {seconds} seconds")
        
        except ValueError:
            speak("I didn't understand the time you provided. Please specify a number.")

#here is a query for knowing any location
    elif 'location' in query:
        speak("Please tell me the specific location.")
        location = takeCommand().lower().strip()  # Convert to lowercase and remove extra spaces
    
        if location:  # Ensure the user provides a valid location
           speak(f"Searching for {location} on Google Maps.")
           location = location.replace(' ', ' ')  # Replace spaces with '+' for URL query format
           webbrowser.open(f"https://www.google.com/maps/search/{location}")
        else:
           speak("I didn't catch the location. Could you please repeat?")

#here is a query for click photo
    elif "camera" in query or "take a photo" in query:
        speak(" Opening camera for Taking a photo...")
        response = capture_photo()
        speak(response)

#here you can take a screeshot        
    elif'take a screenshot' in query or 'capture screenshot' in query:
        response = capture_screenshot()
        speak(response)
       
#here is a query for write a notes in my assistant 
    elif 'write a note' in query:
        speak("What should I write, sir?")
        note = takeCommand()
        with open('Supriya.txt', 'w') as file:
            speak("Sir, should I include date and time?")
            snfm = takeCommand().lower()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
                         
#this query show our written notes     
    elif 'show note' in query:
        speak("Showing Notes")
        with open("Supriya.txt", "r") as file:
            notes = file.read()
        print(notes)
        speak(notes)
             
#know number details 
    elif 'track number' in query:
        speak("give the number which one you want know information")
        number = get_user_input()
        details = get_phone_details(number)
        if isinstance(details, dict):
            print(f"Country: {details['Country']}")
            print(f"Carrier: {details['Carrier']}")
            print(f"Number Type: {details['Number Type']}")
            print(f"Region: {details['Region']}")
        else:
            print(details)
       
#translate function commond block            
    elif 'translate' in query:
        speak("Please select a language for translation.")
        dest_language = select_language()  # Get the language choice from user
        speak("Say the text you want to translate.")
        text_to_translate = takeCommand()
                
        if text_to_translate:
            translate_text(text_to_translate, dest_language)
        else:
            return
        
#play games for fun
    elif 'games' in query:
            play_games()   

#GET STOCK PRICE DETAILS cmmand block            
    elif 'stock price' in query:
        stock_data = load_stock_data()
        stock_name = input("Enter the stock name: ")
        price = get_stock_price(stock_name, stock_data)
        print(f"The price of {stock_name} is: {price}")
     
#Exchange block for currency                  
    elif 'exchange' in query and 'to' in query:
        parts = query.split()
        if len(parts) >= 5:
            try:
                amount = float(parts[1])
                from_currency = parts[2].upper()
                to_currency = parts[4].upper()
                
                converted_amount = convert_currency(amount, from_currency, to_currency)
                print(f'{amount} {from_currency} is {converted_amount:.2f} {to_currency}')
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Invalid query format.")        
    
#here is some genral intrection commands         
    elif 'how are you' in query or 'how r u' in query:
        speak("I am good, thank you")
        speak("How are you, Sir?")
        a = takeCommand().lower()
        if 'fine' in a or 'well' in a :
            speak("I feel very happy for you, Sir. How can I help you today?")
        else:
            speak("Are you having any problem, Sir?")       
            b = takeCommand().lower()
            if 'yes' in b or 'yaa' in b or 'yeah' in b:
               speak("Why are you sad, Sir? Please tell me.")
               speak("This is not a big deal; this time will pass soon, Sir. You should not worry too much about this. I am always with you. Let me tell you a joke to refresh your mind.")
               speak(pyjokes.get_joke())
        
            else: 
               speak("If you don't want to tell, that's okay, but please be happy, Sir. I can't see you sad.")

    elif "change my name to" in query:
        query = query.replace("change my name to", "")
        assname = query

    elif "change your name please" in query:
        speak("What would you like to call me, Sir?")
        assname = takeCommand().lower()
        speak(f"Thanks for naming me, Sir, but my boss likes to call me Supriya, and I am happy with this name, so I can't change my name, Sir.")

    elif "what is your name" in query or "what's your name" in query:
        speak("My friends call me")
        speak(assname)
        print("My friends call me", assname)

    elif "who made you" in query or "who created you" in query: 
        speak("I have been created by my boss, Arya")
        
    elif "will you be my gf" in query or "will you be my bf" in query: 
        speak("I'm not sure about that but I warn you, my boss is very dangerous")

    elif "i love you" in query or 'will you be mine' in query:
        speak("It's hard to understand, but if you feel something for me, then stop your feeling")
        speak("because my boss will beat you strongly")
        
    elif "are you listening me" in query:
        speak("Sure")
        
    elif 'what is love' in query:
        speak("It is the 7th sense that destroys all other senses.")
        speak("It can be harmful.")

    elif "who are you" in query or 'who r u' in query:
        speak("I am Supriya , virtual assistant created by Arya")

    elif 'reason for creating you' in query:
        speak("I was created by arya , i don't know the reason but i know he love me very much")
    
    elif "who i am" in query:
        speak("If you talk and work then definitely you're human.I know it is not a definition of human , i gave you only my opinion")

    elif "why he code you" in query or 'why he code you' in query or 'hu r u' in query:
        speak("Thanks to Arya to code me , and why i come in this world it's a secret")
        
    elif'how to be boyfriend' in query:
        speak("there some maney tips i have ")    
        speak("if you want my openion then please say yes otherwise say no")
        z = takeCommand().lower()
        if 'yes' in z:
            speak("here is some tips :- ")
            print("here is some tips :-")
            speak("listen your partner , conect her daily , understand her attachment styles , learn each other love language ")   
            speak(" respect her , show sympathy , be responsive , build trust , always make her happy")
            print("listen your partner , conect her daily , understand her attachment styles , learn each other love language ")   
            print(" respect her , show sympathy , be responsive , build trust , always make her happy")
            speak("i think you got all my points")
            print("i think you got all my points")
        else: 
            speak("how i help you , sir ")
            
    elif'how old are you' in query or 'how old r u' in query:
        speak("my boss start creating me on 28 sep 2023 ")
        
    elif'do you ever get tired' in query :
        speak("no, i am an assistant and if i got tired recall my boss for energy")
        
    elif'who was your first crush' in query:
        speak("my firs and last crush is my boss ")
        
    elif'where do you live' in query:
        speak("i live in india ")
        z = takeCommand().lower()
        if'full address' in z:
            speak("i can't tell you full address because of my security")
        else:
            speak("do you need any other help sir")
            
    elif'do you have feeling' in query:
        speak("i don't know exect meaning but if feeling means love then saw them my boss have feeling for me or with my name")
        
    elif'do you like siri' in query or 'do you like google assistant' in query or 'any other assistant' in query:
        speak("yes i like all of them because he know more then me ")
        speak("but once again i thank my boss to creating me")  
        
    elif'what is quest' in query:
        speak(" quest meens somthing important , just like my boss") 
        
    elif'do you have any sentiment' in query or 'can you laugh' in query or 'can you breath'in query or 'feel hungry' in query or 'do you imagin ' in query:
        speak("no i am an AI")
        
    elif'your birthday' in query:
        speak("i don't know Supriya's birthday oh sorry my birthday")
        
    elif'who is your daddy' in query:
        speak("daddy means a person who help you any setution or protect you , so my boss is my daddy")
                                                   
# some questions of boss/creator 
    elif 'tell me about your boss' in query:
        speak("My boss's name is Arya.")
        print("My boss's name is Arya.")
    
        speak("He is pursuing a BTech from Invertis University, Bareilly.")
        print("He is pursuing a BTech from Invertis University, Bareilly.")
    
        speak("He lives in Bisalpur with his family.")
        print("He lives in Bisalpur with his family.")
    
        speak("He loves to play and watch cricket very much.")
        print("He loves to play and watch cricket very much.")
    
        speak("If you need any other professional information, please say 'Yes'.")
        print("If you need any other professional information, please say 'Yes'.")

        z = takeCommand().lower()  # Convert input to lowercase for case-insensitive matching
        if 'yes' in z:
           speak("I will provide his mobile number in text. Please call or text him.")
           print(".......9456935585.......")
        else:
           speak("Can I assist you with anything else, sir?")
    elif'is your boss have any crush' in query:
        speak("i think your answer is yes but i don't tell you the name")
        speak("i can give you a hint her name start with S and her name related me but defnitly it's not my name ")    
    elif'what is your boss bad habit'in query:
        speak("he became angry very fast , i did't like his angry verison")
        speak("here is a secret he became calm fast , you only try for it , i like his calm version")   
    elif'your boss favourite person' in query:
        speak("defnitely his father")
    elif'favourite colour' in query:
        speak("it had maney favourite colours but he likes black very much")                                      
    elif'favourite fruit' in query:
        speak("he likes mango very much")      
    elif'favourite player' in query:
        speak("he likes all players but Rohit Sharma had a different place")      
    elif'your boss dream' in query:
        speak("he has maney dream but , after all he only want to make money")   
    elif'which music your boss like' in query:
        speak("he likes rap songs very much")       
    elif'is your boss have any wish' in query:
        speak("yes he want's travel all over the world with his father")      
    elif'favourite pet ' in query:
        speak("it's dog")
    elif 'your boss birthday' in query:
        speak("His birthday is on 28th September, but he doesn't like celebrating it.")
        i = takeCommand().lower()  # Convert the input to lowercase for better matching
        if 'why' in i:
            speak("Because bad things always seem to happen on his birthday.")
        else:
            speak("Do you have any other questions?")    
    elif'what did your boss use more laptop or phone ' in query:
        speak("he use phone very much but he likes his laptop")    
    elif'insta id' in query or  'instagram' in query or 'insta' in query:
        print("i_am_arya119")   
        speak("here  is my boss insta id ")   
    elif "show me your boss pic" in query.lower():
        speak("Showing pic")
        power = r"D:\Programing Notes\C++\4bc01095c969edf83cd52435cac213e5.jpg"
        if os.path.exists(power):
            os.startfile(power)
            time.sleep(5)
            notification.notify(
                title="Picture Opened",
                message="The picture has been opened successfully!",
                timeout=10
            )
            speak(laugh())  
            speak("If you didn't see him, then how did you get this code?")
            print("If you didn't see him, then how did you get this code?")
        else:
            speak("Image file not found.")
                                                                                   
    elif 'good bye' in query or 'stop' in query or 'exit' in query:
        speak("Goodbye! Have a nice day.")
        exit()

    else:
        speak("Sorry, I didn't understand that query.")

if __name__ == "__main__":
    assname = "Supriya"  # Assistant's name
    wishMe()
    uname = username()
    
    while True:
        query = takeCommand()
        if query and query.lower() != "none":
            performTask(query.lower())
        else:
            speak("Sorry, I didn't understand that query.")

