from tkinter import *
from tkinter import messagebox
from selenium import webdriver
#from bs4 import BeautifulSoup as parser
import time
from textblob import TextBlob
import os
import matplotlib.pyplot as plt
import subprocess
import math
os.environ['MOZ_HEADLESS'] = '1'
profile = webdriver.FirefoxProfile()
ui = Tk()
ui.minsize(300,100)
ui.title("YOUTUBE COMMENT ANALYZER")
w1 = Label(ui,text="Enter the term:",font=("Arial Bold",10))
w2 = Entry(ui)
def onclick(EV):
    messagebox.showinfo("Engagement Value","Your Engagement value is "+str(round(EV*100,3))+"%")
def Yt_plt(pv,sv):
    plt.figure()
    plt.title("Engagement Plot")
    plt.xlim((-1, 1))
    plt.xlabel("polarity")
    plt.ylim((0, 1))
    plt.ylabel("subjectivity")
    plt.plot([0, 0], [-1, 1], linewidth=2, color='black')
    plt.plot(pv, sv, 'ob')
    plt.show()
def Yt_Main(term):
    f = open("yt-cmt", "w", encoding="utf-8",errors="ignore")
    driver = webdriver.Firefox(executable_path="C:\\Users\\parat\\PycharmProjects\\NewOne\\geckodriver\\geckodriver.exe")
    driver.get("https://www.youtube.com/watch?v=" + term)
    driver.execute_script('window.scrollTo(1, 500);')

    # now wait let load the comments
    time.sleep(15)

    driver.execute_script('window.scrollTo(1, 3000);')

    comment_div = driver.find_element_by_xpath('//*[@id="contents"]')
    comments = comment_div.find_elements_by_xpath('//*[@id="content-text"]')
    for comment in comments:
        print(comment.text)
        f.write(comment.text + '\n')
    f = open("yt-cmt", "r", errors="ignore")
    blob = TextBlob(f.read())
    Polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    Engagement_Value = math.sqrt(Polarity*Polarity+subjectivity*subjectivity)
    print(Polarity)
    print(subjectivity)
    print(Engagement_Value)
    w4 = Label(ui,text = 'The Engagement and subjectivity value is ('+str(round(Polarity,3))+','+str(round(subjectivity,3))+')')
    w4.grid(column = 0,row = 1,columnspan=3)
    w5 = Button(ui,text="Generate graph",command=lambda:Yt_plt(Polarity,subjectivity))
    w5.grid(column = 0,row = 2)
    w6 = Button(ui,text="comments",command=lambda:subprocess.Popen(["notepad.exe","yt-cmt" ]) )
    w6.grid(column = 1,row = 2)
    w7 = Button(ui,text="Engagement value", command=lambda : onclick(Engagement_Value))
    w7.grid(column = 2,row = 2)
    driver.close()
    f.close()
    driver.quit()
w3 = Button(ui,text="Analyze",command=lambda: Yt_Main(w2.get()))
w1.grid(column=0,row=0)
w2.grid(column=1,row=0)
w3.grid(column=2,row=0)
ui.mainloop()
