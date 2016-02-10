import requests
import json
from flask import Flask, request, redirect, url_for, \
    render_template, flash,jsonify


# configuration

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'gofaniyi.test1@gmail.com'
PASSWORD = 'pass1234'

# create our little application :)
application = Flask(__name__)
application.config.from_object(__name__)


@application.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form['username'] != application.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != application.config['PASSWORD']:
            error = 'Invalid password'
        else:
            return get_credentials(
                request.form['username'], request.form['password'])
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('home.html')


def get_credentials(username, password):
    BASE_URL = 'https://sandbox.seegad.com/api/users'

    v = requests.post('{}/login'.format(BASE_URL),
                      data=json.dumps({'username': username, 'password': password}),
                      headers={'content-type': 'application/json'}, verify=False)
    if v.status_code == 200:
        y = v.json()

        z = requests.get('{}/{}'.format(BASE_URL, y.get('userId')),
                                        headers={'content-type': 'application/json', 'authorization': y.get('id')},
                                        verify=False)
        return jsonify(z.json())


if __name__ == '__main__':
    application.run(host='0.0.0.0')
