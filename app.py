from flask import Flask, request, redirect, url_for, render_template, flash

from datetime import date
from model import *
from flask import Flask
from flask.globals import session

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = 'aoaoaosudoaooaoaoaoaoao'

@app.route('/login/', methods=['GET'])
def Get():
    msg = request.args.get('msg', None)
    return render_template('login.html', msg = msg)
    
    
@app.route('/login/', methods=['POST'])
def Check():
    _username =  request.form['username']
    _password = request.form['password']
    user = Users.get_or_none(_username == Users.username)
    if user == None:
        return redirect('/login/?msg=Такой пользователь остуствует')
    if _password != user.password:
        return redirect('/login/?msg=Неправильный пароль')
    session['username'] = user.username
    session['userid'] = user.id
    return redirect('/')


@app.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register/', methods=['POST'])
def Save_User():
    _username =  request.form['username']
    _password = request.form['password']
    _name = request.form['name']
    _email = request.form['email']
    _phone = request.form['phone']
    Users(
        username = _username,
        password = _password,
        name = _name,
        email = _email,
        phone = _phone
    ).save()
    flash('New entry was successfully posted')
    return redirect('/login/')
    
 

def check_session():
    if not 'username' in session:
        return redirect('/login/')

def GetName():
    username = Users.select().where(Users.id == session['userid'])
    return username

@app.route('/')
def show_entries():
    check_session()
    data = BlogPost.select()
    return render_template('show_entries.html', data=data)

@app.route('/post/<id>')
def show_post(id):
    data = BlogPost.get(id = id)
    comment = Comments.select().where(Comments.id == id)
    return render_template('post.html', data=data, comment =comment)


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if not 'username' in session:
        return redirect('/login/')
    if request.method == 'POST':
        BlogPost(
            title = request.form.get('title'),
            text = request.form.get('description'),
            published = date.today(),
            ownerusername = session['userid']
        ).save()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))
    return render_template('add.html')

@app.route('/createcomment/<id>', methods = ['POST'])
def CreateComment(id):
    _postid = id
    _ownerusername = session['userid']
    _text = request.form.get('comment')
    cmnt = Comments(postid = _postid, text = _text, ownerusername = _ownerusername)
    cmnt.save()
    return redirect('/post/'+str(id))

@app.route("/post/like/<id>", methods=['POST'])
def LikePost(id):
    _postid = id
    query = BlogPost.update(likes=BlogPost.likes + 1).where(BlogPost.id == _postid)
    query.execute()
    return redirect('/post/'+str(id))

@app.route("/post/dislike/<id>", methods=['POST'])
def DislikePost(id):
    _postid = id
    query = BlogPost.update(dislikes=BlogPost.dislikes + 1).where(BlogPost.id == _postid)
    query.execute()
    return redirect('/post/'+str(id))


if __name__ == '__main__':
    app.run(debug=True)
