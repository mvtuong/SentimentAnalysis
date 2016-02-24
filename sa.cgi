#!/home2/ciscerco/src/python27/bin/python
from wsgiref.handlers import CGIHandler
from sentiment import app

app.config['SERVER_NAME'] = 'predict.ciscer.com'
CGIHandler().run(app)
