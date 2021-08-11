from datetime import datetime
from pprint import pprint
import uuid

import requests

player_id = 'KMGKBP'
payload = {'profile_id': player_id, 'content-type':'text/utf-8'}
URL_BASE = "https://blitzmightyparty.ru/gs_api/"
VERSION = "0.85"

headers = {}
headers['PNK-Retry'] ='1'
headers['PNK-Login-ID'] = player_id
headers['PNK-Player-ID'] = player_id
headers['PNK-Platform'] = 'FB_GAMEROOM'
headers['PNK-Env'] = 'WindowsPlayer'
headers['PNK-Version'] = VERSION

# correct format?
guid = str(uuid.uuid4()) # like 'f50ec0b7-f960-400d-91f0-c42a6d44e3d0'
headers['PNK-Request-Id'] = guid

# message.Headers.Add("PNK-Retry", 1.ToString());


#
# The datetime formatter is O like Oscar, not 0 like zero
# think this is .isoformat() in python
# ex. 2008-10-31T17:04:32.0000000
#
now = datetime.now() # current date and time
start = now.isoformat()

current_utc = datetime.datetime.utcnow()
start_utc = current_utc.isoformat()

headers['PNK-request-client-start-time'] = start
headers['PNK-request-client-system-time'] = start
headers['PNK-request-client-system-time-utc'] = start_utc

### HEADER STUFF I HAVEN'T WORKED OUT YET
# string secureString = SecureString(data, device_id, VERSION, ping.ToString());
# string numberObscured = ObscureNumber(ping);
# message.Headers.Add("PNK-Device-ID", device_id);

# message.Headers.Add("PNK-Secure-String", secureString);
# message.Headers.Add("PNK-number", numberObscured);
### END HEADER STUFF


r = requests.post(URL_BASE+"profile/get_player_info", headers=headers, data=payload)
pprint(r.json())

#print(r.status_code)
pprint(r.headers)
#print(r.encoding)
#print(r.json())