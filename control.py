import socket, struct
import requests, sys, re

# take an argument as input
try:
	arg = sys.argv[1]
except:
	arg = ""

# device info
rokuTV = {'mac': '00:11:22:33:aa:bb',
'ip': '192.168.0.10',
'port': '8060'}

# Wake-on-LAN info, ip is the local broadcast IP
wol = {'port': 9,
'ip': '192.168.0.255'}

# after being off for a while http is unavailable so use WOL
def wolRoku():
	packet = chr(255) * 6

	macStr = rokuTV['mac'].replace(':', '').replace('-', '')
	encAddr = ''

	for i in range(6):
		j = 2 * i
		encAddr += struct.pack('B', int(macStr[j:j+2],16))
	packet += encAddr * 16

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(packet, (wol['ip'], wol['port']))


buttons = ['back', 'backspace', 'down', 'enter', 'forward',
 'home', 'info', 'left', 'literal', 'play', 'power', 'replay',
 'reverse', 'right', 'search', 'select', 'up', 'volumedown',
 'volumemute', 'volumeup']

apps = {'netflix': '12', 'vudu': '13842', 'dlna': '2213',
 'fox-sports': '95307', 'espn': '34376', 'abc': '73376',
 'hdmi1': 'tvinput.hdmi1', 'hdmi2': 'tvinput.hdmi2',
 'hdmi3': 'tvinput.hdmi3', 'rca': 'tvinput.cvbs'}

aliases = {'ok': 'select', 'mute': 'volumemute'}

"""
the argument is checked
 if it is a number, launch an app using the app ID,
 if it is a string in the buttons list, keypress event is triggered
 if it is a string found as a key in the alias dict, trigger associated keypress
 if it is a string found as a key in the apps dict, launch the app
 if it is not any of the above, return 'fail'
"""
if re.match('^\d+$', arg):
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/launch/'+ arg
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed attempting to launch App #'+arg
elif arg in buttons:
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/keypress/'+ arg
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed'
		if arg == 'power':
			print 'trying WOL'
			wolRoku()
elif arg in aliases:
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/keypress/'+ aliases[arg]
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed'
elif arg in apps:
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/launch/'+ apps[arg]
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed attempting to launch '+arg
else:
	print 'fail'
