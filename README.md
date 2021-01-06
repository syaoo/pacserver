A simple website for generating pac, with customizable ports (default 1080).Can be deployed to a host such as vps or hosted on a provider such as Heroku.if you want use port 1088,you can use :`host/pac?p=1088`

## file structure
```
.
├── app.json
├── getpac.py
├── manifest.yml
├── pac
│   ├── gfwlist.txt
│   └── user-rules.txt
├── Procfile
├── README.md
├── requirements.txt
└── runtime.txt
```
`app.json` - for Heroku, Describe project information.  
`getpac.py` - app script.  
`manifest.yml` - for IBM Cloud Foundary, includes basic information about your app, such as the name, how much memory to allocate for each instance and the route.  
`pac/` - pac file.  
`Procfile` - to explicitly declare what command should be executed to start your app.  
`README.md`  
`requirements.txt`  - requirements file, which is used by Python’s dependency manager.   
`runtime.txt` - for Heroku (optional), specifying Python version.   

about [Procfile](https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile)

## how to use

### Create a LeanCloud acount and get AppID and AppKey
1. If you don't have a LeanCloud account, register it at https://leancloud.app/
2. Creat a LeanCloud app and get  AppID and AppKey at `Settings`-`App keys`

### on a host
1. install requirements
`pip3 install -r requirements.txt`

2. set `LC_APPID` and `LC_APPKEY`
```shell
export LC_APPID=AppId
export LC_APPKEY=AppKey
```

3. run app
You can run it directly in python, though it's best deployed through a WSGI (uWSGI, FastCGI) service.

### on [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

1. Login herku and creat an app
```bash
# login heroku
herku login
# creat an new app
heroku create appname
```

2. init git repo and connet app repo on Heroku
```bash
git init
heroku git:remoter -a appname # <appname> is Heroku app name
```
3. If it is an existing project
```bash
# add remote
git remote add heroku herokuapp-git-url
```

4. Setting environment variables
```bash
heroku config:set LC_APPID=AppId
heroku config:set LC_APPKEY=AppKey
# check variables
heroku config
```

5. deploy on Heroku
```bash
# push to heroku
git add .
git commit -m "commit info"
git push heroku master  # push to master branch 
# or
git push heroku otherbranch:master 
```
#### ERROR

##### Error H10
1.Setting a PORT as a Heroku environment variable
```python
port = int(os.getenv('PORT', 8000))
```
2.Missing Required Environment Variable 

[Heroku Error Codes](https://devcenter.heroku.com/articles/error-codes#h10-app-crashed)

### on IBM Cloud

1. set up a manifest.yml file,like this:
```yaml
  applications:
  - name: GetStartedPython
    random-route: true
    memory: 128M
```
<name> is your app name.

2. push to IBM Cloud
```bash
ibmcloud cf push
```
When deployment completes you should see a message indicating that your app is running. You can also issue the following command to view your apps status and see the URL.
```bash
ibmcloud cf apps
```

**Befor deploy to Heroku or IBM Cloud you need login your account.**

### Database
I found Heroku does not support SQLite, it will lose the entire database at least every 24 hours, this has mentioned in Heroku's official document, and they recommend using PostgreSQL. In addition to PostgreSQL, I found [LeanCloud](https://leancloud.app) or [MongoDBAtlas](https://www.mongodb.com/cloud/atlas/) may be also a good choice, I'll test LeanCloud later. 

## Changelog
- 2021.01.04: use LeanCloud save date.,add user parameter: http://hostname/pac?p=post&u=username&t=False.