"""
    the request py
"""
# coding=utf-8

import sys
import json
import base64
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

timer = time.perf_counter
IS_PY3 = sys.version_info.major == 3

API_KEY = '8VNGwHwwUhaBh3LHsgGmDNWq'
SECRET_KEY = 'Z5qXjVYfenrEf0BibpNhEBpr22FdhWud'

FORMAT = 'wav'
CUID = '123456PYTHON'
RATE = 16000
DEV_PID = 1536
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'

class DemoError(Exception):
    """
        class for error
    """
    pass


def fetch_token():
    """

    :return:
    """
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if IS_PY3:
        post_data = post_data.encode( 'utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError:
        print('token http response http code : ' + str(URLError))
        result_str = str(URLError)
    if IS_PY3:
        result_str =  result_str.decode()

    result = json.loads(result_str)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def recognize(audio_file):
    """

    :param audio_file:
    :return:
    """
    token = fetch_token()

    with open(audio_file, 'rb') as speech_file:
        speech_data = speech_file.read()

    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % audio_file)
    speech = base64.b64encode(speech_data)
    if IS_PY3:
        speech = str(speech, 'utf-8')
    params = {'dev_pid': DEV_PID,
             #"lm_id" : LM_ID,    #测试自训练平台开启此项
              'format': FORMAT,
              'rate': RATE,
              'token': token,
              'cuid': CUID,
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params)
    # print post_data
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print ("Request time cost %f" % (timer() - begin))
    except URLError as err:
        # print('asr http response http code : ' + str(URLError))
        result_str = str(URLError)

    if IS_PY3:
        result_str = str(result_str, 'utf-8')
    try:
        result_str = eval(result_str)['result'][0]
    except KeyError:
        result_str = ''

    return result_str




