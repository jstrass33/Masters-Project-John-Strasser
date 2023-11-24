import sys

sys.path.insert(0, '/var/www/Network_Tool_Napalm')
activate_this = '/home/pi/.local/share/virtualenvs/Network_Tool_Napalm-jrRMAQaO/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))


from Network_Tool_Napalm import app as application
