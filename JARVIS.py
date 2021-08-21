import pyttsx3
import webbrowser
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
from selenium import webdriver
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import tkinter as tk
from tkinter import Message ,Text
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import time
import tkinter.ttk as ttk
import tkinter.font as font



client = wolframalpha.Client('RRV9XQ-TWX5VYJ9PU')

engine=pyttsx3.init()

def speak(audio):
    print('JARVIS: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def greetMe():
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')
def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query

def attendance():
    window = tk.Tk()
    window.title("Attendance Management System")
    dialog_title = 'QUIT'
    dialog_text = 'Are you sure?'
    window.configure(background='grey')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') )
    lbl.place(x=400, y=200)
    txt = tk.Entry(window,width=20  ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))
    txt.place(x=700, y=215)
    lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold '))
    lbl2.place(x=400, y=300)
    txt2 = tk.Entry(window,width=20  ,bg="yellow"  ,fg="red",font=('times', 15, ' bold ')  )
    txt2.place(x=700, y=315)
    lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold underline '))
    lbl3.place(x=400, y=400)
    message = tk.Label(window, text="" ,bg="yellow"  ,fg="red"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message.place(x=700, y=400)
    lbl3 = tk.Label(window, text="Attendance : ",width=20  ,fg="red"  ,bg="yellow"  ,height=2 ,font=('times', 15, ' bold  underline'))
    lbl3.place(x=400, y=650)
    message2 = tk.Label(window, text="" ,fg="red"   ,bg="yellow",activeforeground = "green",width=30  ,height=2  ,font=('times', 15, ' bold '))
    message2.place(x=700, y=650)
    def clear():
        txt.delete(0, 'end')
        res = ""
        message.configure(text= res)
    def clear2():
        txt2.delete(0, 'end')
        res = ""
        message.configure(text= res)
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False
    def TakeImages():
        Id=(txt.get())
        name=(txt2.get())
        if(is_number(Id) and name.isalpha()):
            harcascadePath = "C:/Users/ACER/Desktop/Attendance-Management/haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            speak('Need to capture few pictures stay still!!')
            cam = cv2.VideoCapture(0)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    sampleNum=sampleNum+1
                    cv2.imwrite("C:/Users/ACER/Desktop/Attendance-Management/TrainingImage/ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    cv2.imshow('frame',img)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif sampleNum>60:
                    break
            
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Saved for ID : " + Id +" Name : "+ name
            speak('Images Saved')
            row = [Id , name]
            with open('C:/Users/ACER/Desktop/Attendance-Management/StudentDetails/StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
        else:
            if(is_number(Id)):
                res = "Enter Alphabetical Name"
                message.configure(text= res)
            if(name.isalpha()):
                res = "Enter Numeric Id"
                message.configure(text= res)
    def TrainImages():
        speak('Images are Trained now you can take Attendance')
        recognizer = recognizer = cv2.face_LBPHFaceRecognizer.create()#cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "C:/Users/ACER/Desktop/Attendance-Management/haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("C:/Users/ACER/Desktop/Attendance-Management/TrainingImage")
        recognizer.train(faces, np.array(Id))
        recognizer.save("C:/Users/ACER/Desktop/Attendance-Management/TrainingImageLabel/Trainner.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        message.configure(text= res)
    def getImagesAndLabels(path):
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
        faces=[]
        Ids=[]
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(Id)
        return faces,Ids
    def TrackImages():
        recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
        recognizer.read("C:/Users/ACER/Desktop/Attendance-Management/TrainingImageLabel/Trainner.yml")
        harcascadePath = "C:/Users/ACER/Desktop/Attendance-Management/haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        df=pd.read_csv("C:/Users/ACER/Desktop/Attendance-Management/StudentDetails/StudentDetails.csv")
        speak('Place your face in front of camera Ill take the attendance')
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names =  ['Id','Name','Date','Time']
        attendance = pd.DataFrame(columns = col_names)
        while True:
            ret, im =cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            for(x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                if(conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa=df.loc[df['Id'] == Id]['Name'].values
                    tt=str(Id)+"-"+aa
                    attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                else:
                    Id='Unknown'
                    tt=str(Id)
                if(conf > 75):
                    noOfFile=len(os.listdir("C:/Users/ACER/Desktop/Attendance-Management/ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown/Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])
                cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
            cv2.imshow('im',im)
            if (cv2.waitKey(1)==ord('q')):
                break
        speak('Attendance taken')
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour,Minute,Second=timeStamp.split(":")
        fileName="C:/Users/ACER/Desktop/Attendance-Management/Attendance/Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
        attendance.to_csv(fileName,index=False)
        cam.release()
        cv2.destroyAllWindows()
        res=attendance
        message2.configure(text= res)
    clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton.place(x=950, y=200)
    clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
    clearButton2.place(x=950, y=300)
    takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    takeImg.place(x=200, y=500)
    trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    trainImg.place(x=500, y=500)
    trackImg = tk.Button(window, text="Track Images", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    trackImg.place(x=800, y=500)
    quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="red"  ,bg="yellow"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
    quitWindow.place(x=1100, y=500)
    copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
    copyWrite.tag_configure("superscript", offset=10)
    copyWrite.configure(state="disabled",fg="red"  )
    copyWrite.pack(side="left")
    copyWrite.place(x=800, y=750)
    window.mainloop()


  

greetMe()
speak('Hello Sir, I am your digital assistant Jarvis!')
speak('How may I help you?')


  



        

if __name__ == '__main__':
      

    while True:
    
        query = myCommand();
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')
        elif 'shutdown' in query or 'shut down' in query:
            speak('Okay shutting down your PC!!')
            os.system('shutdown/s')
        elif 'restart' in query:
            speak('Okay restarting your PC!!')
            os.system('shutdown/r')
        elif 'take attendance' in query:
            speak('Yes sir!!, Give me a moment..')
            attendance()
        elif 'predict emotion' in query:
            face_classifier = cv2.CascadeClassifier("D:\haarcascade_frontalface_default_1.xml")
            classifier =load_model("D:\\Emotion_Detection.h5")
            class_labels = ['Angry','Happy','Neutral','Sad','Surprise']
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                labels = []
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray,1.3,5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    roi_gray = gray[y:y+h,x:x+w]
                    roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
                    if np.sum([roi_gray])!=0:
                        roi = roi_gray.astype('float')/255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi,axis=0)
                        # make a prediction on the ROI, then lookup the class
                        preds = classifier.predict(roi)[0]
                        print("\nprediction = ",preds)
                        label=class_labels[preds.argmax()]
                        print("\nprediction max = ",preds.argmax())
                        print("\nlabel = ",label)
                        label_position = (x,y)
                        cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                    else:
                        cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
                    print("\n\n")
                cv2.imshow('Emotion Detector',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'open google' in query or 'open chrome' in query:
            speak('okay')
            webbrowser.open('www.google.co.in')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')
        elif 'what is your name' in query or 'what should I call you' in query or 'who are you' in query:
            speak('You can call me Jarvis Sir!!')
        elif 'who is your father' in query or 'who is you mother' in query or 'who is your creator' in query or 'who made you' in query:
            speak('I was created by Ashish and his team')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))
        elif "wait" in query:
            speak('Ill be waiting for you sir!!')
            input('Press any button to continue:')

        elif 'send email' in query or 'send an email' in query:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'others' or 'friend' or 'faculty' or 'family' in recipient:
                try:
                    speak('What should I say? ')
                    content = myCommand()
        
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    #speak("Please enter your login credentials!!")
                    #username=input('Enter username: ')
                    #password=input('Enter password: ')
                    #username='ashish.y0807@gmail.com'
                    #password='Luicfer@@0807'
                    server.login("ashish.y0807@gmail.com","Lucifer@@0807")
                    speak("Please enter the recipients gmail!!")
                    gm=input('Gmail: ')
                    server.sendmail("ashish.y0807@gmail.com", gm, content)
                    server.close()
                    speak('Email sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')


        elif 'nothing' in query or 'abort' in query or 'stop' in query:
            speak('okay')
            speak('Bye Sir, have a good day.')
            sys.exit()
           
        elif 'hello' in query or 'hi' in query:
            speak('Hello Sir')

        elif 'bye' in query:
            speak('Bye Sir, have a good day.')
            sys.exit()
        elif 'send a message' in query or 'open whatsapp' in query:
            speak('Sure thing, give me one minute to open Whatsapp')
            driver=webdriver.Chrome(executable_path="D:/chromedriver.exe")
            driver.get("https://web.whatsapp.com/")
            driver.maximize_window()
            speak('Please enter the details sir!!')
            name=input("Enter name or group name: ")
            speak('What should I say?')
            msg=myCommand()
            count=int(input("Enter count:"))
            speak('Please press any button after scanning QR code')
            input()
            user=driver.find_element_by_xpath("//span[@title='{}']".format(name))
            user.click()
            msg_box=driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]")
            for i in range(count):
                msg_box.send_keys(msg)
                driver.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[3]/button").click()
            speak('Message sent successfully')

            
        elif 'open a folder' in query or 'open a folder' in query or 'open file' in query or 'open a file' in query:
            speak('Please enter the directory')
            st=myCommand()
            speak('Please enter the folder name')
            fl=myCommand()
            y=st+"://"+fl
            os.startfile(y)
                                    
        elif 'play music' in query or 'play a song' in query:
            music_folder = 'D:\\Songs\\'
            music = ['SaahoreBaahubali','Samajavaragamana']
            random_music = music_folder + random.choice(music) + '.mp4'
            os.system(random_music)                  
            speak("Okay, here is your music! Enjoy!")
            sys.exit()
                  
            
            

        else:
            query = query
            speak('Searching...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('Got it.')
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('Google says - ')
                    speak(results)
        
            except:
                webbrowser.open('www.google.com')
        
        speak('Next Command! Sir!')

