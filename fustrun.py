from flask import Flask, url_for, redirect, render_template ,make_response,request
import os
import json
app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

# home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# login page
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user1']
        return username
        # if username == 'kur0mi':
        #     return 'login success.'
        # else:
        #     return 'login failed.'
    return render_template('login.html')

# get pac file
@app.route('/pac/<fname>')
def info(fname):
    directory = "/home/astro/test/static/"
    resp = make_response(open(directory+fname).read())
    resp.headers["Content-type"]="application/json;charset=UTF-8"
    return resp

if __name__ == '__main__':
    # app.run() # only localhost
    app.run(host='0.0.0.0',debug=True,port=5001)
    # open debug mode (auto apply code modify) or use this : app.debug = True
