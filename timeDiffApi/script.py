from subprocess import call

call("pip install virtualenv", shell=True)
call("virtualenv apienv", shell=True)
call("source apienv/bin/activate", shell=True)
call("pip install flask", shell=True)
call("pip install flask_restful --user", shell=True)
call("pip install python-dateutil", shell=True)
call("pip install requests", shell=True)
call("pip install json", shell=True)
call("python3 app.py", shell=True)
