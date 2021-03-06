from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)


contact = [
  {'name': 'João da Silva', 'email': 'joao@gmail.com', 'phone': '(16) 99922-1122'},
  {'name': 'Maria Souza', 'email': 'maria1@gmail.com', 'phone': '(16) 99922-3333'}
]



class users (db.Model) :
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  password = db.Column(db.String())
  created_at = db.Column(db.String())
  uodated_at = db.Column(db.String())

class contacts (db.Model) : 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  phone = db.Column(db.String())
  image = db.Column(db.String())
  user_id = db.Column(db.Integer)
  created_at = db.Column(db.String())
  uodated_at = db.Column(db.String())



@app.route('/login')
def login():
 return render_template('login.html')


@app.route('/signin', methods=['POST'])
def signin():
   email = request.form.get('email')
   password = request.form.get('password')
   user = users.query.filter_by(email=email).first()
   if not user:
      return redirect('/login')
   if not check_password_hash(user.password, password):
      return redirect('/login')
   else:
      session['user_id'] = user.id
      return redirect('/')


@app.route('/signup', methods=['POST'])
def signup():
 name = request.form.get('name')
 email = request.form.get('email')
 password = request.form.get('password')
 user = users.query.filter_by(email=email).first()
 if user:
   return redirect('/register')
 new_user = users(
 email=email, name=name,
 password=generate_password_hash(password, method='sha256')
 )
 db.session.add(new_user)
 db.session.commit()
 return redirect('/login')


@app.route('/register')
def register():
 return render_template('register.html')

@app.route('/')
def index():
 if 'user_id' not in session:
   return redirect('/login')
 else:
   new_todo = contacts.query.all()
 return render_template('index.html',contact=contact, new_todo=new_todo)


@app.route('/create', methods=['POST'])
def create():
 name = request.form.get('name')
 email = request.form.get('email')
 phone = request.form.get('phone')
 new_todo = contacts(name=name, email=email, phone = phone)
 db.session.add(new_todo)
 db.session.commit()
 return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
 if 'user_id' not in session:
   return redirect('/login')
 todo = contacts.query.filter_by(id=id).first()
 db.session.delete(todo)
 db.session.commit()
 return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
 if 'user_id' not in session:
   return redirect('/login')
 todo = contacts.query.filter_by(id=id).first()
 todo.complete = True
 db.session.commit()
 return redirect('/')

  
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
 if 'user_id' not in session:
   return redirect('/login')
 name = request.form.get('name')
 email = request.form.get('email')
 phone = request.form.get('phone')
 todo = contacts.query.filter_by(id=id).first()
 todo.name = name
 todo.email = email
 todo.phone = phone
 db.session.commit()
 return redirect('/')

@app.route('/logout')
def logout():
 if 'user_id' in session:
   session.pop('user_id', None)
   return redirect('/')



if __name__ == '__main__':
  db.create_all()
  app.run(host= '0.0.0.0', port=8080)
