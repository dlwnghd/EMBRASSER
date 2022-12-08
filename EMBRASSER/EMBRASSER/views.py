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

def index(request):
    return render(request, 'index.html')

def joinmember(request):
    name = request.GET.get('name')
    # age = request.GET.get('age')
    # id_card = request.GET.get('id_card')
    # number = request.GET.get('number')
    # email = request.GET.get('email')
    # address = request.GET.get('address')
    # religion = request.GET.get('religion')
    # education = request.GET.get('education')
    # # sex = request.GET.get('sex')
    # job = request.GET.get('job')
    # salary = request.GET.get('salary')
    # money = request.GET.get('money')
    # debt = request.GET.get('debt')
    # marriage = request.GET.get('marriage')
    # alchol = request.GET.get('alchol')
    # tabacco = request.GET.get('tabacco')
    # cm = request.GET.get('cm')
    # kg = request.GET.get('kg')
    # sibling = request.GET.get('sibling')

    try :
        print("name : ", name)
        Members.objects.create(
            name = name,
            # age = age,
            # p_code = id_card,
            # phone = number,
            # email = email,
            # addr = address,
            # sex = sex,
            # height = cm,
            # weight = kg,
            # family = sibling
            # company = job,
            # salary = salary,
            # property = money,
            # debt = debt,
            # religion = religion,
            # drink = alchol,
            # smoke = tabacco,
            # scholar = education,
            # re_marry = marriage,
        )
        print("읽을 수 있는 파일!")

    except Exception as e:
        print(e)
        print("읽을 수 없는 파일")
    # return joinmember(request, 'joinmember.html')



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

            # json 파일 저장 경로                         
            fs_json = FileSystemStorage(location = 'static/source/')

            # 이미지 파일을 저장할때 이미지명
            imgname = fs.save(f'image/src-{name_old}',uploadfile)
            img_name, file_type = os.path.splitext(imgname)

            # 파일열기
            # imgfile = Image.open(f'./static/source/{imgname}')
            
            # 결과 텍스트
            # resulttext = pytesseract.image_to_string(imgfile, lang='kor')
            
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
            

            # 등본
            # image_file = r'C:\DevRoot\dataset\project\emdqhs.png'
            # json_file = r'C:\DevRoot\dataset\project\emdqhs.json'

            # 가족관계증명서
            # image_file = r'C:\DevRoot\dataset\project\family.png'
            # json_file = r'C:\DevRoot\dataset\project\family.json'

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
            
            # sentences = [('성명(한글)','나이(만)'), '나이(만)', '주민등록번호','전화번호','E-mail','주소',
            #         ('종교', '학력'), ('학력', '성별'), '성별', ('직업', '연봉'), '연봉', ('재산', '부채'),
            #         '부채', ('결혼여부','음주횟수(월)'), ('음주횟수(월)','흡연여부(O/X)'), '흡연여부(O/X)',
            #         ('신장(cm)','체중(kg)'), ('체중(kg)', '형제관계'), '형제관계']

            # sentences_dic = ['name', 'age', 'id_card','number','Email','address',
            # 'religion', 'Education', 'sex', 'job', 'salary', 'money',
            #  'fan', 'marriage', 'alcohol', 'tobacco',
            # 'cm', 'kg', 'sibling']

            sentences = {('성명(한글)','나이(만)'):'name',
            '나이(만)':'age',
            '주민등록번호':'id_card',
            '전화번호':'number',
            'E-mail':'email',
            '주소':'address',
            ('종교', '학력'):'religion',
            ('학력', '성별'):'education',
            '성별':'sex',
            ('직업', '연봉'):'job',
            '연봉':'salary',
            ('재산', '부채'):'money',
            '부채':'debt',
            ('결혼여부','음주횟수(월)'):'marriage',
            ('음주횟수(월)','흡연여부(O/X)'):'alcohol',
            '흡연여부(O/X)':'tobacco',
            ('신장(cm)','체중(kg)'):'cm',
            ('체중(kg)', '형제관계'):'kg',
            '형제관계':'sibling'}

            ocr = OCR(local)
            context['resulttext'] = ocr.result_application(sentences)
            # ocr.result_application(sentences)

    # context에 데이터 담기
    context['imgname'] = imgname

    return render(request, 'member_ocr.html', context)
