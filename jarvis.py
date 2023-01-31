import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import geocoder
import numpy as np
import random
from time import sleep
import pyjokes
import requests
from bs4 import BeautifulSoup
import array

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()


if __name__ == "__main__":
    wishMe()
    while True:
        # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "youremail@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry. I am not able to send this email")

        elif 'location' in query:
            g = geocoder.ip('me')
            speak(g.latlng)
            print(g.latlng)

        elif 'tell a joke' in query:
            My_joke = pyjokes.get_joke(language="en", category="all")
            speak(My_joke)
            print(My_joke)
        
        elif 'bye' in query:
            speak("Bye Bye Sir")
            break

        elif 'switch off' in query:
            os.system("shutdown /s /t 1")
        elif 'logout' in query:
            os.system("logout -l")

        elif 'generate a password' in query:
            # maximum length of password needed
            # this can be changed to suit your password length
            MAX_LEN = int(input("Enter the maximum length of your password\n"))

            # declare arrays of the character that we need in out password
            # Represented as chars to enable easy string concatenation
            DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                                'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                'z']

            UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                                'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                'Z']

            SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                    '*', '(', ')', '<']

            # combines all the character arrays above to form one array
            COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

            # randomly select at least one character from each character set above
            rand_digit = random.choice(DIGITS)
            rand_upper = random.choice(UPCASE_CHARACTERS)
            rand_lower = random.choice(LOCASE_CHARACTERS)
            rand_symbol = random.choice(SYMBOLS)

            # combine the character randomly selected above
            # at this stage, the password contains only 4 characters but
            # we want a 12-character password
            temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol


            # now that we are sure we have at least one character from each
            # set of characters, we fill the rest of
            # the password length by selecting randomly from the combined
            # list of character above.
            for x in range(MAX_LEN - 4):
                temp_pass = temp_pass + random.choice(COMBINED_LIST)

                # convert temporary password into array and shuffle to
                # prevent it from having a consistent pattern
                # where the beginning of the password is predictable
                temp_pass_list = array.array('u', temp_pass)
                random.shuffle(temp_pass_list)

            # traverse the temporary password array and append the chars
            # to form the password
            password = ""
            for x in temp_pass_list:
                    password = password + x
                    
            # print out password
            print(password)


        elif 'what is the temperature' in query:
            speak("Enter the name of the city please")
            city=input("Enter the city name:\n")
            city.lower()
            url = "https://www.google.com/search?q="+"weather"+city
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
            data = str.split('\n')
            time = data[0]
            sky = data[1]
            listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
            strd = listdiv[5].text
            pos = strd.find('Wind')
            other_data = strd[pos:]
            print("Temperature is", temp)
            print("Time: ", time)
            print("Sky Description: ", sky)
            print(other_data)
            speak(temp)
            speak(time)
            speak(sky)
            speak(other_data)