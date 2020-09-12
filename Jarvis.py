import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import requests
import json
import bs4

engine=pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    Time=datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(Time)

def date():
    day=int(datetime.datetime.now().day)
    month=int(datetime.datetime.now().month)
    year=int(datetime.datetime.now().year)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)

def jokes():
    speak(pyjokes.get_joke())

def wish():
    speak("Welcome Back Sir")
    date()
    time()
    hour=datetime.datetime.now().hour
    if hour>=6 and hour<12:
        speak("Good Morning Sir")
    elif hour>=12 and hour<18:
        speak("Good aftenroon Sir")
    elif hour>=18 and hour <24:
        speak("Good evening Sir")
    else:
        speak("Goodnight Sir")            
    speak("Jarvis at your service. Please tell me how can i help you?")

def sendEmail(to,msg):
    server=smtplib.SMTP("smtp@gmail.com",587)
    server.ehlo()
    server.starttls
    server.login('abc@gmail.com','12345')
    server.sendmail('abc@gmail.com',to,msg)
    server.close()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") 
        r.pause_threshold=1
        audio=r.listen(source)

    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(query)

    except Exception as e:
        print(e)
        print("can you please repeat...")
        speak("can you please repeat...") 
        return ("none")
    return query    

def cases():
    speak("Which country cases you want to know?")
    countryname=takeCommand()
    print("Searching about "+countryname)
    speak("Searching about "+countryname)
    r=requests.get("https://coronavirus-19-api.herokuapp.com/countries/"+countryname)
    data=r.json()
    text = f'Confirmed Cases : {data["cases"]}\n Deaths : {data["deaths"]}\n Recovered : {data["recovered"]}'
    print(text)
    speak(text)

def weather():
    speak("Which city name weather you want to know?")
    city_name=takeCommand()
    url = f'https://www.google.com/search?&q=weather in {city_name}'
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text,"html.parser")
    update = s.find("div",class_="BNeawe").text
    print("Temperature in "+city_name+" is "+update)
    speak("Temperature in "+city_name+" is "+update)
def screenshot():
    image=pyautogui.screenshot()
    image.save("ss.png")

def cpu():
    usage=str(psutil.cpu_percent())
    speak('CPU is at '+usage)
    battery=psutil.sensors_battery()
    speak('Battery is at ')
    speak(battery.percent)    

if __name__ == '__main__':
    wish()
    while True:
        query=takeCommand().lower()
        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif 'wikipedia' in query:
            speak("Searching...")
            query=query.replace("wikipedia","")
            result=wikipedia.summary(query,sentences=2)
            print(result)
            speak(result)
        elif 'search in chrome' in query:
            speak("What should I search?")
            chromePath='C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search=takeCommand().lower()
            wb.get(chromePath).open_new_tab(search+'.com')  
        elif 'cpu' in query:
            cpu()  
        elif 'joke' in query:
            jokes()
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        elif 'logout' in query:
            os.system("shutdown -1")   
        elif 'remember that' in query:
            speak("What should i remember?")
            data=takeCommand()
            speak("You have said me to remember "+data)
            remember=open('data.txt','w')
            remember.write(data)
            remember.close()  
        elif 'cases' in query:
            cases()     
        elif 'weather' in query:
            weather()    
        elif 'remember anything' in query:
            remember=open('data.txt','r')
            speak("You told me to remember that "+remember.read())    
        elif 'play songs' in query:
            song_dir='F:\\Songs'
            songs=os.listdir(song_dir)
            os.startfile(os.path.join(song_dir,songs[0])) 
        elif 'screenshot' in query:
            screenshot()
            speak("Done!")                     
        elif 'send email' in query:
            try:
                speak('What should I say?')
                content=takeCommand()
                to='xyz@gmail.com'
                sendEmail(to,content)
                speak("Send Successfully")  
            except Exception as e:
                print(e)
                speak("Unable to send email")      
        elif 'offline' in query:
            speak("Ok Sir have a good day")
            quit()            