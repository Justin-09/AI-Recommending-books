from flask import Flask,render_template,request,redirect,session,flash
from flask.helpers import url_for
import mysql.connector
import os


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="",database='finalform')
cursor=conn.cursor()
@app.route('/')
def homes():
    return render_template('login.html')
@app.route('/book')
def book():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
@app.route('/register')
def about():
    return render_template('register.html')
@app.route('/home',methods=['POST'])
def home():
    email= request.form.get('email')
    password= request.form.get('password')


    cursor.execute("""SELECT * FROM `users`WHERE `email`LIKE '{}' AND `password`LIKE'{}'"""
            .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        flash("you are successfuully login")
        return redirect('/index')
    else:
       flash('please enter correct user name and password')
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
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('home')

@app.route('/forget_password')
def forget():
    return render_template('forget_password.html')
@app.route('/forget_pass',methods=['POST'])
def forget_pass():
    email=request.form.get('femail')
    password=request.form.get('fpassword')
    cursor.execute( """UPDATE `users`SET`password`=`{}`WHERE `email`=`{}` """.format(password,email))
    
    conn.commit()
    
    return redirect(url_for('home'))
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/choose_singer')
def choose_singer():
    return "hii bhailo kaise ho"
@app.route('/emotion_detect')
def emotion_detect():
    return render_template('emotion_detect')
    
    



    
    

    


    
   

    


if __name__=="__main__":
    app.run(debug=True)