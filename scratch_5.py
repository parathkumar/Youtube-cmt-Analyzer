from tkinter import *
from selenium import webdriver
#from bs4 import BeautifulSoup as parser
import time
from textblob import TextBlob
import os
os.environ['MOZ_HEADLESS'] = '1'
profile = webdriver.FirefoxProfile()
profile.set_preference("media.volume_scale", "0.0")
ui = Tk()
ui.minsize(300,100)
ui.title("YOUTUBE COMMENT ANALYZER")
w1 = Label(ui,text="Enter the term:",font=("Arial Bold",10))
w2 = Entry(ui)
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
    print(blob.sentiment.polarity)
    driver.close()
    f.close()
    driver.quit()
w3 = Button(ui,text="Analyze",command=lambda: Yt_Main(w2.get()))
w1.grid(column=0,row=0)
w2.grid(column=1,row=0)
w3.grid(column=2,row=0)
ui.mainloop()