import shutil, subprocess, json, sys, os, time, urllib, csv, tempfile, itertools
import datetime
from datetime import date

import bottle 
from bottle import get, post, response, request, run, route, template, static_file, redirect, SimpleTemplate
from cork import Cork
from beaker.middleware import SessionMiddleware
from cork.backends import MongoDBBackend
import logging

import tps

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.cookie_expires': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.encrypt_key': 'secret',
    'session.auto': True
}

backend = MongoDBBackend(db_name='friendly', initialize=False)

#application = bottle.default_app()
#application = SessionMiddleware(application, session_opts)

app = bottle.app()
app = SessionMiddleware(app, session_opts)
aaa = Cork(backend=backend)

def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@post('/get_interactions')
def get_interaction():
    access_token = post_get('access_token')
    tps.stored_access_token = access_token
    
    week = datetime.timedelta(weeks=10)
    start_date = datetime.datetime.today() - week
    response = {}
    
    try:
        friends = tps.get_interactions_from_last(access_token, start_date)
        response['response'] = 'true'
        response['fbFriends'] = friends

    except:
        response['response'] = 'false'

    return json.dumps(response)
    
@route('/channel')
def channel():
    return render('<script src="//connect.facebook.net/en_US/all.js"></script>')

@route('/')
def index():
    return template('index')
    
@route('/assets/<file_path:path>')
def static(file_path):
	return static_file(file_path, root="assets/")
	
@route('/log', method="POST")
def write_log():

	try:
		data=json.loads(request.body.read())
		log_file = check_unique("%s_%s" % (data['taskID'],data['pID']))
		log = open('logs/%s.txt' % log_file, 'w')
		log.write(json.dumps(data))
		log.close()
		update_stage()
	except:
		response.status = 500;
		return "<div>ERROR WRITING RESPONSES</div>"

def check_unique(fname,suffix=1):
	fname_new=fname
	while (os.path.exists('logs/%s.txt' % fname_new)):
		fname_new = '%s_%i' % (fname,suffix)
		suffix+=1
	return fname_new
	
# #  Web application main  # #

def main():

    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(app=app, quiet=False, reloader=True)

if __name__ == "__main__":
    main()
