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

### HEADER STUFF
# string secureString = SecureString(data, device_id, VERSION, ping.ToString());
# string numberObscured = ObscureNumber(ping);

#
# The datetime formatter is O like Oscar, not 0 like zero
# ex. 2008-10-31T17:04:32.0000000
#
# string start = DateTime.Now.ToString("O");
# message.Headers.Add("PNK-Device-ID", device_id);
# message.Headers.Add("PNK-Secure-String", secureString);
# message.Headers.Add("PNK-request-client-start-time", start);
# message.Headers.Add("PNK-request-client-system-time", DateTime.Now.ToString("O"));
# message.Headers.Add("PNK-request-client-system-time-utc", DateTime.UtcNow.ToString("O"));
# message.Headers.Add("PNK-number", numberObscured);
### END HEADER STUFF


r = requests.post(URL_BASE+"profile/get_player_info", headers=headers, data=payload)
pprint(r.json())

#print(r.status_code)
pprint(r.headers)
#print(r.encoding)
#print(r.json())