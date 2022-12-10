from django.core.files.storage import FileSystemStorage
from PIL import Image
from ocr_module.first_ocr import *
import os
import json

from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from config.State import State

from EMBRASSER.models import Members
import requests
import uuid
import time
import json

def coocr_upload(request):

    context = {}
    context['menutitle'] = 'OCR READ'

    imgname = ''

    # Upload할 파일을 Web에서 받아온다면
    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile','') # upload가 있으면 uploadfile 없으면 " " request

        if uploadfile != '':
            name_old = uploadfile.name

            # 이미지 파일 저장 경로                         
            fs = FileSystemStorage(location = 'static/source')

            # 이미지 파일을 저장할때 이미지명
            imgname = fs.save(f'image/src-{name_old}',uploadfile)
            img_name, file_type = os.path.splitext(imgname)
            
            # API 키 불러오기
            api_url = 'https://89w7f3qfa7.apigw.ntruss.com/custom/v1/19515/7dc8cb6af87386e43b045c2c4b47139b424763a831b47a497b51c005c2cb894c/general'
            secret_key = 'WEtTcUlIRmZGSENGU1RoSVBSR21vR3piY05IcGNMS1E='

            print("")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("fs.base_location : ",fs.base_location + fs.url(imgname))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("")
            # 신청서
            image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

            print("777777777777777777777777777777")
            print("json_file : ", json_file)
            print("777777777777777777777777777777")

            # 결과 json
            request_json = {
                'images': [
                    {
                        'format': file_type.replace(".",""),    # 포맷 타입
                        'name': 'demo'                                             # 이름
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

            # 응답
            response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

            local = json.loads(response.text.encode('utf8'))
            
            print("11111111111111" , local)
            with open(json_file, 'w', encoding='utf-8') as outfile:
                print("2222222222222222")
                json.dump(local, outfile, indent=4, ensure_ascii=False)
            print("3333333333333333333")

            sentences = {('성명(한글)','나이(만)'):'name',
            '나이(만)':'age',
            '주민등록번호':'p_code',
            '전화번호':'phone',
            'E-mail':'email',
            '주소':'addr',
            ('종교', '학력'):'religion',
            ('학력', '성별'):'scholar',
            '성별':'sex',
            ('직업', '연봉'):'job',
            '연봉':'salary',
            ('재산', '부채'):'property',
            '부채':'debt',
            ('결혼여부','음주횟수(월)'):'re_marry',
            ('음주횟수(월)','흡연여부(O/X)'):'drink',
            '흡연여부(O/X)':'smoke',
            ('신장(cm)','체중(kg)'):'height',
            ('체중(kg)', '형제관계'):'weight',
            '형제관계':'family'}

            ocr = OCR(local)
            context['resulttext'] = ocr.result_application(sentences)

    # context에 데이터 담기
    context['imgname'] = imgname

    return render(request, 'member_ocr.html', context)

def joinmember(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    p_code = request.GET.get('p_code')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    address = request.GET.get('address')
    religion = request.GET.get('religion')
    scholar = request.GET.get('scholar')
    sex = request.GET.get('sex')
    job = request.GET.get('job')
    salary = request.GET.get('salary')
    property = request.GET.get('property')
    debt = request.GET.get('debt')
    re_marry = request.GET.get('re_marry')
    drink = int(request.GET.get('drink'))
    smoke = request.GET.get('smoke')
    height = request.GET.get('height')
    weight = request.GET.get('weight')
    family = request.GET.get('family')

    salary = int(salary.replace(",",""))
    property = int(property.replace(",",""))
    debt = int(debt.replace(",",""))
    
    if smoke == "x" or smoke == "X":
        smoke = 0
    else:
        smoke = 1
    
    if re_marry == "미혼":
        re_marry = 0
    else:
        re_marry = 1
    
    ddrink = ''
    for d in drink:
        if d.isdigit():
            ddrink += d
    drink = int(ddrink)

    hheight = ''
    for h in height:
        if h.isdigit():
            hheight += h
    height = int(hheight)

    wweight = ''
    for w in weight:
        if w.isdigit():
            wweight += w
    weight = int(wweight)

    try :
        print("name : ", name)
        Members.objects.create(
            name = name,
            # age = age,
            # p_code = p_code,
            # phone = phone,
            # email = email,
            # addr = addr,
            # sex = sex,
            # height = height,
            # weight = weight,
            # family = family
            # job = job,
            # salary = salary,
            # property = property,
            # debt = debt,
            # religion = religion,
            # drink = drink,
            # smoke = smoke,
            # scholar = scholar,
            # re_marry = re_marry,

            # grade 계산에서 넣어주기
        )
        print("읽을 수 있는 파일!")

    except Exception as e:
        print(e)
        print("읽을 수 없는 파일")
    # return joinmember(request, 'joinmember.html')
