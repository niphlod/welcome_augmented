#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import signal
import subprocess
import time
import logging
from splinter.browser import Browser

logging.basicConfig()

if 'WEB2PY_PATH' in os.environ:
    sys.path.append(os.environ['WEB2PY_PATH'])
else:
    path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(path,'web2py.py')):
        i = 0
        while i<10:
            i += 1
            if os.path.exists(os.path.join(path,'web2py.py')):
                break
            path = os.path.abspath(os.path.join(path, '..'))
    os.environ['WEB2PY_PATH'] = path

if not os.environ['WEB2PY_PATH'] in sys.path:
    sys.path.insert(0, os.environ['WEB2PY_PATH'])

def startwebserver(context):
    """
    starts the default webserver on port 8000
    """
    webserverprocess = subprocess.Popen([sys.executable, os.path.join(context.web2py_path, 'web2py.py'), '-a',  'testpass'])
    print 'Sleeping before web2py starts...'
    for a in range(1,5):
        time.sleep(1)
        print a, '...'
    print ''
    return webserverprocess

def terminate_process(pid):
    """
    Taken from http://stackoverflow.com/questions/1064335/in-python-2-5-how-do-i-kill-a-subprocess
    all this shit is because we are stuck with Python 2.5 and \
    we cannot use Popen.terminate()
    """
    if sys.platform.startswith('win'):
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        os.kill(pid, signal.SIGKILL)

def stopwebserver(webserverprocess):
    """
    stops the attached webserver
    """
    print 'Killing webserver'
    if sys.version_info < (2,6):
        terminate_process(webserverprocess.pid)
    else:
        webserverprocess.terminate()

def reset_database(context):
    """
    wipes out the databases folder !!!
    """
    databases = os.path.join(context.web2py_path, 'applications', context.appname, 'databases')
    for a in os.listdir(databases):
        complete_path = os.path.join(databases, a)
        if os.path.isfile(complete_path):
            os.unlink(complete_path)

def load_fixtures(context):
    """
    ATM it looks for a fixtures.csv file and loads it into the database
    and install a URL helper
    """
    from gluon.shell import env
    app_path = os.path.join(context.web2py_path, 'applications', context.appname)
    fixture_file = os.path.join(app_path, 'tests', 'features', 'fixtures.csv')
    env_ = env(a=context.appname, import_models=True, dir=app_path)
    def bogus_url(
        a=None,
        c=None,
        f=None,
        r=None,
        args=None,
        vars=None,
        anchor='',
        extension=None,
        env=None,
        hmac_key=None,
        hash_vars=True,
        salt=None,
        user_signature=None,
        scheme=None,
        host=None,
        port=None,
        encode_embedded_slash=False,
        url_encode=True):
        return env_['URL'](a=a,c=c,f=f,r=r,
            args=args,
            vars=vars,
            anchor=anchor,
            extension=extension,
            env=env,
            hmac_key=hmac_key,
            hash_vars=hash_vars,
            salt=salt,
            user_signature=user_signature,
            scheme=scheme,
            host=host if host is not None else context.host,
            port=port,
            encode_embedded_slash=encode_embedded_slash,
            url_encode=url_encode)
    context.URL = bogus_url
    if os.path.isfile(fixture_file):
        print 'loading fixtures...'
        with open(fixture_file, 'rb') as g:
            env_['db'].import_from_csv_file(g)
        env_['db'].commit()

def before_all(context):
    context.host = '127.0.0.1:8000'
    context.appname = 'welcome_augmented'
    context.web2py_path = os.environ['WEB2PY_PATH']
    logger = logging.getLogger(context.appname)
    context.l = logger
    reset_database(context)
    load_fixtures(context)
    context.webserverprocess = startwebserver(context)
    context.b = Browser('firefox')
    time.sleep(1)
    #visit home page
    home_page = context.URL('default', 'index')
    context.b.visit(home_page)

def after_all(context):
    stopwebserver(context.webserverprocess)
