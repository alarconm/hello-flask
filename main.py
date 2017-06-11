from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    '''Display home page'''
    return render_template('hello_form.html')


@app.route("/hello", methods=['POST'])
def hello():
    '''Get a text input from user, post it to the hello greeting page'''
    first_name = request.form['first_name']
    return render_template('hello_greeting.html', name=first_name)


@app.route('/validate-time')
def display_time_form():
    '''render the time form page'''
    return render_template('time_form.html')

def is_integer(num):
    '''takes in an argument, checks if its an integer, returns true/false'''
    try:
        int(num)
        return True
    except ValueError:
        return False


@app.route('/validate-time', methods=['POST'])
def validate_time():
    '''validate that user enters a valid number of hours(0-23) and minutes(0-59)
    give error message and don't accept input if not valid'''

    hours = request.form['hours']
    minutes = request.form['minutes']

    hours_error = ''
    minutes_error = ''

    if not is_integer(hours):
        hours_error = 'Not a valid integer'
        hours = ''
    else:
        hours = int(hours)
        if hours > 23 or hours < 0:
            hours_error = 'Hour value out of range (0-23)'
            hours = ''

    if not is_integer(minutes):
        minutes_error = 'Not a valid integer'
        minutes = ''
    else:
        minutes = int(minutes)
        if minutes > 59 or minutes < 0:
            minutes_error = 'Minutes value out of range(0-59)'
            minutes = ''

    #redirect when form submission is all valid
    if not minutes_error and not hours_error:
        time = str(hours) + ':' + str(minutes)
        return redirect('/valid-time?time={0}'.format(time))
    else:
        return render_template('time_form.html', hours_error=hours_error,
                               minutes_error=minutes_error, hours=hours, minutes=minutes)


@app.route('/valid-time')
def valid_time():
    '''Landing page when a valid integer is passed for hours and minutes on validate-time page'''
    time = request.args.get('time')
    return '<h1>You submitted {0}. Thanks for submitting a valid time!</h1>'.format(time)


tasks = []

@app.route('/todos', methods=['POST', 'GET'])
def todos():
    '''Add each input posted from todo.html to tasks list'''

    if request.method == 'POST':
        task = request.form['task']
        if task != '':
            tasks.append(task)

    return render_template('todos.html', title="TODOs", tasks=tasks)

app.run()