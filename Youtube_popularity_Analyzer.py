from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from selenium import webdriver
#from bs4 import BeautifulSoup as parser
from time import sleep
from textblob import TextBlob
import os
import matplotlib.pyplot as plt
from subprocess import Popen
from math import sqrt
os.environ['MOZ_HEADLESS'] = '1'
profile = webdriver.FirefoxProfile()
ui = Tk()
ui.minsize(300,100)
ui.title("YOUTUBE COMMENT ANALYZER")
w1 = Label(ui,text="Enter the term:",font=("Arial Bold",10))
w2 = Entry(ui)
def onclick(ev):
    messagebox.showinfo("Engagement Value","Your Engagement value is "+str(round(ev%sqrt(2)*100,3))+"%")
def yt_plt(pv,sv):
    plt.figure()
    plt.suptitle("Engagement Plot")
    plt.title("(Far from origin is better)")
    plt.xlim((-1, 1))
    plt.xlabel("polarity")
    plt.ylim((0, 1))
    plt.ylabel("subjectivity")
    plt.plot([0, 0], [-1, 1], linewidth=2, color='black')
    plt.plot(pv, sv, 'ob')
    plt.show()
def yt_main(term):
    f = open("yt-cmt", "w", encoding="utf-8",errors="ignore")
    driver = webdriver.Firefox(executable_path="C:\\Users\\parat\\PycharmProjects\\NewOne\\geckodriver\\geckodriver.exe")
    driver.get("https://www.youtube.com/watch?v=" + term)
    driver.execute_script('window.scrollTo(1, 500);')

    # now wait let load the comments
    sleep(15)

    driver.execute_script('window.scrollTo(1, 3000);')

    comment_div = driver.find_element_by_xpath('//*[@id="contents"]')
    comments = comment_div.find_elements_by_xpath('//*[@id="content-text"]')
    for comment in comments:
        print(comment.text)
        f.write(comment.text + '\n')
    f = open("yt-cmt", "r", errors="ignore")
    blob = TextBlob(f.read())
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    engagement_value = sqrt(polarity*polarity+subjectivity*subjectivity)
    print(polarity)
    print(subjectivity)
    print(engagement_value)
    w4 = Label(ui,text = 'The Engagement and subjectivity value is ('+str(round(polarity,3))+','+str(round(subjectivity,3))+')')
    w4.grid(column = 0,row = 1,columnspan=3)
    w5 = Button(ui,text="Generate graph",command=lambda:yt_plt(polarity,subjectivity))
    w5.grid(column = 0,row = 2)
    w6 = Button(ui,text="comments",command=lambda:Popen(["notepad.exe","yt-cmt" ]) )
    w6.grid(column = 1,row = 2)
    w7 = Button(ui,text="Engagement value", command=lambda : onclick(engagement_value))
    w7.grid(column = 2,row = 2)
    driver.close()
    f.close()
    driver.quit()
w3 = Button(ui,text="Analyze",command=lambda: yt_main(w2.get()))
w1.grid(column=0,row=0)
w2.grid(column=1,row=0)
w3.grid(column=2,row=0)
ui.mainloop()
