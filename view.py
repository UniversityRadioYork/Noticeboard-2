from flask import Flask, render_template, redirect, session, request
from gevent.pywsgi import WSGIServer
import os
import requests
import json
import random
from datetime import datetime
import pytz
import sys
import secrets
import re
import jwt
from forms import Forms
from jsondb import Jsondb
from myradioupdater import MyRadioUpdater
from flask_apscheduler import APScheduler

#Imports ENV variables

#url to redirect to when using jwt auth
notice_url = os.environ.get('NOTICE_URL', "http://127.0.0.1:5042/")

#key used for myradio jwt auth
myradio_key = os.environ.get('MYRADIO_SIGNING_KEY', "dev")

#key used to validate myradio api requests. This is the only thing you will need to edit for development.
myradio_api = os.environ.get('MYRADIO_API_KEY', "CHANGE_ME")

#I'm not sure if this does anything but i'm scared to delete it
log_location = os.environ.get('LOG_LOCATION', "/logs/")

#url of the myradio api, change this if you want to test with the myradio dev instance (you don't)
myradio_url = os.environ.get('MYRADIO_URL', "https://www.ury.org.uk/api/v2/")

#creates an app and scheduler thread
class Config:
    SCHEDULER_API_ENABLED = True
    PREFERRED_URL_SCHEME = 'https'

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

#just logs some stuff
unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
print("Starting at " + str(unix_timestamp) , file=sys.stderr)

#important for session stuff
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  

#formats api key a little
myradio_apikey = "api_key="+myradio_api

#creates the database object. And by database I mean json file. it works.
json_db = Jsondb()

#the scheduler thread runs myradio api calls every 15 minutes and stores the result
#this stops this app from spamming myradio with requests and also makes its own api way faster
@scheduler.task('interval', id='do_job_1', minutes=15, misfire_grace_time=900)
def job1():
    myradioupdater = MyRadioUpdater(myradio_url, myradio_apikey)
    myradioupdater.updateNextEvent()
    myradioupdater.updateRecentShows()
    myradioupdater.updateRoles()

def verifyKey(key):
    pattern = re.compile('^[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789]+$')
    return re.search(pattern, key)

#lets you in if you are comp officer or have "edit banner" permission or if the app is in dev mode
def verifySession(session):
    if myradio_key == "dev":
        return True
    if ('name' in session and 'uid' in session):
        api_url = myradio_url + "/user/"+str(session["uid"])+"/permissions?" + myradio_apikey
        response = requests.get(api_url)
        officer = json.loads(response.text)
        if 221 in officer["payload"] or 234 in officer["payload"]:
            return True
    return False

@app.route("/")
def index():
    return render_template('index.html')

#just background
@app.route("/noboard/<start>")
def noboardstart(start):
    return render_template('noboard.html', start=start)

@app.route("/noboard")
def noboard():
    return render_template('noboard.html', start=1)

#either redirects the user to myradio to signing (see auth) or renders a flask-wtf form or stores the values from a submitted form
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if verifySession(session):
        form = Forms.buildEditForm()
        if form.is_submitted():
            json_db.set_userdata(form.brokenlabel.data, form.brokenhtml.data, form.joinlabel.data, form.joinhtml.data, form.listenlabel.data, form.listenhtml.data, form.extralabel.data, form.extrahtml.data, form.welfarelabel.data, form.welfarehtml.data, form.bannerlabel.data, form.meetinglabel.data, form.meetinghtml.data, form.committeehtml.data, form.showlabel.data, form.refresh.data)
            return "Content Updated!"
        return render_template('edit.html', title='EditNoticeboard', form=form)
    else:
        return redirect("https://ury.org.uk/myradio/MyRadio/jwt?redirectto="+notice_url+"auth/", code=302)

#uses a jwt to authenticate the user then redirects them back to edit
@app.route('/auth/', methods=['GET'])
def auth( ):
    args = request.args
    userinfo = jwt.decode(args['jwt'], myradio_key, algorithms=["HS256"])
    session['name'] = userinfo['name']
    session['uid'] = userinfo['uid']
    return redirect(notice_url+"edit", code=302)

@app.route("/openroles")
def openroles():
    try:
        openroles = json_db.get_openroles()
        return openroles
    except:
        print("Error occured serving open roles" , file=sys.stderr)
        return {}

@app.route("/nextevent")
def nextevent():
    try:
        nextevent = json_db.get_nextevent()
        return nextevent
    except:
        print("Error occured serving next event" , file=sys.stderr)
        return {}

#creates a pool from the current week's shows, next week's shows and the last 20 podcasts and then picks a random one
@app.route("/nextlisten")
def nextlisten():
    try:
        pool =  json.loads(json_db.get_recentshows())
        if len(pool) < 1:
            return {"id": 0}
        else:
            random.shuffle(pool)
            return json.dumps(pool[0])
    except:
        print("Error occured serving next event" , file=sys.stderr)
        return {} 

#reads all the values for the "static" text boxes and spits them out
@app.route("/userdata")
def userdata():
    broken_label = json_db.get_brokenlabel()
    broken_html = json_db.get_brokenhtml()
    join_label = json_db.get_joinlabel()
    join_html = json_db.get_joinhtml()
    listen_label = json_db.get_listenlabel()
    listen_html = json_db.get_listenhtml()
    extra_label = json_db.get_extralabel()
    extra_html = json_db.get_extrahtml()
    welfare_label = json_db.get_welfarelabel()
    welfare_html = json_db.get_welfarehtml()
    banner_label = json_db.get_bannerlabel()
    meeting_label = json_db.get_meetinglabel()
    meeting_html = json_db.get_meetinghtml()
    committee_html = json_db.get_committeehtml()
    show_label = json_db.get_showlabel()
    return {
        "brokenlabel": broken_label,
        "brokenhtml": broken_html,
        "joinlabel": join_label,
        "joinhtml": join_html,
        "listenlabel": listen_label,
        "listenhtml": listen_html,
        "extralabel": extra_label,
        "extrahtml": extra_html,
        "welfarelabel": welfare_label,
        "welfarehtml": welfare_html,
        "bannerlabel": banner_label,
        "meetinglabel": meeting_label,
        "meetinghtml": meeting_html,
        "committeehtml": committee_html,
        "showlabel1": show_label,
        "showlabel2": show_label
    }

#returns the frequency the page should refresh
@app.route("/refreshtime")
def getrefresh():
    refresh = json_db.get_refresh()
    return {"refresh": refresh}

#runs all the myradio requests before serving the webpage
#comment this out if you want the app to start faster
job1()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5042))
    print("Starting server on port " + str(port) , file=sys.stderr)
    #app.run(debug=False, host='0.0.0.0', port=port)
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
