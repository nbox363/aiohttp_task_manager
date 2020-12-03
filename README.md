# Flask task manager

It's an app that has been created as a test-task for "Appvelox" company


# Install 

```bash
$ git clone https://github.com/nbox363/flask_task_manager
$ cd flask_task_manager
```

Create a virtualenv and activate it:
```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

Install pip packages:
```bash
$ pip install -r requirements.txt
```

# Run
```bash
$ flask init-db
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ flask run
```

Visit http://127.0.0.1:5000/
