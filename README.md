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
app.json - for Heroku, Describe project information.
getpac.py - app script.
manifest.yml - for IBM Cloud Foundary, includes basic information about your app, such as the name, how much memory to allocate for each instance and the route.
pac/ - pac file.
Procfile - to explicitly declare what command should be executed to start your app.
README.md
requirements.txt - requirements file, which is used by Python’s dependency manager.
runtime.txt - for Heroku (optional), specifying Python version.

about [Procfile](https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile)

## how to use

### on a host
1. install requirements
`pip3 install -r requirements.txt`
2. run app
You can run it directly in python, though it's best deployed through a WSGI (uWSGI, FastCGI) service.

### on [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)

```bash
# creat an new app
heroku create
```
1. init git repo and connet app repo on Heroku
```bash
git init
heroku git:remoter -a appname # <appname> is Heroku app name
```
2. deploy on Heroku
```bash
git add .
git commit -m "commit info"
git push heroku master  # push to master branch            
```

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

