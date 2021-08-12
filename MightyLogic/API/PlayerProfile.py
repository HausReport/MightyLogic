from datetime import datetime
from pprint import pprint
import uuid

import requests

player_id = 'KMGKBP'
payload = {'profile_id': player_id, 'content-type':'text/utf-8'}
URL_BASE = "https://blitzmightyparty.ru/gs_api/"
VERSION = "0.85"
ping = 1
#
# ping starts off as 1, then is apparently rec'd from server
#
# public async Task Ping()
# {
#     var pingInfo = await SendMessageAsync("profile/ping", "{}");
#     var info = Deserialize < PingInfo > (pingInfo);
#     ping = info.result.pingNumber;
#     log.LogInformation($"Ping set to {ping}");
# }

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

current_utc = datetime.utcnow()
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


# C# for obscurenumber
# private static string ObscureNumber(int ping)
# {
# return new string(((long)ping ^ int.MaxValue).ToString().Reverse().ToArray());
# }
#
# private static string SecureString(string data, string deviceId, string version, string ping)
# {
# var b = new
# StringBuilder();
# b.Length = 0;
# b.Append(GetMD5(data));
# b.Append(deviceId);
# b.Append(version);
# b.Append(ping);
# string mD = GetMD5(b.ToString());
# b.Length = 0;
# return mD;
# }
# private static string GetMD5(string data)
# {
# return GetMD5(new UTF8Encoding().GetBytes(data));
# }
# private static string GetMD5(byte[] bytes)
# {
# bytes = new
# MD5CryptoServiceProvider().ComputeHash(bytes);
# StringBuilder stringBuilder = new StringBuilder(32);
# for (int i = 0; i < bytes.Length; i++)
#     {
#         stringBuilder.Append(Convert.ToString(bytes[i], 16).PadLeft(2, '0'));
#     }
# int count = 32 - stringBuilder.Length;
# stringBuilder.Insert(0, "0", count);
# return stringBuilder.ToString();
# }

# MD5 in Python3:
# import hashlib
# msg = "whatever your string is"
# encoded = hashlib.md5(msg.encode('utf-8')).hexdigest()
# print(encoded)