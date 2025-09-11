from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)

    def __init__(self, id, name, importance, date):
        self.id = id
        self.name = name
        self.importance = importance
        self.date = date

    def __repr__(self):
        return f"Task(name={self.name}, importance={self.importance}, date={self.date})"

#db.create_all() # database dosyası açmak için şunu 1 kere yazıp runla sonra sil


task_post_args = reqparse.RequestParser()
task_post_args.add_argument("name", type=str, help="enter valid name", required=True)
task_post_args.add_argument("importance", type=int, help="enter valid importance", required=True)
task_post_args.add_argument("date", type=str, help="enter valid date", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("name", type=str, help="enter valid name")
task_put_args.add_argument("importance", type=int, help="enter valid importance")
task_put_args.add_argument("date", type=str, help="enter valid date")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "importance": fields.Integer,
    "date": fields.String
}

class Task(Resource):
    @marshal_with(resource_fields)
    def get(self, task_id):
        result = TaskModel.query.filter_by(id = task_id).first()
        if not result:
            abort(404, message="couldnt find task")
        return result

    @marshal_with(resource_fields)
    def post(self, task_id):
        args = task_post_args.parse_args()

        result = TaskModel.query.filter_by(id = task_id).first()
        if result:
            abort(409, message="task id taken")

        task = TaskModel(id=task_id, name=args["name"], importance=args["importance"], date=args["date"])
        db.session.add(task)
        db.session.commit()
        return task, 201

    @marshal_with(resource_fields)
    def put(self, task_id):
        args = task_put_args.parse_args()

        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="couldnt find task")

        for arg in args:
            if args[arg]:
                setattr(result, arg, args[arg])

        db.session.commit()
        return result, 200

    def delete(self, task_id):
        result = TaskModel.query.filter_by(id=task_id).first()
        if not result:
            abort(404, message="couldnt find task")

        db.session.delete(result)
        db.session.commit()
        return "", 204

class TaskList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        tasks = TaskModel.query.all()
        return tasks

class Entry(Resource):
    def get(self):
        return "hello"

@app.route("/tasks_html")
def tasks_html():
    tasks = TaskModel.query.all()
    return render_template("index.html", tasks=tasks)

api.add_resource(Task, "/task/<int:task_id>")
api.add_resource(TaskList, "/tasks")
api.add_resource(Entry, "/")

if __name__ == "__main__":
    app.run(debug=True)