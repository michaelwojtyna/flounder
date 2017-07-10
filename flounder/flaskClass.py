from jsonpickle import encode
import os
from flask import Flask
from flask import flash
from flask import abort, redirect, url_for
from flask import request
from flask import render_template
from flask import session
from userdao import UserDao
from user import User
from postingdao import PostingDao
from posting import Posting
import sys
import string
import random
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/student/csc324/Spring2017/flounder/pictures'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index(): 
    return redirect(url_for('home'))

@app.route('/home')
def home():
    dao = PostingDao()
    postings = dao.selectAll()
    userdao = UserDao()
    return render_template('home.html', **locals())

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    

    if request.method == 'POST':
        

        if (isValid(request.form['userid'], request.form['password']) and (request.form['userid']=='wgreelish' or request.form['userid']=='mwojtyna' or request.form['userid']=='dsmolinski' or request.form['userid']=='icornelius')):
           
            return redirect(url_for('adminHome'))
                    
        
        elif isValid(request.form['userid'], request.form['password']):
        
          
            return signedinHome()
            
            
        else:
            error = 'Invalid userid/password'

    return render_template('login.html', error = error)

@app.route('/adminHome', methods=['POST','GET'])
def adminHome():
    
    error = None
    userLogged = userLog
    userdao = UserDao()
    dao = PostingDao()
    postings = dao.selectAll()
    if('deleteAll' in request.form):
        
        session['value'] = request.form['deleteAll']
        return deleteAll()
    else:
        postings = dao.selectAll()
    return render_template('adminHome.html', **locals())
                                                

@app.route('/signedinHome', methods=['POST','GET'])
def signedinHome():
    userLogged = userLog
    userdao = UserDao()
    dao = PostingDao()
    postings = dao.selectAll()
    return render_template('signedinHome.html', **locals())

    
                    

def isValid(userid, password):
    
    global userLog
    userLog = userid
    dao = UserDao()
    user = dao.selectByUserid(userid)
    if(user is not None) and (userid == user.userid) and (password==user.password):
        session['user']=encode(user)
        return True
    else:
        return False

def isValidUsername(userid):
   
    userLog = userid
    dao = UserDao()
    user = dao.selectByUserid(userid)
    if(user is not None) and (userid == user.userid):
        session['user'] = encode(user)
        return True
    else:
        return False



def id_generator(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    

@app.route('/createaccount', methods=['POST','GET'])
def createaccount():
    error = None
    dao = UserDao()
   

    if request.method == 'POST':
        
        if request.form['password'] == request.form['confirmPassword']:
            
            if request.form['userid'] and request.form['password'] and request.form['email']:
                if dao.selectByUserid(request.form['userid']) is not None:
                    
                else:
                    
                    newUser = User(request.form['userid'], request.form['password'], request.form['email'])
                    dao.insert(newUser)
                    return redirect(url_for('login'))
                
                       
                
        
        
    return render_template('createaccount.html', **locals())

def deleteAll():
    
    
    error = None
    dao = PostingDao()
    userLogged = userLog
    userdao = UserDao()
    if('value' not in session):
        print 'Value not found in post data'
    else:
        value = session['value']
        dao.delete(value)
        
    postings = dao.selectAll()
    return render_template("adminHome.html", **locals())

def delete():
    error = None
    dao = PostingDao()
    userLogged =userLog
    if('value' not in session):
        print 'Value not found in post data'
    else:
        value = session['value']
        dao.delete(value)
    postings = dao.selectPostByUser(userLogged)
    return render_template("managePosts.html", **locals())

def admindelete():
    error = None
    dao = PostingDao()
    userLogged =userLog
    if('value' not in session):
        print 'Value not found in post data'
    else:
        value = session['value']
        dao.delete(value)
    postings = dao.selectPostByUser(userLogged)
    return render_template("adminmanagePosts.html", **locals())

                                            
    

@app.route('/lostit', methods=['POST', 'GET'])
def lostit():
    error = None
    userLogged =userLog
    dao = PostingDao()
    if request.method == 'POST':
        if request.form['item'] and request.form['description']:
            newPosting = Posting(userLogged, request.form['item'], request.form['description'], request.form['message'], 'lost', 0, id_generator(), request.form['date'])
            dao.insert(newPosting)
            
        
    return render_template('lostit.html', **locals())


@app.route('/adminlostit', methods=['POST', 'GET'])
def adminlostit():
    error = None
    userLogged =userLog
    dao = PostingDao()
    if request.method == 'POST':
        if request.form['item'] and request.form['description']:
            newPosting = Posting(userLogged, request.form['item'], request.form['description'], request.form['message'], 'lost', 0, id_generator(), request.form['date'])
            dao.insert(newPosting)

            
    return render_template('adminlostit.html', **locals())
                                                            

@app.route('/foundit', methods=['POST', 'GET'])
def foundit():
    error = None
    userLogged = userLog
    dao = PostingDao()
    if request.method == 'POST':
        if request.form['item'] and request.form['description']:
            newPosting = Posting(userLogged, request.form['item'], request.form['description'], request.form['message'], 'found', 0, id_generator(), request.form['date'])
            dao.insert(newPosting)

                                    
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename=='':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(newPosting.value) + ".png"))
            return redirect(url_for('foundPosting',filename=filename))
      
                                            
        
                                            
    return render_template('foundit.html', **locals())

@app.route('/pictures/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/adminfoundit', methods=['POST', 'GET'])
def adminfoundit():
    error = None
    userLogged = userLog
    dao = PostingDao()
    if request.method == 'POST':
        if request.form['item'] and request.form['description']:
            newPosting = Posting(userLogged, request.form['item'], request.form['description'], request.form['message'], 'found', 0, id_generator(), request.form['date'])
            dao.insert(newPosting)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file and allowed_file(file.filename):
            
            
            filename=secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(newPosting.value) + ".png"))
            return redirect(url_for('adminfoundPosting',filename=filename))
                                                                                                                    
            
    return render_template('adminfoundit.html', **locals())
                                                            
    
@app.route('/lostpostings', methods=['POST', 'GET'])
def lostPostings():
    error = None
    userdao = UserDao()
    dao = PostingDao()
    postings = dao.selectByStatus('lost')
    return render_template('lostpostings.html', **locals())

@app.route('/foundposting', methods=['POST', 'GET'])
def foundPosting():
    error = None
    userdao = UserDao()
    dao = PostingDao()
    userLogged = userLog
    postings = dao.selectByStatus('found')
    return render_template('foundposting.html', **locals())

@app.route('/adminfoundposting', methods=['POST', 'GET'])
def adminfoundPosting():
    error = None
    userdao = UserDao()
    dao = PostingDao()
    userLogged = userLog
    postings = dao.selectByStatus('found')
    filename=secure_filename('nopics.png')
    return render_template('adminfoundposting.html', **locals())

@app.route('/adminlostpostings', methods=['POST', 'GET'])
def adminlostPostings():
    error = None
    userdao = UserDao()
    dao = PostingDao()
    userLogged = userLog
    usernames = userdao.selectByUserid(userLogged)
    postings = dao.selectByStatus('lost')
    return render_template('adminlostpostings.html', **locals())
                    
                    
@app.route('/managePosts', methods=['POST', 'GET'])
def managePosts():
    error = None
    dao = PostingDao()
    userLogged =userLog
    postings = dao.selectPostByUser(userLogged)
    if('delete' in request.form):
        session['value'] = request.form['delete']
        return delete()
    else:
        postings = dao.selectPostByUser(userLogged)
        return render_template('managePosts.html', **locals())
    
@app.route('/adminmanagePosts', methods=['POST', 'GET'])
def adminmanagePosts():
    error = None
    dao = PostingDao()
    userLogged =userLog
    postings = dao.selectPostByUser(userLogged)
    if('delete' in request.form):
        session['value'] = request.form['delete']
        return admindelete()
    else:
        postings = dao.selectPostByUser(userLogged)
        return render_template('adminmanagePosts.html', **locals())
                                        
    

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', debug=True)
