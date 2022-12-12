from django.core.files.storage import FileSystemStorage
from ocr_module.first_ocr import *
import requests
import uuid
import os
import json
import time

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse

from EMBRASSER.models import Members

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
                    partner_check = True
                    break
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