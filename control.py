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

# Wake-on-LAN info, bcip is the local broadcast IP
wol = {'port': 9,
'bcip': '192.168.0.255'}

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
	sock.sendto(packet, (wol['bcip'], wol['port']))


buttons = ['back', 'backspace', 'down', 'enter', 'forward',
 'home', 'info', 'left', 'literal', 'play', 'power', 'InstantReplay',
 'reverse', 'right', 'search', 'select', 'up', 'volumedown',
 'volumemute', 'volumeup']

# list of app names for easy launching, the ID numbers can be
# found from a /query/apps API call
apps = {'netflix': '12', 'vudu': '13842', 'dlna': '2213',
 'fox-sports': '95307', 'espn': '34376', 'abc': '73376'}

# alternative names for common inputs
# the tvinput.* keys are how the apps list labels the physical inputs
aliases = {'ok': 'select', 'mute': 'volumemute', 'tvinput.hdmi1': 'InputHDMI1',
 'tvinput.hdmi2': 'InputHDMI2', 'tvinput.hdmi3': 'InputHDMI3',
 'tvinput.cvbs': 'InputAV1', 'tvinput.dtv': 'InputTuner',
 'hdmi1': 'InputHDMI1', 'hdmi2': 'InputHDMI2', 'hdmi3': 'InputHDMI3',
 'rca': 'InputAV1', 'tuner': 'InputTuner', 'antenna': 'InputTuner',
 'replay': 'InstantReplay'}

"""
the argument is checked
 if it starts with LIT_, type character,
 if it is a number, launch an app using the app ID,
 if it is a string in the buttons list, keypress event is triggered
 if it is a string found as a key in the alias dict, trigger associated keypress
 if it is a string found as a key in the apps dict, launch the app
 if it is not any of the above, return 'fail'
"""
if re.match('^lit_.$', arg, re.IGNORECASE):
	# character input for searches
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/keypress/'+ arg
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed'
elif re.match('^\d+$', arg):
	# launch app by given ID number
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/launch/'+ arg
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed attempting to launch App #'+arg
elif arg in buttons:
	# argument found in button name dict
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/keypress/'+ arg
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed'
		if arg == 'power':
			print 'trying WOL'
			wolRoku()
elif arg in aliases:
	# argueent found in aliases dict
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/keypress/'+ aliases[arg]
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed'
elif arg in apps:
	# app name given, launch app by associated ID
	try:
		url = 'http://'+ rokuTV['ip'] +':'+ rokuTV['port'] +'/launch/'+ apps[arg]
		r = requests.post(url,timeout=2)
	except requests.Timeout:
		print 'API failed attempting to launch '+arg
else:
	print 'fail'
