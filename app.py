from flask import Flask, render_template, session, redirect, url_for, \
    g, request,flash, make_response
import sqlite3, os


app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
app.config.update(dict(
    DATABASE='./resources/user-rules1.db',
    #DEBUG=True,
    SECRET_KEY='development key',
))

class sqlHandler:
    def __init__(self,dbPath):
        self.dbPath=dbPath
        self.connect = self.conndb()

    def conndb(self):
        conn=sqlite3.connect(self.dbPath)
        conn.row_factory=sqlite3.Row
        return conn
    
    def exeScript(self,dbScript):
        with self.connect:
            with open(dbScript,'r') as f:
                cur=self.connect.executescript(f.read())
        return cur

    def exeOne(self,sql):
        with self.connect:
            cur = self.connect.execute(sql)
        return cur
    def close(self):
        self.connect.close()
@app.route('/export')
# def exportPAC(db,PAC):
def exportPAC():
    pac='./resources/user-rules.txt'
    db=sqlHandler(app.config['DATABASE'])
    cur = db.exeOne("SELECT * FROM rules")
    with open(pac,'w') as f:
        for i in cur.fetchall():
            f.write(i['rule'])
            f.write('\n')
    return('Export Ok!')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        db=sqlHandler(app.config['DATABASE'])
        email=request.form['log']
        passwd = request.form['pwd']
        cur=db.exeOne('SELECT * FROM USERS WHERE email="{}"'.format(email))
        res=cur.fetchone()
        if res==None:
            error = "用户不存在"
            return render_template('login.html',error=error)
        else:
            print(passwd)
            print(res['passwd'],res['name'])
            print(passwd==res['passwd'])
            print(type(passwd))
            print(type(res['passwd']))
            if passwd==res['passwd']:
                session['logged_in'] = True
                session['username'] = res['name']
                flash('登录成功')
                return redirect(url_for('index'))
            else:
                error="密码错误"
                # flash(error)
                # return render_template('login.html')
                return render_template('login.html',error=error)
        # else:
            # flash('email or password error')
            # return render_template('login.html')
            # return render_template('login.html',error='email or password error')
    return render_template('login.html')

@app.route('/')
def index():
    if session.get('logged_in'):
        db=sqlHandler(app.config['DATABASE'])
        cur=db.exeOne('SELECT * FROM rules')
        items = cur.fetchall()
        return render_template('index.html',rules=items)
    else:
        return redirect(url_for('login'))
@app.route('/add',methods=['POST'])
def add_item():
    rule=request.form['rule']
    db=sqlHandler(app.config['DATABASE'])
    c=db.exeOne("INSERT INTO rules (rule) VALUES ('{}')".format(rule))
    print(c.rowcount)
    print(len(c.fetchall()))
    db.close()
    return redirect(url_for('index'))

@app.route('/del/<string:id>',methods=['POST'])
def del_item(id):
    db=sqlHandler(app.config['DATABASE'])
    db.exeOne('DELETE FROM rules WHERE id="{}"'.format(id))
    # item = cur.fetchone()
    db.close()
    return redirect(url_for('index'))

@app.route('/edit/<string:id>',methods=['GET','POST'])
def edit_item(id):
    # 未完成
    db=sqlHandler(app.config['DATABASE'])
    cur = db.exeOne('SELECT * FROM rules WHERE id="{}"'.format(id))
    item = cur.fetchone()
    db.close()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/pac')
def pac():
    cdir = os.path.dirname(__file__)
    print(cdir)
    # pdir = cdir+"/pac/" # source file path is different when debug is off or on.
    pdir = "resources/"
    port = request.args.get('p')
    if port == None:
        return "plz use url like this: 'host/pac?p=1801'"
    if port == '':
        port = '1080'

    ###########################
    #  method a
    ###########################
    # !! this method can not update web page immediately
    # cmd = 'genpac --pac-proxy "SOCKS5 127.0.0.1:%s" --output="%sautoproxy.pac" --gfwlist-local "%s/gfwlist.txt"' %(port,pdir,pdir)
    # # genpac ref this: https://github.com/JinnLynn/genpac
    # # -o FILE, --output FILE 输出到文件, 无此参数或FILE为-, 则输出到stdout
    # os.popen(cmd)
    # resp = make_response(open(pdir+"autoproxy.pac").read())

    ###########################
    #  method b
    ###########################
    # Recommend this method
    cmd = 'genpac --pac-proxy "SOCKS5 127.0.0.1:%s" --gfwlist-local "%s/gfwlist.txt" --user-rule-from "%s/user-rules.txt"' %(port,pdir,pdir)
    gfwlist = os.popen(cmd)
    resp = make_response(gfwlist.read())

    resp.headers["Content-type"]="application/json;charset=UTF-8"
    return resp

def create_user(db,name,email,passwd):
    try:
        sql="INSERT INTO users (name,email, passwd) VALUES ('{}','{}','{}')".format(name,email,passwd)
        print(sql)
        db.exeOne(sql)
    except Exception as e:
        print(e)

def initdb(db):
    try:
        db.exeScript('./resources/init.sql')
    except Exception as e:
        raise e
        
if __name__ == "__main__":
    # init database
    if False:
        db=sqlHandler(app.config['DATABASE'])
        initdb(db)
        name='test'
        email="test@mail.cn"
        passwd="123456"
        create_user(db,name,email,passwd)
        db.close()
    app.run(host=0.0.0.0,port=port)
