from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)        # intialise the database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)       # we dont want it to be left blank so nullabe is False
    date_created = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return '<Task %r>' % self.id    # return the ask and the id of the task created

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =="POST":
        task_content = request.form['content']          #task_content is equal to the form's content
        new_task = Todo(content = task_content)                                              # creating a todo object for the todo model
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Problem occured while adding this task"
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)          # gets the task by the id and if not found gives a 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Problem occured while deleting this task"
    
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)  
    if request.method =='POST':
        task.content = request.form['content']    # settinf current task content to content in the input box
        

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Problem occured while updating this task"
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug= True)