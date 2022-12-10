from django.core.files.storage import FileSystemStorage
from PIL import Image
from ocr_module.first_ocr import *
import os
import json

from django.shortcuts import render, redirect
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
    age = int(request.GET.get('age'))
    p_code = request.GET.get('p_code')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    addr = request.GET.get('addr')
    religion = request.GET.get('religion')
    scholar = request.GET.get('scholar')
    sex = request.GET.get('sex')
    job = request.GET.get('job')
    salary = request.GET.get('salary')
    property = request.GET.get('property')
    debt = request.GET.get('debt')
    re_marry = request.GET.get('re_marry')
    drink = request.GET.get('drink')
    smoke = request.GET.get('smoke')
    height = request.GET.get('height')
    weight = request.GET.get('weight')
    family = request.GET.get('family')

    salary = int(salary.replace(",", "").replace(".", ''))
    property = int(property.replace(",", "").replace(".", ''))
    debt = int(debt.replace(",", "").replace(".", ''))

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

# 등급 매기기

    # 직업 
    job_grade = {("판사", "의사", "교수", "검사", "박민준", "파일럿", "약사", "프로그래머"): 20,
    ("교사", "은행원", "고위공무원", "대기업", "스타강사", "변호사") : 15,
    ("경찰", "소방관", "디자이너", "행정공무원", "세무사") : 10,
    ("일용직", "무직", "파트타이머", "학생", "계약직") : 5
    }

    for jobs, j_grade in job_grade.items():
        if job in jobs:
            grade_job = j_grade
            break
        else:
            grade_job = 0
    
    # 나이
    if 20 <= age <= 26:
        grade_age = 8
    elif 27 <= age <= 35:
        grade_age = 10
    elif 36 <= age <= 40:
        grade_age = 7
    elif 41 <= age <= 45:
        grade_age = 5
    elif 46 <= age:
        grade_age = 3
    else:
        grade_age = 0

    # 연봉
    if salary <= 30000000:
        grade_salary = 5
    elif 30000000 < salary <= 45000000:
        grade_salary = 10
    elif 45000000 < salary <= 100000000:
        grade_salary = 15
    else:
        grade_salary = 20
    
    # 부채
    propotion = debt / property * 100
    if propotion < 5:
        grade_debt = 20
    elif propotion < 20:
        grade_debt = 15
    elif propotion < 50:
        grade_debt = 10
    else :
        grade_debt = 5

    # 재산
    if property < 100000000:
        grade_property = 5
    elif property < 500000000:
        grade_property = 10
    elif property < 3000000000:
        grade_property = 15
    elif property < 10000000000:
        grade_property = 20
    else:
        grade_property = 30
    


    grade = grade_age + grade_salary + grade_debt + grade_property + grade_job
    if grade >= 90:
        grade = "S"
    elif grade >= 80:
        grade = "A"
    elif grade >= 70:
        grade = "B"
    elif grade >= 60:
        grade = "C"
    else:
        grade = "F"


    flag = False
    try :
        
        Members.objects.get(p_code=p_code)
        msg = "이미 등록된 회원입니다"
    except Exception as e:
        try:
            Members.objects.create(
                name = name,
                age = age,
                p_code = p_code,
                phone = phone,
                email = email,
                addr = addr,
                sex = sex,
                height = height,
                weight = weight,
                family = family,
                job = job,
                salary = salary,
                property = property,
                debt = debt,
                religion = religion,
                drink = drink,
                smoke = smoke,
                scholar = scholar,
                re_marry = re_marry,
                grade = grade
            )
            print("읽을 수 있는 파일!")
            flag = True
            msg = "등록이 완료 되었습니다."
        except Exception as ex:
            print(ex)
            print("읽을 수 없는 파일")
            
        print(e)
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
            try:

                image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            except Exception as e:
                print(e)
                image_file = fs.base_location + fs.url(imgname)
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
            
            #==============================
            # ocr2 = OCR(local)
            
            # list = ocr2.main_sentences
            
            # confirm_form = ""
            # for li in list:
            #     confirm_form += li.replace(" ", '')
            
            # if "회원가입신청서" not in confirm_form:
            #     msg = "회원가입신청서 형식이 아닙니다."
            #     return redirect("url", msg)

            #==============================
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
