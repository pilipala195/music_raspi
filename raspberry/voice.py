import json
import urllib, urllib2
import base64


def getToken():
    apiKey  = "qiZhLzhuVoEvP9iILTRp7tUs"
    secretKey = "lIdIMvGs0Vyw9atv0wXv4n313GQRtSjP"
    getTokenURL = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials" + "&client_id=" + apiKey + "&client_secret=" + secretKey
    
    response = json.loads(urllib.urlopen(getTokenURL).read())
    return response['access_token']


def getResult():
    token = getToken()
    serverURL = "http://vop.baidu.com/server_api"
    cuid = "A85B78636F6E"

    speech_file = 'voice.wav'
    with open(speech_file, 'rb') as f:
        speech_data = f.read()
        speech_base64=base64.b64encode(speech_data).decode('utf-8')
    speech_length=len(speech_data)
    params = {
        'format':'pcm',
        'rate':8000,
        'channel':'1',
        'token':token,
        'cuid':cuid,
        'lan':'zh',
        'len':speech_length,
        'speech':speech_base64
    } 
    json_data = json.dumps(params).encode('utf-8')
    json_length = len(json_data)
    request = urllib2.Request(url=serverURL)
    request.add_header("Content-Type", "application/json")
    request.add_header("Content-Length", json_length)
    fs = urllib2.urlopen(url=request, data=json_data)

    result_str = fs.read().decode('utf-8')
    json_resp = json.loads(result_str)
    print json_resp
    if json_resp['err_no']:
        res = [0]
    else:
        res = json_resp['result']
    print unicode(res[0])
    return  res[0]


if __name__ == '__main__':
    res = getResult()
    print res