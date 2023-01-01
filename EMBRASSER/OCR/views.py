from django.core.files.storage import FileSystemStorage
import requests
import uuid
import os
import json
import time

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse

from EMBRASSER.models import Members
from django.core.paginator import Paginator

from ocr_module.first_ocr import *
from ocr_module.model.utils.Preprocess import Preprocess
from ocr_module.model.intent.IntentModel import IntentModel

from django.db.models import Q      # filter OR 사용하는 모듈



# 승현, 희지 import
from django.db.models import Count, Avg, Sum

# 회원가입신청서 OCR
def coocr_first (request):
    context = {}
    context['menutitle'] = '회원 등록'

    imgname = ''
    image_file = ''
    bounding_path = ''

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
            
            # 신청서
            try:
                image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            except Exception as e:
                print(e)
                image_file = fs.base_location + fs.url(imgname)
                
            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

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

            ocr = OCR(local)
            
            all_sentences = ocr.plusword()
            
            confirm_form = ""
            for li in all_sentences:
                confirm_form += li.replace(" ", '')
                
            if "회원가입신청서" not in confirm_form:
                msg = {'alrt' : False,
                    'imgname' : ''}
                return render(request, 'member_ocr_f.html', msg)

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(local, outfile, indent=4, ensure_ascii=False)

            bounding_path = bounding_img(image_file, json_file)

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

            context['resulttext'] = ocr.result_application(sentences)

    # context에 데이터 담기
    context['imgname'] = imgname
    context['pre_img'] = image_file[14:]
    context['bounding_img'] = bounding_path[14:]

    return render(request, 'member_ocr_f.html', context)

# 주민등록등본 OCR
def coocr_second (request):
    name = request.POST.get('name')
    age = request.POST.get('age')
    p_code = request.POST.get('p_code')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    addr = request.POST.get('addr')
    religion = request.POST.get('religion')
    scholar = request.POST.get('scholar')
    sex = request.POST.get('sex')
    job = request.POST.get('job')
    salary = request.POST.get('salary')
    property = request.POST.get('property')
    debt = request.POST.get('debt')
    re_marry = request.POST.get('re_marry')
    drink = request.POST.get('drink')
    smoke = request.POST.get('smoke')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    family = request.POST.get('family')
    
    context = {}
    context['menutitle'] = '회원 등록'

    imgname = ''
    image_file = ''
    bounding_path = ''
    
    name_check = ''
    pcode_check = ''

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
            api_url = 'https://9d3gh23gql.apigw.ntruss.com/custom/v1/19510/d807e8f68a4ff6abcef26f0ed8d896695550657a3a3eb34e243eb056c9e8e474/general'
            secret_key = 'ZEVjYW53TlpiYkp4eWxGeUJNQ1RTWmJ1aUlETW1ZdkY='

            # 주민등록번호
            try:
                image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            except Exception as e:
                print(e)
                image_file = fs.base_location + fs.url(imgname)
                
            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

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

            ocr = OCR(local)
            
            all_sentences = ocr.plusword()
            
            confirm_form = ""
            for li in all_sentences:
                confirm_form += li.replace(" ", '')
                
            print("confirm_form:", confirm_form)
            
            if "주민등록표" not in confirm_form:
                msg = {'alrt' : False,
                    'imgname' : '',
                    'namecheck' : '',
                    'pcodecheck' : ''}
                return render(request, 'member_ocr_s.html', msg)

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(local, outfile, indent=4, ensure_ascii=False)
            
            bounding_path = bounding_img(image_file, json_file)
            
            names = ocr.result_IDcard('주민등록번호')
            
            name_check = False
            pcode_check = False
            for n in names:
                if n['name'] == name:
                    name_check = True
                    if n['code'] == p_code:
                        pcode_check = True
                        break
            for n in names:
                if n['code'] == p_code:
                    pcode_check = True
                    break

    context['resulttext'] = {
        'name' : name,
        'age' : age,
        'p_code' : p_code,
        'phone' : phone,
        'email' : email,
        'addr' : addr,
        'sex' : sex,
        'height' : height,
        'weight' : weight,
        'family' : family,
        'job' : job,
        'salary' : salary,
        'property' : property,
        'debt' : debt,
        'religion' : religion,
        'drink' : drink,
        'smoke' : smoke,
        'scholar' : scholar,
        're_marry' : re_marry,
    }

    # context에 데이터 담기
    context['imgname'] = imgname
    context['pre_img'] = image_file[14:]
    context['bounding_img'] = bounding_path[14:]
    context['namecheck'] = name_check
    context['pcodecheck'] = pcode_check
    
    return render(request, 'member_ocr_s.html', context)

# 가족관계증명서 OCR
def coocr_third (request):
    name = request.POST.get('name')
    age = request.POST.get('age')
    p_code = request.POST.get('p_code')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    addr = request.POST.get('addr')
    religion = request.POST.get('religion')
    scholar = request.POST.get('scholar')
    sex = request.POST.get('sex')
    job = request.POST.get('job')
    salary = request.POST.get('salary')
    property = request.POST.get('property')
    debt = request.POST.get('debt')
    re_marry = request.POST.get('re_marry')
    drink = request.POST.get('drink')
    smoke = request.POST.get('smoke')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    family = request.POST.get('family')
    
    context = {}
    context['menutitle'] = '회원 등록'

    imgname = ''
    image_file = ''
    bounding_path = ''
    
    partner_check = ''
    child = 0

    # Upload할 파일을 Web에서 받아온다면
    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile','')

        if uploadfile != '':
            name_old = uploadfile.name

            # 이미지 파일 저장 경로                         
            fs = FileSystemStorage(location = 'static/source')

            # 이미지 파일을 저장할때 이미지명
            imgname = fs.save(f'image/src-{name_old}',uploadfile)
            img_name, file_type = os.path.splitext(imgname)
            
            # API 키 불러오기
            api_url = 'https://9d3gh23gql.apigw.ntruss.com/custom/v1/19510/d807e8f68a4ff6abcef26f0ed8d896695550657a3a3eb34e243eb056c9e8e474/general'
            secret_key = 'ZEVjYW53TlpiYkp4eWxGeUJNQ1RTWmJ1aUlETW1ZdkY='
            
            # 가족관계증명서
            try:
                image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            except Exception as e:
                print(e)
                image_file = fs.base_location + fs.url(imgname)
                
            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

            # 결과 json
            request_json = {
                'images': [
                    {
                        'format': file_type.replace(".",""),    # 포맷 타입
                        'name': 'demo'                          # 이름
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

            ocr = OCR(local)

            all_sentences = ocr.plusword()

            confirm_form = ""
            for li in all_sentences:
                confirm_form += li.replace(" ", '')

            if "가족관계증명서" not in confirm_form:
                msg = {'alrt' : False,
                    'imgname' : ''}
                return render(request, 'member_ocr_t.html', msg)

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(local, outfile, indent=4, ensure_ascii=False)

            bounding_path = bounding_img(image_file, json_file)

            family_li = ocr.result_family('구분')

            partner_check = False
            for f in family_li:
                if "배우자" in f :
                    context['msg'] = "배우자가 있습니다.<br>배우자가 있을 경우 회원 등록이 불가능합니다.<br>확인 후 문서를 처음부터 다시 등록해주세요."
                    context['flag'] = False
                    return render(request, 'member_ocr_fine.html', context)

            for f in family_li:
                if "자녀" in f :
                    child = 1
                    break

    context['resulttext'] = {
        'name' : name,
        'age' : age,
        'p_code' : p_code,
        'phone' : phone,
        'email' : email,
        'addr' : addr,
        'sex' : sex,
        'height' : height,
        'weight' : weight,
        'family' : family,
        'job' : job,
        'salary' : salary,
        'property' : property,
        'debt' : debt,
        'religion' : religion,
        'drink' : drink,
        'smoke' : smoke,
        'scholar' : scholar,
        're_marry' : re_marry,
        'partner_check' : partner_check,
        'child' : child,
    }

    # context에 데이터 담기
    context['imgname'] = imgname
    context['pre_img'] = image_file[14:]
    context['bounding_img'] = bounding_path[14:]
    
    return render(request, 'member_ocr_t.html', context)

# 회원 등록
def join_member(request):
    context = {}
    
    name = request.POST.get('name')
    age = int(request.POST.get('age'))
    p_code = request.POST.get('p_code')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    addr = request.POST.get('addr')
    religion = request.POST.get('religion')
    scholar = request.POST.get('scholar')
    sex = request.POST.get('sex')
    job = request.POST.get('job')
    salary = request.POST.get('salary')
    property = request.POST.get('property')
    debt = request.POST.get('debt')
    re_marry = request.POST.get('re_marry')
    drink = request.POST.get('drink')
    smoke = request.POST.get('smoke')
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    family = request.POST.get('family')
    child = request.POST.get('child')

    salary = int(salary.replace(",", "").replace(".", ''))
    property = int(property.replace(",", "").replace(".", ''))
    debt = int(debt.replace(",", "").replace(".", ''))

    if sex == "남자" or sex == '남':
        sex = '남'
    elif sex == "여자" or sex == "여":
        sex = '여'
    else:
        sex = "모름"

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
    
    # ======== 등급 매기기 =========
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

    try :
        Members.objects.get(p_code=p_code)
        context['msg'] = f"{name}님은 이미 등록된 회원입니다."
        context['flag'] = False
        
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
                child = child,
                grade = grade
            )
            context['flag'] = True
            context['name'] = name
            context['grade'] = grade
            context['msg'] = "등록이 완료 되었습니다."
        except Exception as ex:
            print(ex)
            context['msg'] = "등록에 실패했습니다.<br>문서를 처음부터 다시 등록해주세요."
            context['flag'] = False
            
        print(e)
    return render(request, 'member_ocr_fine.html', context)

# 이벤트 OCR1
def event_first (request):
    context = {}
    context['menutitle'] = '이벤트 참여 등록'

    imgname = ''
    image_file = ''
    bounding_path = ''
    
    bone_check = ''
    bae_check = ''

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
            
            # 신청서
            try:
                image_file = preprocessing(fs.base_location + fs.url(imgname)) # 여기 경로를 수정
            except Exception as e:
                print(e)
                image_file = fs.base_location + fs.url(imgname)
                
            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

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

            ocr = OCR(local)
            
            all_sentences = ocr.plusword()
            
            confirm_form = ""
            for li in all_sentences:
                confirm_form += li.replace(" ", '')
            
            if "혼인관계증명서" not in confirm_form:
                msg = {'alrt' : False,
                    'imgname' : ''}
                return render(request, 'event_ocr_f.html', msg)

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(local, outfile, indent=4, ensure_ascii=False)

            bounding_path = bounding_img(image_file, json_file)

            sentences = {'본인': "bone", "배우자": "bae"}

            marry_dict = ocr.result_marry(sentences)
            
            try :
                Members.objects.get(name=marry_dict['namebone'], p_code=marry_dict['codebone'])
                bone_check = True
                bae_check = False
                context['resulttext'] = marry_dict
                Members.objects.get(name=marry_dict['namebae'], p_code=marry_dict['codebae'])
                bae_check = True
                context['flag'] = True
                context['resulttext'] = marry_dict

            except Exception as e:
                context['flag'] = False

    # context에 데이터 담기
    context['imgname'] = imgname
    context['pre_img'] = image_file[14:]
    context['bounding_img'] = bounding_path[14:]
    context['bone_check'] = bone_check
    context['bae_check'] = bae_check

    return render(request, 'event_ocr_f.html', context)

# 이벤트 OCR2
def event_second (request):
    context = {}
    context['menutitle'] = '이벤트 참여 등록'

    imgname = ''
    image_file = ''
    bounding_path = ''
    
    bone_check = ''
    bae_check = ''
    
    namebone = request.POST.get('namebone')
    codebone = request.POST.get('codebone')
    namebae = request.POST.get('namebae')
    codebae = request.POST.get('codebae')
    
    context['marry_dict'] = {
        "namebone" : namebone,
        "codebone" : codebone,
        "namebae" : namebae,
        "codebae" : codebae
    }

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
            
            image_file = fs.base_location + fs.url(imgname)

            json_file = fs.base_location + '/json/' + img_name[6:] + '.json'  # ~.jpg.json 형식

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
            
            # 💙💙💙 이 부분 수정해야 함 ! =====================
            ocr = OCR(local)
            
            all_sentences = ocr.plusword()
            
            confirm_form = ""
            for li in all_sentences:
                confirm_form += li.replace(" ", '') + ' '
            
            # CNN + Bi-LSTM 모델 적용 부분
            # 전처리 객체 생성
            p = Preprocess(
                word2index_dic = 'ocr_module/model/train_tools/invitation.bin',
                userdic = 'ocr_module/model/utils/user_dic.tsv'
            )
            
            # 의도 파악 모델 (1)
            intent = IntentModel(model_name='ocr_module/model/intent/Epoch_004_Val_0.000.h5', preprocess=p)
            
            intent_predict = intent.predict_class(confirm_form)
            intent_name = intent.labels[intent_predict]

            if intent_name != "청첩장":
                msg = {'alrt' : False,
                    'imgname' : ''}
                return render(request, 'event_ocr_s.html', msg)

            # ====================================================

            with open(json_file, 'w', encoding='utf-8') as outfile:
                json.dump(local, outfile, indent=4, ensure_ascii=False)

            bounding_path = bounding_img(image_file, json_file)
            
            inv_sentences = confirm_form.replace(" ", '')

            try :
                if namebone in inv_sentences:
                    bone_check = 0
                elif namebone[1:] in inv_sentences:
                    bone_check = 1
                else:
                    bone_check = 2

                if namebae in inv_sentences:
                    bae_check = 0
                elif namebae[1:] in inv_sentences:
                    bae_check = 1
                else:
                    bae_check = 2

            except Exception as e:
                print(e)
                
    # context에 데이터 담기
    context['imgname'] = imgname
    context['pre_img'] = image_file[14:]
    context['bounding_img'] = bounding_path[14:]
    context['bone_check'] = bone_check
    context['bae_check'] = bae_check
    
    return render(request, 'event_ocr_s.html', context)

# 이벤트 update
def event_update (request):
    context = {}
    
    namebone = request.POST.get('namebone')
    codebone = request.POST.get('codebone')
    namebae = request.POST.get('namebae')
    codebae = request.POST.get('codebae')

    member_bone = Members.objects.get(name=namebone, p_code=codebone)
    member_bae = Members.objects.get(name=namebae, p_code=codebae)
    
    try :
        member_bone.event = 1
        member_bae.event = 1
        
        member_bone.save()
        bone_check = True
        Members.save(member_bae)
        bae_check = True

        context['flag'] = True
        context['namebone'] = namebone
        context['namebae'] = namebae
        
    except Exception as e:
        print(e)
        context['flag'] = False
        context['msg'] = "등록에 실패했습니다.<br>문서를 처음부터 다시 등록해주세요."
        return render(request, 'event_result.html', context)
            
    return render(request, 'event_result.html', context)

# 통계
def all_statistics(request):

    # 총 가입자 수 구하기
    tot_mem = Members.objects.values('idx').aggregate(cnt = Count('idx'))
    print('tot_mem:  ', tot_mem)

    # 성비, 매칭성공률, 전체 인원 수 , 평균 연봉, 평균 나이

    # 성비
    sex = Members.objects.values('sex').annotate(all=Count('sex'))
    for d in sex:
        if d['sex'] == '남':
            man = d['all']
        elif d['sex'] =='여':
            wo = d['all']

    sex_count = man+wo

    sex_man = round(man/sex_count,2)
    sex_wo = round(wo/sex_count,2)

    # 매칭성공률
    # print("매칭이다   ",Members.objects.values("matching").annotate(rate=Count("matching")))
    matching = Members.objects.values("matching").annotate(rate=Count("matching"))


    # 전체 인원수
    all = Members.objects.aggregate(all=Count('idx'))

    # 평균 연봉
    salary_avg = Members.objects.aggregate(avg_salary=Avg('salary'))

    # 평균 나이
    age_avg = Members.objects.aggregate(avg_age=Avg('age'))



    mat_tot = 0

    for mat in matching:
        
        if mat['matching'] in [1,2]:
            mat_tot += mat['rate']
            
            if mat['matching'] == 1:
                mat_1 = mat['rate']
            elif mat['matching'] == 2:
                mat_2 = mat['rate']
        else:
            mat_0 = mat['rate']   # 매칭 전 인원 수


    mat_success = mat_2 / mat_tot * 100    
    mat_fail = mat_1 / mat_tot * 100    
    
    context = {
        'tot_mem': tot_mem['cnt'],  
        "mat_success" : mat_success,
        "mat_fail" : mat_fail,
        'mat_0' : mat_0,  # 매칭 전 인원수
        'sex_man' :sex_man ,
        'sex_wo' :sex_wo ,
        'all' : all['all'],
        'salary_avg' : round(salary_avg['avg_salary']),
        'age_avg' : round(age_avg['avg_age'], 2)
    }


    return render(request, 'member_statistics/all_statistics.html', context)

# 등급 통계
def grade_statistics(request):
    context = {}
    
    context['A_2'] = 0
    context['B_2'] = 0
    context['C_2'] = 0
    # 등급별 / 성비, 매칭성공률, 전체 인원 수 , 평균 연봉, 평균 나이

    # 성비
    sex = Members.objects.values('grade').annotate(all=Count('sex'))

    print('sexxxx : ', sex)


    # for d in sex:
    #     if d['grade']
    #     if d['sex'] == '남':
    #         man = d['all']
    #     elif d['sex'] =='여':
    #         wo = d['all']

    # sex_count = man+wo

    # sex_man = round(man/sex_count,2)
    # sex_wo = round(wo/sex_count,2)

    # 매칭성공률
    matching = Members.objects.values('grade', "matching").annotate(mat_count=Count("matching"))
    print('matching: ',matching)

    # mat_suc_fail = 0   # 매칭 성공 or 실패한 사람
    mat_suc = 0        # 매칭 성공한 사람
    
    for mat in matching:

        if mat['grade'] == 'F':

            if mat['matching'] == 1:
                context['F_1'] = mat['mat_count']


            elif mat['matching'] == 2:
                context['F_2'] = mat['mat_count']
                mat_suc += mat['mat_count']
                

            else:
                context['F_0'] = ''

        elif mat['grade'] == 'C':

            if mat['matching'] == 1:
                context['C_1'] = mat['mat_count']

            elif mat['matching'] == 2:
                context['C_2'] = mat['mat_count']
                mat_suc += mat['mat_count']

            else:
                context['B_0'] = ''

        elif mat['grade'] == 'B':

            if mat['matching'] == 1:
                context['B_1'] = mat['mat_count']

            elif mat['matching'] == 2:
                context['B_2'] = mat['mat_count']
                mat_suc += mat['mat_count']

            else:
                context['C_0'] = ''
                
        elif mat['grade'] == 'A':

            if mat['matching'] == 1:
                context['A_1'] = mat['mat_count']
                

            elif mat['matching'] == 2:
                context['A_2'] = mat['mat_count']

                mat_suc += mat['mat_count']

            else:
                context['A_0'] = ''

        elif mat['grade'] == 'S':

            if mat['matching'] == 1:
                context['S_1'] = mat['mat_count']
                

            elif mat['matching'] == 2:
                context['S_2'] = mat['mat_count']
                mat_suc += mat['mat_count']

            else:
                context['S_0'] = ''

    # 전체 인원수
    all = Members.objects.all().values('grade').annotate(all=Count('idx'))

    # 평균 연봉
    salary_avg = Members.objects.values('grade').annotate(avg_salary=Avg('salary'))

    # 평균 나이
    age_avg = Members.objects.values('grade').annotate(avg_age=Avg('age'))

    for ag in salary_avg:
        if ag['grade'] == "S":
            context['s_S'] = round(ag['avg_salary'])
        elif ag['grade'] == "A":
            context['s_A'] = round(ag['avg_salary'])
        elif ag['grade'] == "B":
            context['s_B'] = round(ag['avg_salary'])
        elif ag['grade'] == "C":
            context['s_C'] = round(ag['avg_salary'])
        elif ag['grade'] == "F":
            context['s_F'] = round(ag['avg_salary'])

    for ag in age_avg:
        if ag['grade'] == "S":
            context['age_S'] = round(ag['avg_age'], 2)
        elif ag['grade'] == "A":
            context['age_A'] = round(ag['avg_age'], 2)
        elif ag['grade'] == "B":
            context['age_B'] = round(ag['avg_age'], 2)
        elif ag['grade'] == "C":
            context['age_C'] = round(ag['avg_age'], 2)
        elif ag['grade'] == "F":
            context['age_F'] = round(ag['avg_age'], 2)

    for ag in all:
        if ag['grade'] == "S":
            context['a_S'] = ag['all']
        elif ag['grade'] == "A":
            context['a_A'] = ag['all']
        elif ag['grade'] == "B":
            context['a_B'] = ag['all']
        elif ag['grade'] == "C":
            context['a_C'] = ag['all']
        elif ag['grade'] == "F":
            context['a_F'] = ag['all']
    
    # 등급별 매칭 성공 확률
    context['mat_suc_S'] = round(context['S_2'] / context['a_S'] * 100, 2)
    context['mat_suc_A'] = round(context['A_2'] / context['a_A'] * 100, 2)
    context['mat_suc_B'] = round(context['B_2'] / context['a_B'] * 100, 2)
    context['mat_suc_C'] = round(context['C_2'] / context['a_C'] * 100, 2)
    context['mat_suc_F'] = round(context['F_2'] / context['a_F'] * 100, 2)


    print('context :  ', context)
    print('age_avg :  ', age_avg)

    return render(request, 'member_statistics/grade_statistics.html', context)

# 성별 통계
def sex_statistics(request):
    # 남자 남 , 여자 여 처리


    context = {}


    # 성별 / 성비, 전체 인원 수 , 평균 연봉, 평균 나이


    # 성별 인원 수
    sex_count = Members.objects.values('sex').annotate(sex_count=Count('idx'))

    for sex in sex_count:
        if sex['sex'] == '여':
            context['wo_count'] = sex['sex_count']
        elif sex['sex'] == '남':
            context['man_count'] = sex['sex_count']

    # 남자 여자 전체 수
    tot_sex = context['wo_count'] + context['man_count']

    # 남자/여자 비율
    context['wo_rate'] = round(context['wo_count']/tot_sex * 100 , 2)
    context['man_rate'] = round(context['man_count']/tot_sex * 100 , 2)




    # 평균 연봉
    salary_avg = Members.objects.values('sex').annotate(avg_salary=Avg('salary'))

    # 평균 나이
    age_avg = Members.objects.values('sex').annotate(avg_age=Avg('age'))


    for salary in salary_avg:
        if salary['sex'] =='여':
            context['wo_salary'] = round(salary['avg_salary'])

        elif salary['sex'] =='남':
            context['man_salary'] = round(salary['avg_salary'])

        else:
            context['salary_etc'] = '' 


    for age in age_avg:
        if age['sex'] =='여':
            context['wo_age'] = round(age['avg_age'], 2)

        elif age['sex'] =='남':
            context['man_age'] = round(age['avg_age'], 2)

        else:
            context['age_etc'] = '' 

        


    print('salary_avg: ', salary_avg)
    print('age_avg: ', age_avg)
    # context['salary_avg'] = salary_avg
    # context['age_avg'] = age_avg


    return render(request, 'member_statistics/sex_statistics.html', context)

# 회원 리스트 보기
def member_list(request):
    member = Members.objects.filter().values('idx', 'name', 'sex', 'religion', 'job', 'property', 'height', 'weight', 'grade', 'matching').order_by("-idx")  # 데이터 조회
    paginator = Paginator(member, 10)                   # 페이지에 표시할 갯수
    page = int(request.GET.get('page', 1))              # 처음에 보여줄 페이지 설정
    member_list = paginator.get_page(page)
    context = {'title' : '회원 목록', 'board_list' : member_list}
    return render(request, 'member_list.html', context)

# 회원 검색
def member_search(request):
    word = request.GET.get('word')

    q = Q(name__icontains=word)                            # 참고 URL : https://axce.tistory.com/10 
    q.add(Q(sex=word), q.OR)
    q.add(Q(religion=word), q.OR)
    q.add(Q(job=word), q.OR)
    q.add(Q(grade=word), q.OR)

    print('💚💚💚', word)
    member = Members.objects.filter(q).values('idx', 'name', 'sex', 'religion', 'job', 'property', 'height', 'weight', 'grade', 'matching').order_by("idx")  # 데이터 조회
    paginator = Paginator(member, 10)                   # 페이지에 표시할 갯수
    page = int(request.GET.get('page', 1))              # 처음에 보여줄 페이지 설정
    member_list = paginator.get_page(page)
    context = {'title' : '회원 목록', 'board_list' : member_list}

    return render(request, 'member_list.html', context)

# 매칭 업데이트
def member_matching(request):
    try:
        Members.objects.filter(idx=int(request.GET.get('idx'))).update(matching = int(request.GET.get('matching')))
        context = {'result' : 'ok',}
    except Exception as e:
        context = {'result' : 'no',}
    return HttpResponse(json.dumps(context), content_type="application/json")

# 회원정보 수정하기 페이지로 이동
def modify_customer(request:HttpRequest):
    idx = request.GET.get('idx')
    customer = Members.objects.get(idx=idx)
    context = {
        'customer' : customer
    }
    return render(request,'member_modify.html',context)

# 회원정보 수정 승인
def modify_confirm(request:HttpRequest):
    member = Members.objects.get(idx=request.POST.get("idx"))
    
    try:
        # 이름 수정
        new_name = request.POST.get("name")
        if new_name != '':
            member.name = new_name
        
        # 나이 수정
        new_age = request.POST.get("age")
        if new_age != '':
            member.age = new_age
        
        # 주민번호 수정 
        new_p_code = request.POST.get("p_code")
        if new_p_code != '':
            member.p_code = new_p_code

        # 전화번호 수정
        new_phone = request.POST.get("phone")
        if new_phone != '':
            member.phone = new_phone
        
        # 이메일 수정
        new_email = request.POST.get("email")
        if new_email != '':
            member.email = new_email

        # 주소 수정
        new_addr = request.POST.get("addr")
        if new_addr != '':
            member.addr = new_addr
        
        # 종교 수정
        new_religion = request.POST.get("religion")
        if new_religion != '':
            member.religion = new_religion

        # 학력 수정
        new_scholar = request.POST.get("scholar")
        if new_scholar != '':
            member.scholar = new_scholar

        # 성별 수정
        new_sex = request.POST.get("sex")
        if new_sex != '':
            member.sex = new_sex
        
        # 직업 수정
        new_job = request.POST.get("job")
        if new_job != '':
            member.job = new_job

        # 연봉 수정
        new_salary = request.POST.get("salary")
        if new_salary != '':
            member.salary = new_salary

        # 재산 수정
        new_property = request.POST.get("property")
        if new_property != '':
            member.property = new_property

        # 부채 수정
        new_debt = request.POST.get("debt")
        if new_debt != '':
            member.debt = new_debt

        # 결혼여부 수정
        new_re_marry = request.POST.get("re_marry")
        if new_re_marry != '':
            member.re_marry = new_re_marry

        # 음주 수정
        new_drink = request.POST.get("drink")
        if new_drink != '':
            member.drink = new_drink

        # 담배 수정
        new_smoke = request.POST.get("smoke")
        if new_smoke != '':
            member.smoke = new_smoke

        # 신장 수정
        new_height = request.POST.get("height")
        if new_height != '':
            member.height = new_height

        # 몸무게 수정
        new_weight = request.POST.get("weight")
        if new_weight != '':
            member.weight = new_weight

        # 가족관계 수정
        new_family = request.POST.get("family")
        if new_family != '':
            member.family = new_family

        # 매칭 수정
        new_matching = request.POST.get("matching")
        if new_matching != '':
            member.matching = new_matching
        
        # DB에 있는 Members 수정
        Members.save(member)

    except Exception as e:
        print("☢️오류발생☢️")
        print(e)
        return render(request, 'index.html')

    member = Members.objects.get(idx=request.POST.get("idx"))
    context = {
        'member' : member
    }

    return redirect('/ocr/list')

# 회원정보 삭제
def delete_customer(request:HttpRequest):
    customer = Members.objects.get(idx=request.GET.get("idx"))
    customer.delete()

    return redirect('/ocr/list')