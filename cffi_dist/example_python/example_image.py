import ctypes
import json
import base64
import re

# load the tls-client shared package for your OS you are currently running your python script (i'm running on mac)
library = ctypes.cdll.LoadLibrary('./../dist/tls-client-darwin-amd64-0.9.0.dylib')

# extract the exposed request function from the shared package
request = library.request
request.argtypes = [ctypes.c_char_p]
request.restype = ctypes.c_char_p

freeSession = library.freeSession
freeSession.argtypes = [ctypes.c_char_p]
freeSession.restype = ctypes.c_char_p

freeAll = library.freeAll
freeAll.restype = ctypes.c_char_p

requestPayload = {
    "tlsClientIdentifier": "chrome_105",
    "followRedirects": False,
    "insecureSkipVerify": False,
    "withoutCookieJar": False,
    "withRandomTLSExtensionOrder": False,
    "isByteResponse": True,
    "timeoutSeconds": 30,
    "proxyUrl": "",
    "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7"
    },
    "headerOrder": [
        "accept",
        "user-agent",
        "accept-encoding",
        "accept-language"
    ],
    "requestUrl": "https://avatars.githubusercontent.com/u/17678241?v=4",
    "requestMethod": "GET",
    "requestBody": "",
    "requestCookies": []
}

# this is a pointer to the response
response = request(json.dumps(requestPayload).encode('utf-8'))

# we dereference the pointer to a byte array
response_bytes = ctypes.string_at(response)

# convert our byte array to a string (tls client returns json)
response_string = response_bytes.decode('utf-8')

# convert response string to json
response_object = json.loads(response_string)

data = response_object['body']

dataWithoutMimeType = data.split(",")[1]

with open("./example.png", "wb") as fh:
    fh.write(base64.urlsafe_b64decode(dataWithoutMimeType))