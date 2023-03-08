from gtts import gTTS
myobj = gTTS(text="Hello world", lang="en",slow=False)#,tld="co.in")
myobj.save("welcome.mp3")