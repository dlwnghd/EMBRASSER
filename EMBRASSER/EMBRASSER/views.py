import pytesseract

from django.core.files.storage import FileSystemStorage
from PIL import Image
from ocr_module.first_ocr import *
import os
import json
# import numpy as np

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from config.State import State

import requests
import uuid
import time
import json

def index(request):
    return render(request, 'index.html')

def coocr_upload(request):

    context = {}
    context['menutitle'] = 'OCR READ'

    imgname = ''
    resulttext = ''

    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile','')

        if uploadfile != '':
            name_old = uploadfile.name

            fs = FileSystemStorage(location = 'static/source')
            imgname = fs.save(f'src-{name_old}',uploadfile)

            imgfile = Image.open(f'./static/source/{imgname}')
            # resulttext = pytesseract.image_to_string(imgfile, lang='kor')


            # API 키 불러오기
            api_url = 'https://89w7f3qfa7.apigw.ntruss.com/custom/v1/19515/7dc8cb6af87386e43b045c2c4b47139b424763a831b47a497b51c005c2cb894c/general'
            secret_key = 'WEtTcUlIRmZGSENGU1RoSVBSR21vR3piY05IcGNMS1E='

            # 신청서
            image_file = preprocessing(r'C:\DevRoot\dataset\project\app22.jpg')
            json_file = r'C:\DevRoot\dataset\project\app22.json'


            # 등본
            # image_file = r'C:\DevRoot\dataset\project\emdqhs.png'
            # json_file = r'C:\DevRoot\dataset\project\emdqhs.json'

            # 가족관계증명서
            # image_file = r'C:\DevRoot\dataset\project\family.png'
            # json_file = r'C:\DevRoot\dataset\project\family.json'

            request_json = {
                'images': [
                    {
                        'format': 'png',
                        'name': 'demo'
                    }
                ],
                'requestId': str(uuid.uuid4()),
                'version': 'V2',
                'timestamp': int(round(time.time() * 1000))
            }

            payload = {'message': json.dumps(request_json).encode('UTF-8')}
            files = [
            ('file', open(image_file,'rb'))
            ]
            headers = {
            'X-OCR-SECRET': secret_key
            }

            response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

            res = json.loads(response.text.encode('utf8'))
            print(res)

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(res, outfile, indent=4, ensure_ascii=False)
                




















    context['imgname'] = imgname
    context['resulttext'] = resulttext.replace(" ","")

    return render(request, 'coocr_upload.html', context)