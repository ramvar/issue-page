
from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from datetime import datetime
import re

app=Flask(__name__)

#mail= Mail(app)

mysql = MySQL()
  
# configuring MySQL for the web application
app.config['MYSQL_DATABASE_USER'] = 'root'    # default user of MySQL to be replaced with appropriate username
app.config['MYSQL_DATABASE_PASSWORD'] = 'Myjesus1' # default passwrod of MySQL to be replaced with appropriate password
app.config['MYSQL_DATABASE_DB'] = 'issueprofile'  # Database name to be replaced with appropriate database name
app.config['MYSQL_DATABASE_HOST'] = 'localhost' # default database host of MySQL to be replaced with appropriate database host
#initialise mySQL
mysql.init_app(app)
#create connection to access data
conn = mysql.connect()
  
    
@app.route('/')
def index():
      cursor = conn.cursor()
      cursor.execute('SELECT issuename FROM issuedb where resolution is NOT NULL')
      issues = cursor.fetchall()
      return render_template("display.html", issues=issues)
       
@app.route('/resolution',methods=["POST"])
def resolution():
    if request.method =="POST":
        if request.form['submit-button'] == 'Show':
           name1 = request.form.get('issuename')
           display(name1)
           cursor = conn.cursor()
           cursor.execute('SELECT resolution FROM issuedb WHERE issuename = % s', (name1))
           resolve = cursor.fetchone()    
           display(resolve)
           return render_template("resolution.html", msg = resolve)
        elif request.form['submit-button'] == 'Post My Issue':
           new = request.form.get('newissue')
           display(new)
           cursor = conn.cursor()
           cursor.execute('INSERT INTO issuedb(issuename) VALUES (%s)', (new))
           conn.commit()
           display ('success')
           return render_template("close.html")

@app.route('/add')
def add():    
      return render_template("add.html")

@app.route('/addissue',methods=["POST"])
def addissue():    
     if request.method=='POST':
       if request.form['submit-button'] == 'Add':
          now    = datetime.now()
          adddt  = now.strftime('%Y-%m-%d')
          addiss = request.form.get('addissue')
          addres = request.form.get("addres")
          cursor = conn.cursor()
          cursor.execute('INSERT INTO issuedb(issuename,resolution,Date_issue) VALUES (%s,%s,%s)', (addiss,addres,adddt))
          conn.commit()
          return render_template("close.html")
         
@app.route('/update')
def update():
      cursor = conn.cursor()
      cursor.execute('SELECT issuename FROM issuedb where resolution is NULL')
      upd = cursor.fetchall()
      print(upd)
      return render_template("update.html", upd=upd)

@app.route('/updateissue',methods=["POST"])
def updateissue():    
      if request.method=='POST':
         if request.form['submit-button'] == 'Update':
#             upd1 = document.getElementById("updname").value
             upd1 = request.form.get("updname")
#             upd1 = request.form['updname']
             display(upd1)
             updname = request.form.get("updissue")
             display(updname)
             cursor = conn.cursor()
             cursor.execute('UPDATE issuedb set resolution = %s where issuename = %s', (updname,upd1))
             conn.commit()
             return render_template("close.html")

            
@app.route('/close',methods=["POST"])
def close():
    return render_template("close.html")
        
if __name__ == "__main__":
    app.run(host ="localhost", debug = True , use_reloader=False , port = int("5000"))
