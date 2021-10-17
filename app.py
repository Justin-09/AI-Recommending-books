from flask import Flask, render_template, request,redirect,url_for,session
import numpy as np
import cv2
import mysql.connector
from keras.models import load_model
import webbrowser
import os


app = Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="",database='finalform')
cursor=conn.cursor()

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

info = {}

haarcascade = "C:\\Users\\Nikhil\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\cv2\\data\haarcascade_frontalface_default.xml"
label_map = ['Anger', 'Neutral', 'Fear', 'Happy', 'Sad', 'Surprise']
print("+"*50, "loadin gmmodel")
model = load_model(r"C:\Users\Nikhil\Downloads\emotion-book\emotion-based-music-ai-main\model.h5")
cascade = cv2.CascadeClassifier(haarcascade)

@app.route('/')
def homes():
	return render_template('login.html')

@app.route('/login')
def logout():
	return render_template('login.html')

@app.route('/register')
def about():
	return render_template('register.html')

@app.route('/home')
def signin():
	return render_template('login.html')

@app.route('/home',methods=['POST'])
def home():
    email= request.form.get('email')
    password= request.form.get('password')


    cursor.execute("""SELECT * FROM `users`WHERE `email`LIKE '{}' AND `password`LIKE'{}'"""
            .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        
        return redirect('/index')
    else:
       
       return redirect('/')
@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cursor.execute("""INSERT INTO `users`(`user_id`,`name`,`email`,`password`)VALUES 
    (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    
    

    return redirect(url_for('home'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/choose_author', methods = ["POST"])
def choose_author():
	info['language'] = request.form['language']
	print(info)
	return render_template('choose_author.html', data = info['language'])


@app.route('/emotion_detect', methods=["POST"])
def emotion_detect():
	info['book'] = request.form['book']

	found = False

	cap = cv2.VideoCapture(0)
	while not(found):
		_, frm = cap.read()
		gray = cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)

		faces = cascade.detectMultiScale(gray, 1.4, 1)

		for x,y,w,h in faces:
			found = True
			roi = gray[y:y+h, x:x+w]
			cv2.imwrite("static/face.jpg", roi)

	roi = cv2.resize(roi, (48,48))

	roi = roi/255.0
	
	roi = np.reshape(roi, (1,48,48,1))

	prediction = model.predict(roi)

	print(prediction)

	prediction = np.argmax(prediction)
	prediction = label_map[prediction]

	cap.release()

	link  = f"https://www.google.com/search?tbm=bks&q={info['book']}+{prediction}+{info['language']}+book"
	webbrowser.open(link)

	return render_template("emotion_detect.html", data=prediction, link=link)

if __name__ == "__main__":
	app.run(debug=True)