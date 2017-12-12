# roku-tv-control
A python script for controlling any aspect of a Roku TV, and likely other Roku devices

control your Roku TV by passing arguments to this Python script

it does require some minor configuration.  The IP address and mac address of your Roku device should be added to the rokuTV dict  
and your local broadcast IP address needs to be added to the wol dict.  
Broadcast IP addresses usually look like normal IP addresses on the network only they end with 255  
  
For example:
the rokuTV IP might be 192.168.0.102  
the broadcast IP would be 192.168.0.255  
  
ie.  
python control.py power //turn the TV on or off  
python control.py 12 // launch the an app by ID  
python control.py vudu // launch the an app by name  

