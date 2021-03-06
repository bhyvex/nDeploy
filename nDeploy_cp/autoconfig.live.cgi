#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import shutil


__author__ = "Anoop P Alias"
__copyright__ = "Copyright 2014, PiServe Technologies Pvt Ltd , India"
__license__ = "GPL"
__email__ = "anoop.alias@piserve.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
backend_config_file = installation_path+"/conf/backends.yaml"
myhome = os.environ["HOME"]

cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>nDeploy</title>')
print('<style>')
print('.boxedyellow {border: 1px solid grey;background-color:LightYellow;font-size: 12px}')
print('.boxedblue {border: 1px solid grey;background-color:LightBlue;font-size: 12px}')
print('</style>')
print('</head>')
print('<body>')
print('<a href="ndeploy.live.cgi"><img border="0" src="nDeploy.png" alt="nDeploy"></a>')
print('<HR>')
if form.getvalue('domain') and form.getvalue('custom'):
    mydomain = form.getvalue('domain')
    customconf = form.getvalue('custom')
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        profileyaml_data_stream = open(profileyaml, 'r')
        yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        profileyaml_data_stream.close()
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        if os.path.isfile(backend_config_file):
            backend_data_yaml = open(backend_config_file, 'r')
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
            backend_data_yaml.close()
            print(('<p style="background-color:LightGrey">CONFIGURE:  '+mydomain+'</p>'))
            print('<HR>')
            if customconf == "0":
                print('<div class="boxedblue">')
                print('<form action="autoconfig2.live.cgi" method="post">')
                print(('You are currently using '+backend_category+' as backend<br>'))
                print('Select a BACKEND from the drop down below to continue<br>')
                print('</div>')
                print('<select name="backend">')
                for backends_defined in list(backend_data_yaml_parsed.keys()):
                    print(('<option value="'+backends_defined+'">'+backends_defined+'</option>'))
                print('</select>')
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print('<input type="submit" value="PROCEED">')
                print('</form>')
            elif customconf == "1":
                try:
                    shutil.copyfile('/etc/nginx/sites-enabled/'+mydomain+'.include', myhome + '/' + mydomain + '_nginx.include.custom.conf')
                except IOError:
                    print("IOError in config file copying")
                print('<form action="update.live.cgi" method="post">')
                print('<textarea name="textcontent" placeholder="Copy contents of '+ myhome + '/' + mydomain + '_nginx.include.custom.conf here and edit" cols="120" rows="50">')
                print('</textarea>')
                print('<HR>')
                print('<input type="submit" value="Submit" />')
                print(('<input style="display:none" name="domain" value="'+mydomain+'">'))
                print('</form>')
                print('<HR>')
                print('<div class="boxedyellow">')
                print('You can use FASTCGICACHE as the cache zone with fastcgi_cache directive<br>')
                print('You can use PROXYCACHE as the cache zone with proxy_cache directive<br>')
                print('</div>')
            else:
                print('ERROR : Invalid POST data')
        else:
            print('ERROR : nDeploy backend defs file i/o error')
    else:
        print('ERROR : domain-data file i/o error')
else:
    print('ERROR : Forbidden')
print('</body>')
print('</html>')
