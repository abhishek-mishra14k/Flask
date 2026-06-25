from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)  #it can not be empty so nullabke is false 
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/' , methods=['GET' , 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
     
    return render_template('index.html',allTodo=allTodo)
    # return "Hello, World!"

@app.route('/show' )  #new endpoints
def abhishek():     
    allTodo = Todo.query.all()
    print(allTodo)
    return "this is my world!"

@app.route('/update/<int:sno>' , methods=['GET' , 'POST'] )  #new endpoints
def update(sno):     
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    return "this is my world!"

@app.route('/delete/<int:sno>' )  #new endpoints
def delete(sno):     
    allTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    with app.app_context():   # ✅ create tables inside app context
        db.create_all()
    app.run(debug=True , port=8003)  #if we do debug false then it will not tell the exact error it will just say internal server error

