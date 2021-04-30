#Imports libraries
import requests
import webbrowser
from playsound import playsound
from random import randrange
import pyttsx3
from datetime import datetime
import pyaudio
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup
import wikipedia
from num2words import num2words
from word2number import w2n
import webbrowser
import imaplib
import email
import traceback
import smtplib
import time as Time

# intilize sepach recognition
def listen(thresh=1):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.energy_threshold = 4000 #Capture audio at 4000
        audio = r.listen(source)
        r.dynamic_energy_threshold = True
        r.pause_threshold = thresh
        try:
            r.adjust_for_ambient_noise(source,duration=0.2)
            command = r.recognize_google(audio) #Text to speech 
        except sr.UnknownValueError: #Value
            r.adjust_for_ambient_noise(source,duration=1) #Re calibrate for ambient noise
            return "None"
        return command

#Initlizing text to speach engine and sets the voice 
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[5].id)
engine.setProperty('rate',225)

# You pass this function a piece of text you want it to read and it reads
# I made this so that I dont have to keep on writing engine.say() then engine.runAndWait()
def speak(text):
    engine.say(text)
    engine.runAndWait()

#Time functions
def time():
    dateTime = datetime.now()
    #Grabs date and time from date time class
    DateArray = [dateTime.strftime("%A"),dateTime.strftime("%B"),dateTime.strftime("%d"),dateTime.strftime("%Y"),dateTime.strftime("%I"),dateTime.strftime("%M"),dateTime.strftime("%p")]
    return DateArray

def add_contact():
    complete_contact = []
    correct = False
    while not correct:
        speak("Please say the email of the person you would like to add.")
        email = listen(thresh=10).lower()
        #Speaks email out letter by letter 
        for letter in email:
            speak(letter)
        speak("Is this right spelling?")
        awns = listen().lower()
        if "yes" in awns:
            speak("What would you like to name this contact as?")
            name = listen(thresh=10).lower()
            #Speaks out name letter by letter
            for letter in name:
                speak(letter)
            speak("Is this correct?")
            awns = listen().lower()
            if "yes" in awns:
                correct = True
            else:
                continue
        else:
            continue #If it is wrong it will redo it
    email = email.replace(" ","").replace("at","@")
    complete_contact.append([email, name]) #Adds email and name as an array
    return complete_contact
  
def read_contacts(contacts):
    if len(contacts) == 0: #means no contacts
        speak("You don't have any contacts")
    else:
        speak("you're contacts are")
        for contact in contacts: #Goes one by one through contact list and speaks their name
            speak(contact[1])

def delete_contacts(contacts):
    contacts = contacts
    org_length = len(contacts)
    attempts_to_locate = 0
    speak("Who's contact would you like to delete?")
    delete_person = listen().lower()
    for i in range(len(contacts)):
    #I used try and except block to make sure it does not error out out if it could not find that person 
        try: 
            if contacts[i].index(str(delete_person)): #Checks if that persons name is valid within the current contatc
                del contacts[i]
        except:
            attempts_to_locate += 1
    if attempts_to_locate < org_length:
        speak("Contact has been deleted")
    else:
        speak(f"No such contact as {delete_person}")
    
    return contacts
    
def send_mail(recipient, message=None):
    sender_email = "DavidJhonyTechAlt@gmail.com"
    recive_email = recipient
    password = "BurnerAcc"
    if message == None: #Message param is just so that I can make it so I can send new's url; which is a special send
        speak("What would you like to send")
        message = listen().lower()
    else:
        message = message
    server = smtplib.SMTP('smtp.gmail.com',587) #Starts the server conntection
    server.starttls() #Makes it some what secure
    server.login(sender_email, password) #Log in credintals needed to log in
    print("Log in pass")
    server.sendmail(sender_email, recive_email, message) #Actul sending
    print("message has been sent")
    server.quit() #Ends the server

#Greeting
#Basic idea there are two possible themes; either a formal or informal
#It generates a random number from 2 the length of the array and selects the theme
#So from there it checks time if it selected formal and says a greeting according to the time 
#if informal then it says a random greeting from the informal theme 
def Greeting(Time, user): 
    greetings = [[f"Good morning, {user}! how can I help you?","Good afternoon, {user}! How can I help you?","Good evening, {user}! What can I do for you?"],["How can I help you {user}?","What can I do for you...","How can I be of assistance?","Here to help!",]]
    if randrange(2) == 0: #To see if it does formal greetings
        if Time[-1] == "AM":
            speak(greetings[0][0] + user)
        elif Time[-1] == "PM" and 12 - int(Time[4]) == 0 or 12 - int(Time[4])  <= 11 and 12 - int(Time[4]) >= 6: #Just checks if the time is the afternoon, does so by checking if it is withn a certain time frame
            speak(greetings[0][1])
        else: #Just says good evening
            speak(greetings[0][2]) 
    elif randrange(2) == 1: #This does informal greetings, like how can I help you etc.
        speak(greetings[1][randrange(len(greetings[1]))])

#Settings function
#takes a statment rus through if statments looks for key words 
#Once it has found a key word like voice or rate it changes that setting
#For voice all it does is it loops through the voice properties and sets it to a diffrent voice and reads a sample of text
#If the user likes that voice and says yes the voice is saved and a conformation message is played
#For rate it just asks for a number from 0 to 100
# Then it takes that inputed value and converts to a int and divides by 100 then muktiplies by the maximum increase in voice rate then adds that to base line rate
# Then asks user if it is okay and if it is then it saves it 
def ChangeSettings(statement):
    if "voice" in statement:
        speak("Please say stop at the voice you like. If you did not mean to change my voice")
        for i in voices:
            engine.setProperty('voice',i.id)
            speak('Hello, my name is jarvis , would you like to save this voice?')
            awnser = listen().lower()
            if awnser == "no":
                continue
            else:
                break
        speak("This is conformation that my voice has changed")

    if "rate" in statement or "speed" in statement:
        org_rate = engine.getProperty('rate')
        speak("how fast do you want my rate to be? Make sure it is from 0 percent to 100 percent ")
        value = listen().lower()
        percent = 150 + ((w2n.word_to_num(value.replace("%",""))/100)*100) #This makes it into a valid percent. 150 added as anything below 150 is not working so well  
        engine.setProperty('rate',int(percent))
        speak("Do you like this speed?")
        b = listen().lower()
        if "yes" in b:
            speak("Alright, this rate has been saved")
        elif "no" in b:
            speak("Alright this rate has not been saved")
            engine.setProperty('rate',org_rate)

#Check if the awnser givin for the calibration matches the actual awnser
def check(inpt,awnser):
    awnser = awnser.lstrip()#Removes leading spaces
    awnser = awnser.rstrip()#Removes trailing spaces
    if inpt == awnser: 
        awns = ["Good","Good almost done","Almost done","Excellent","almost there"]
        speak(awns[randrange(0,len(awns))])
        return True
    else:
        return False    

#Variables 
contacts = [["person1@gmail.com","Person1"],["person2@yahoo.com","person2"]]
ask_for_name = True
user = ""
boolOn = False #for auto start 
calendar = [] #For reminder part
last_command = None #Stores last command of user
Calibrate_needed = True #See's if calibration is needed


while True:
#Calibration
#basic idea is when a variable is set to True the calibraion runs 
#All the calibration part does is it loops throught the wanted awnsers and waits for user to say it correctly 
#The user must say it correctly for 2 times
# This allows the program to adjust not only to their voice but also to the background noise
# Variables  
    if Calibrate_needed == True:
        speak("Hello, I am jarvis your personal assistant. I am here to help, but before I am able to help I need to get accustomed to your home environment")
        Calibrate_needed = False
        passed = False
        Check_points = 0
        while not passed:
            stages = [[False,"weather"],[False,"jarvis"]]
            for i in stages:
                if not stages[stages.index(i)][0]: #Checks if that stage is not complete by seeing if it is false 
                    for i in range(len(stages)):
                        stages[i][0] = True #If the last if was passed then it sets the stage value to be complete this ensure's we are not stuck in this loop for ever
                        while Check_points <2: # Basicly you have to say what every phrase is in the stage two times, then it moves on to next stage. I did this design so that I can have how ever many stages is need
                            speak("Say " + stages[i][1])
                            result_awn = listen().lower()
                            print(result_awn)
                            if check(result_awn,stages[i][1]):
                                Check_points+=1
                            else:
                                speak("Try again")
                        Check_points = 0            
            if stages[0][0] and stages[1][0]: #Checks if both stages are set true meaing they were sucsessfully complete
                passed = True
                speak("Calibration complete")         

    #Main section, all it does is, it takes your request and see's if there is any other request like that, if not then it will say 'can't do that
    command = listen().lower()
    if "jarvis" in command or boolOn: #If Jarvis is in command it starts the program or if the user has aldready turned Jarvis on thenn boolOn would be true and no need to say Jarvis
        if not boolOn:
            playsound(r"C:\Users\rahul\OneDrive\Desktop\ActivatedSound.mp3") #Makes sure sound only plays if user is just starting
        
        #This is just to ensure you only said 2 words so that the program does not get confused
        if len(command.split(" ")) <= 2 and not boolOn: #This is so that if user says greeting it follows a diffrent methof of getting rqst
            Greeting(time(), user)
            rqst = listen().lower()
            print(rqst)
            #I personally dont like auto run so I turn it to false but turning it to True will auto run till you say one of the exit phrases
            boolOn = False #here I set boolOn to True becuase the program was activated
        
        else: #If user says hey Jarvis what is the time then it will automaticly give the time and not say any greetings
            rqst = command
            print(rqst)
            boolOn = False #boolOn is activated to true becaue Jarvis was woken up

            if "repeat" in rqst:
                if last_command == None: 
                    speak("You did not ask me anything.")
                elif last_command != None:
                    rqst = last_command
        #Repeat command
        #Repeat command basicly sets rqst to the last rqst
        #It does this by making rqst == to last_command
        #Then the program has the last statment exuctued and will just redo it again
         #What it can do
        if "What can you do" in rqst:
            speak("I can: Check the weather, read the latest news, send emails to contacts, tell the time and date, Remind you to do things and search the Wikipidea")
        
        #This is the weather
        #It has a API key and all the weather properties are stored in properties
        # To find direction of wind I just thought about quadrants in functions 
        # So in this case there are 8 directions then we know bewtween each direction there is a 45degree intrval 
        #So know if you divide the degree by 45 and do a index on the array you get the right direction
        elif "weather" in rqst: 
            orgRate = engine.getProperty('rate')
            engine.setProperty('rate',225)
            data = requests.get("http://api.openweathermap.org/data/2.5/weather?q=mississauga&APPID=e0fd78f229e0bd96f4b4add91220c94f&units=metric").json()        
            properties = [
                str(round(data["main"]["temp"])),
                str(round(data["main"]["feels_like"])),
                str(data["weather"][0]["main"]),
                str(data["wind"]["speed"]),
                str(data["wind"]["deg"])
                ]

            directions = ["north","north east","east","south east","south","south west","west","north west"] 
            speak("The weather in mississauga is " + properties[0] + " ,feels like " + properties[1] + "!" + " and the weather is " + properties[2] + "...,There is a " + str(round(float(properties[3]))) + " kilometers per hour wind, Coming from the " + str([directions[(round(int(properties[4])/45))%len(directions)]])) 
            engine.setProperty('rate',orgRate)
            last_command = "weather"
            

        #This is for wiki search
        elif "wiki" in rqst:
            speak("What would you like to search up in the wiki")
            search = listen().lower() #This is what you want to search for
            #It uses a try and except because sometimes wikipidea does not have a post for that so this just allows for it not to crash if no results are found
            try: 
                search_res = wikipedia.summary(search,sentences=3)  
                speak("According to Wikipidea..." + str(search_res))
                last_command = "wiki"
            except:
                #If there was an error the only error there could be is a no result error so if except is activated then No results gets plated
                speak("No results")            

        #Change settings
        elif "settings" in rqst:
            speak("What would you like to change?")
            thing_to_change = listen().lower()
            if "what can i change" in thing_to_change:
                speak("You can change my voice, how fast I can talk, and how loud I can talk")
                thing_to_change = listen().lower() 
                ChangeSettings(thing_to_change)
            else:
                ChangeSettings(thing_to_change)
                   
        #The time
        elif "time" in rqst:
            speak("The time is currently " + str(time()[4]) + " " + str(time()[5]) + " " + str(time()[6]))
            last_command = "time"
        
        #The date
        elif "date" in rqst:
            if int(time()[2]) <= 9: #Just checks if day is less than 9
                speak("The date is " + str(time()[0]) + " " + str(time()[1]) + " " + str(time()[2]).replace('0',"") + " " + str(time()[3]) + " " +str(time()[4]) + " " + str(time()[5]) + " " + str(time()[6]))
            elif int(time()[2]) > 9: #Checks if dat is greater than 9 
                speak("The date is " + str(time()[0]) + " " + str(time()[1]) + " " + str(time()[2]) + " " + str(time()[3]) + " " +str(time()[4]) + " " + str(time()[5]) + " " + str(time()[6]))
            last_command = "date"
        #Send email
        elif "send email" in rqst:
            email_addr = None
            speak("Whom shall I send this email to??")
            recipient = listen(thresh=5).lower()
            for contact in range(len(contacts)):
                for item in range(len(contacts[contact])): #Checks the if the name matches the name provided
                    if contacts[contact][item] == recipient: #If it does then it will give the email of the contact to the send_email funtion otherwise it says no contact found
                        email_addr = contacts[contact][0] 
            if email_addr == None:
                speak(f"Sorry...There is no person named {recipient}")
                continue
            else:
                send_mail(email_addr)
            last_command = "send email"

        #read contacts
        elif "read" in rqst and "my" in rqst and "contact" in rqst:
            read_contacts(contacts)
        #delete contacts
        elif "remove" in rqst and "contact" in rqst:
            contacts = delete_contacts(contacts)
    
        #Add contact
        elif "add in contact" in rqst:
            contacts.append(add_contact())
            print(contacts)
        
        #reminder
        elif "remind me to" in rqst:
            rqst = rqst.replace("remind me to","").replace("hey","").replace("jarvis","")
            speak("Should I add " + rqst + " to your reminders?")
            awns = listen().lower()
            if "yes" in awns:
                calendar.append(rqst)
                speak("alright")
            elif "no" in awns:
                speak("Fine.")

        #Things to do
        elif "what do i have today" in rqst:
            speak("You have to, ")
            for remind in calendar:
                speak(remind)
            last_command = "what do i have today"

        elif "call me by" in rqst:
            user = rqst.replace("call me by", "")
            speak(f"sure I will call you by {user}")
            if not ask_for_name:
                ask_for_name = True 

        elif "calibrate"  in rqst:
            speak("Sure thing!")
            Calibrate_needed = True

        #News
        elif "news" in rqst:
            main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=&apiKey=25c028c073ea4b8cb0db261460eda1f4"
            open_bbc = requests.get(main_url).json()
            articales = open_bbc["articles"]
            for artical in articales:
                speak("This articale is from " + str(artical["author"]))
                speak(artical["title"])
                speak(artical["description"])
                speak("Would you like me to send you the link to the full artical??")
                send_link = listen().lower()
                if "yes" in send_link:
                    print("Starting LP")
                    send_mail("DavidJhonyTechAlt@gmail.com",message="The link is : " + str(artical["url"]))
                elif "stop" in send_link:
                    speak("Ok.")
                    break
            last_command = "news"

        elif "who made you" in rqst or "who created you" in rqst:
            speak("7 4 3 6 2 7 made me") 

        elif  "jarvis shut down" in rqst or "thank you jarvis" in rqst or "go to sleep jarvis" in rqst  or rqst == "bye":
            goodByeGreeting = ["Until next time","bye","","see you","glad I could help you"]
            speak(goodByeGreeting[randrange(len(goodByeGreeting))])
            boolOn = False 
        else:
            #If no commands were matched it will say one of the things in the sorry_awnsers
            Sorry_awnsers = ["Sorry I am not sure","Unfortunatly I was not programed with that abilty","Sorry I dont recognize that command"]
            speak(Sorry_awnsers[randrange(0,len(Sorry_awnsers))])
