############
# just used to get pac file according to parameters. 
# same as:https://tlanyan.me/trojan-pac.php?p=1080
# ver: 0.1
# date: 2020-06-16
# author: syaoo
############

from flask import Flask, make_response, request
import os
app = Flask(__name__)
port = int(os.getenv('PORT', 8000))
@app.route('/')
def index():
    return "hello!"
    
@app.route('/pac')
def pac():
    cdir = os.path.dirname(__file__)
    print(cdir)
    # pdir = cdir+"/pac/" # source file path is different when debug is off or on.
    pdir = "pac/"
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
    cmd = 'genpac --pac-proxy "SOCKS5 127.0.0.1:%s" --gfwlist-local "%s/gfwlist.txt"' %(port,pdir)
    gfwlist = os.popen(cmd)
    resp = make_response(gfwlist.read())

    resp.headers["Content-type"]="application/json;charset=UTF-8"
    return resp

if __name__ == "__main__":
    # use this url like this: "127.0.0.1:5020/pac?p=1080" to get pac
    # app.run(host='0.0.0.0',debug=True,port=5020)

    # !!!! Remember to turn off debug mode when the web page goes online!!!!
    app.run(host='0.0.0.0',port=port)
