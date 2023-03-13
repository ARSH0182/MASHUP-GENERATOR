from flask import Flask, request
import re
import random
import os
from pytube import YouTube
from pydub import AudioSegment
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import urllib.request
from email import encoders

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        X = request.form['singer_name']
        N = int(request.form['num_videos'])
        Y = int(request.form['duration'])
        email = request.form['email']
        
        X=X.lower()
        X=X.replace(" ", "")+"videosongs"
        
        html=urllib.request.urlopen("https://www.youtube.com/results?search_query="+X)
        video_ids=re.findall(r"watch\?v=(\S{11})" , html.read().decode())
        
        l=len(video_ids)
        url = []
        for i in range(N):
            url.append("https://www.youtube.com/watch?v=" + video_ids[random.randint(0,l-1)])
        
        final_aud = AudioSegment.empty()
        for i in range(N):   
            audio = YouTube(url[i]).streams.filter(only_audio=True).first()
            audio.download(filename='Audio-'+str(i)+'.mp3')
            aud_file = str(os.getcwd()) + "/Audio-"+str(i)+".mp3"
            file1 = AudioSegment.from_file(aud_file)
            extracted_file = file1[:Y*1000]
            final_aud +=extracted_file
            final_aud.export('mashup.mp3', format="mp3")
            
        sender_email = "arshkathpal182@gmail.com" # Put your email address here
        sender_password = "Arsh@0724" # Put your email password here
        receiver_email = email
        subject = "Mashup Audio File"
        message = "Please find the attached mashup audio file."
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        filename = "mashup.mp3"
        attachment = open(filename, "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
        except:
            print("Could not send email.")
        
        return "Mashup audio file sent to " + email + " successfully!"
    
    return '''
        <html>
            <body>
                <h2>Create Mashup Audio File</h2>
                <form method="post">
                    Singer Name: <input type="text" name="singer_name">
                    Number of Videos: <input type="number" name="num_videos">
                    Duration (in seconds): <input type="number" name="duration">
                    Email: <input type="email" name="email">
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

