# roku-tv-control
A python script for controlling any aspect of a Roku TV, and likely other Roku devices

control your Roku TV by passing arguments to this Python script

it does require some minor configuration.  The IP address and mac address of your Roku device should be added to the rokuTV dict  
and your local broadcast IP address needs to be added to the wol dict.  
The mac address is needed to turn on the TV, if it has been off long enough that it is unable to accept API requests.  
That and the broadcast IP allow it to be turned on via a WOL packet.  
Broadcast IP addresses usually look like normal IP addresses on the network only they end with 255  
  
For example:
the rokuTV IP might be *192.168.0.102*  
the broadcast IP would be *192.168.0.255*  


To change the `apps` dictionary you can get a list of installed apps as XML includeing the name and ID number of every app by
`curl http://roku_ip:8060/query/apps'  
 * Calling and parsing the XML file could buid the `app` dict dynamically but I chose to use a static variable*
  
Some example uses.  
`python control.py power` //toggle the TV on or off  
`python control.py 12` // launch the an app by ID  
`python control.py vudu` // launch the an app by name  
`python control.py left` // navigate the menu
