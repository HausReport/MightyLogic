from pprint import pprint

import requests
payload = {'profile_id': 'KMGKBP', 'content-type':'text/utf-8'}
URL_BASE = "https://blitzmightyparty.ru/gs_api/"
headers = {}
headers['PNK-Retry'] ='1'

### HEADER STUFF
# string secureString = SecureString(data, device_id, VERSION, ping.ToString());
# string numberObscured = ObscureNumber(ping);
# string start = DateTime.Now.ToString("O");
#
# message.Headers.Add("PNK-Retry", 1.ToString());
# message.Headers.Add("PNK-Device-ID", device_id);
# message.Headers.Add("PNK-Login-ID", player_id);
# message.Headers.Add("PNK-Player-ID", player_id);
# message.Headers.Add("PNK-Platform", "FB_GAMEROOM");
# message.Headers.Add("PNK-Env", "WindowsPlayer");
# message.Headers.Add("PNK-Version", VERSION);
# message.Headers.Add("PNK-Secure-String", secureString);
# message.Headers.Add("PNK-request-client-start-time", start);
# message.Headers.Add("PNK-request-client-system-time", DateTime.Now.ToString("O"));
# message.Headers.Add("PNK-request-client-system-time-utc", DateTime.UtcNow.ToString("O"));
# message.Headers.Add("PNK-number", numberObscured);
# message.Headers.Add("PNK-Request-Id", Guid.NewGuid().ToString());
### END HEADER STUFF


r = requests.post(URL_BASE+"profile/get_player_info", headers=headers, data=payload)
pprint(r.json())

#print(r.status_code)
pprint(r.headers)
#print(r.encoding)
#print(r.json())