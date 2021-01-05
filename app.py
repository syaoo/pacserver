from flask import Flask, render_template, session, redirect, url_for, \
    g, request,flash, make_response
from functools import wraps
import leancloud, os, json, requests, sys
from assist import LcHandler
from gfw2pac import genpac

####
# 继续完善：
# 1. 编辑规则功能
# 2. 显示服务器信息
# 3. 用装饰器来增加已登录验证
# 4. 增加404页面

app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
app.config.update(dict(
    # get leancloud appid and key from envirometn
    LC_DB = "pac_rules", # {rule:url}
    LC_USER = "pac_user",
    APPID = os.getenv('LC_APPID'),
    APPKEY = os.getenv('LC_APPKEY'),
    DEBUG=True,
    SECRET_KEY='development key',
))

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/export')
@is_logged_in
def exportPAC():
    user = session.get('username')
    pac='./resources/pac/{}-rules.txt'.format(user)
    LC_class=LcHandler(app.config['LC_DB'])
    try:
        res = LC_class.query.matched('rule', '.*', ignore_case=True)
        with open(pac,'w') as f:
            for i in res.find():
                f.write(i.get('rule'))
                f.write('\n')
        flash('Export {} items!'.format(len(res.find())),'success')
        return redirect(url_for('index'))
    except leancloud.LeanCloudError as e:
        flash(e,'error')
        return redirect(url_for('index'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        LC_class=LcHandler(app.config['LC_USER'])
        email=request.form['log']
        passwd = request.form['pwd']
        res = LC_class.item_query('email',email)
        print("+++++++++++++++++++++:{}".format(len(res)))
        if len(res) == 0:
            error = "用户不存在"
            return render_template('login.html',error=error)
        else:
            res = res[0]
            print(passwd)
            print(res.get('passwd'),res.get('name'))
            print(res.get('email'))

            if passwd==res.get('passwd'):
                session['logged_in'] = True
                session['username'] = res.get('name')
                flash('登录成功','success')
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
@is_logged_in
def index():
    LC_class=LcHandler(app.config['LC_DB'])
    try:
        res = LC_class.query.matched('rule', '.*', ignore_case=True)
        print('1+++++++++++++++++++++')
        print(res.find())
        for i in res.find():
            print(i.get('rule'))
        items = [i.get('rule') for i in res.find()]
        with open('./resources/pac_source.json','r') as f:
            pac_source=json.loads(f.read())
        return render_template('index.html',rules=items,pac_source=pac_source['source'])

    except leancloud.LeanCloudError as e:
        flash(e,'error')
        return redirect(url_for('index'))

@app.route('/add',methods=['POST'])
@is_logged_in
def add_item():
    rule=request.form['rule']
    LC_class=LcHandler(app.config['LC_DB'])
    try:
        print("++++++ add item ++++{}".format(rule))
        c=LC_class.items_add({'rule':rule},'rule')
        flash("Add {} items".format(c),"success")
        return redirect(url_for('index'))
    except leancloud.LeanCloudError as e:
        flash(e,'error')
        return redirect(url_for('index'))

# 路径传参数
# @app.route('/del/<string:id>, <string:rule>',methods=['POST'])
# def del_item(id,rule):
# get传参数
@app.route('/del',methods=['POST'])
@is_logged_in
def del_item():
    id = request.args.get('id')
    rule = request.args.get('rule')
    print("get rule",rule)
    LC_class=LcHandler(app.config['LC_DB'])
    LC_class.item_del('rule',rule)
    flash("delete {}".format(rule),"success")
    return redirect(url_for('index'))

@app.route('/edit/<string:id>',methods=['GET','POST'])
@is_logged_in
def edit_item(id):
    # 未完成 编辑规则
    db=sqlHandler(app.config['DATABASE'])
    cur = db.exeOne('SELECT * FROM rules WHERE id="{}"'.format(id))
    item = cur.fetchone()
    db.close()
    return redirect(url_for('index'))

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/updatepac',methods=['GET','POST'])
@is_logged_in
def updatepac():
    source = request.form.get('select')
    print('123')
    try:
        req = requests.get(source)
        with open('./resources/pac/gfwlist.txt','w') as f:
            f.write(req.text)
        print('ada')
        flash('已从 "{}" 更新PAC'.format(source),'success')
        print('af')
        return redirect(url_for('index'))
    except Exception as e:
        print('afsss')
        flash("更新失败: {}".format(e),'danger')
        return redirect(url_for('index'))

@app.route('/pac')
def pac():
    ############
    # just used to get pac file according to parameters. 
    # same as:https://tlanyan.me/trojan-pac.php?p=1080
    # ver: 0.1
    # date: 2020-06-16
    # author: syaoo
    ############
    cdir = os.path.dirname(__file__)
    print(cdir)
    # pdir = cdir+"/pac/" # source file path is different when debug is off or on.
    pdir = "resources/"
    port = request.args.get('p')
    user = request.args.get('u')
    print("get user",user)
    if port == None:
        return render_template('pac.html')
    if port == '':
        port = '1080'
    if (user == None or user == ''):
        user='user' 
    # Recommend this method
    # cmd = 'genpac --pac-proxy "SOCKS5 127.0.0.1:%s" --gfwlist-local "%s/gfwlist.txt" --user-rule-from "%s/user-rules.txt"' %(port,pdir,pdir)
    # gfwlist = os.popen(cmd)
    # resp = make_response(gfwlist.read())
    # use gfw2pac package
    pac_str = genpac(fin = './resources/pac/gfwlist.txt', 
            proxy = 'SOCKS5 127.0.0.1:{}'.format(port),
            other = 'resources/pac/{}-rules.txt'.format(user), 
            precise = True)
    resp = make_response(pac_str)
    resp.headers["Content-type"]="application/json;charset=UTF-8"
    return resp

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def create_user(db,name,email,passwd):
    LC_class=LcHandler(db)
    try:
        LC_class.items_add({
            'name':name,
            'email':email,
            'passwd':passwd
        },'email')
        print({
            'name':name,
            'email':email,
            'passwd':passwd
        })
        flash("Add {}".format(name),"success")
        return redirect(url_for('index'))
    except leancloud.LeanCloudError as e:
        print(e)
        flash(e,'error')
        return redirect(url_for('index'))

def init_rules(db):
    LC_class=LcHandler(db)
    try:
        LC_class.entry.save()
       
    except leancloud.LeanCloudError as e:
        print(e)
        
if __name__ == "__main__":
    # init database
    APPID = os.getenv('LC_APPID')
    APPKEY = os.getenv('LC_APPKEY')
    if (APPID == None or APPKEY == None):
        print("no 'LC_APPID' and 'LC_APPKEY' set.")
        sys.exit(0)
    leancloud.init(APPID, APPKEY)
    args=sys.argv
    init = args[1]
    if init=='True':
        print(":++++++++++++++++++++:")
        db = app.config['LC_USER']
        name='test'
        email="test@mail.cn"
        passwd="123456"
        print('email is {}'.format(email))
        create_user(db,name,email,passwd)
        init_rules(app.config['LC_DB'])
    app.run(host="0.0.0.0",port=port)
