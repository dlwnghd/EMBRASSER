import numpy as np
import cv2
import json
import matplotlib.pyplot as plt

# cv2로 이미지 보기
def cv2_imshow(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# plt로 이미지 보기
def plt_imshow_bgr(bgr_img):
    cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(20, 15))
    plt.imshow(cvtImg)
    plt.show()

# 신청서 전처리 함수
def preprocessing(img_path):
    
    # 1️⃣이미지 읽기
    img = cv2.imread(img_path)

    # 2️⃣Gray Scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3️⃣Threshold
    th, src_after = cv2.threshold(gray, 
            0,  # thresh 값을 0으로 둠(이는 Otsu 에 의해 결정될 것임)
            255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU  # 비트연산자가 들어와있다는것은 값이 상수라는 뜻
            )

    # 4️⃣이미지 내에서 문서(신청서)의 외곽선 찾기
    contours, _ = cv2.findContours(
        src_after, 
        mode=cv2.RETR_LIST, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )

    app = []
    app_area = []

    # 5️⃣OCR할 문서의 외곽선 찾기
    for pts in contours:
        if cv2.contourArea(pts)  < 400000 : continue
        approx = cv2.approxPolyDP(        # (K, 1, 2) 형태가 나온다~ return 값이~
        pts,                              # curve
        cv2.arcLength(pts, True) * 0.02,  # epsilon
        True,                             # closed
        )
        app.append(approx)

    for i in range(len(app)):
        app_area.append(cv2.contourArea(app[i])) # 여기서 app_area_list 생성

    max_area = app[np.argmax(app_area)]

    # 6️⃣이미지 위에 외곽선 그리기
    cv2.polylines(
                img,        # 영상 위에 바로 그림.
                [max_area],
                True,            # isClosed = True
                (0, 0, 255),
                thickness = 5# 색상
            )

    seq = np.squeeze(max_area)
    
    pts = np.lexsort((seq[:,1], seq[:, 0])) 
    pts1 = seq[pts]
    
    if pts1[0, 1] > pts1[1, 1]:
        pts1[[0, 1]] = pts1[[1, 0]]

    if pts1[2, 1] < pts1[3, 1]:
        pts1[[2, 3]] = pts1[[3, 2]]
    

    top_left = pts1[0 , :]      # 좌측 상단
    top_right = pts1[3 , :]     # 우측 상단

    bottom_left = pts1[1 , :]   # 좌측 하단
    bottom_right = pts1[2 , :]  # 우측 하단


    pts1 = np.float32([top_left, top_right, 
                    bottom_right, bottom_left])

    w1 = abs(bottom_right[0] - bottom_left[0])  # 하단 넓이
    w2 = abs(top_right[0] - top_left[0])        # 상단 넓이
    h1 = abs(top_right[1] - bottom_right[1])    # 우측 높이
    h2 = abs(top_left[1] - bottom_left[1])      # 좌측 높이

    max_width = max([w1, w2])                   # 최대 넓이
    max_height = max([h1, h2])                  # 최대 높이

    pts2 = np.float32([[0, 0], 
                [max_width-1, 0], 
                [max_width-1, max_height-1], 
                [0, max_height-1]])

    # 투시를 변환에 사용할 3 x 3 행렬 생성
    M = cv2.getPerspectiveTransform(pts1, pts2)

    # 이미지를 평평하게 만들기
    dst = cv2.warpPerspective(img, M, (max_width, max_height))
    
    # warpPerspective 한 후 전처리 하기
    
    # GrayScale
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    
    # GaussianBlur
    img_blurred = cv2.GaussianBlur(
        gray,             # 
        ksize = (3, 3),   # 색을 뭉개는 범위??
        sigmaX = 0,   # x방향 sigma
    )

    # Blur_Threshold
    img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred, 
        maxValue=255.0, 
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        thresholdType=cv2.THRESH_BINARY, 
        blockSize=19, 
        C=9
    )
    
    # =====================================================================
    
    # 이미지 저장 경로
    image_path = "{}_pre.jpg".format(img_path)

    # 이미지 저장
    cv2.imwrite(image_path, img_blur_thresh)
    return image_path

# 이미지 바운딩 처리
def bounding_img(image_file, json_file):
    file = image_file
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    file = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    with open(json_file, encoding = 'UTF8' ) as data_file:
        local = json.load(data_file)

    copy_img = img.copy()                   # 이미지 복사
    for i in local['images'][0]["fields"]:
        point=i['boundingPoly']['vertices']

        x=int(point[0]['x'])
        y=int(point[0]['y'])
        h=int(point[2]["x"])
        w=int(point[2]['y'])

        # BoundingRect 그리기
        cv2.rectangle(copy_img,pt1=(x, y), pt2=(h,w), color=(0, 255, 0), thickness=3)
            
    # 바운딩 이미지 저장
    image_path = "{}_bounding.jpg".format(image_file)
    cv2.imwrite(image_path, copy_img)
    
    return image_path

from operator import itemgetter
import re

# OCR
class OCR:
    # from operator import itemgetter
    # import re

    # 초기화 매서드
    def __init__(self, local):
        self.local = local
        self.main_sentences = []

    # ==================단어 연결==================
    def plusword(self):
        sentence = []
        
        for i in range(len(self.local['images'][0]['fields'])):
            sentence.append(self.local['images'][0]['fields'][i]['inferText'])
        
        return sentence
    
    # =============우측 하단 좌표값 뽑기============
    # 입력받은 단어(input_test)의 우측하단의 좌표, 전체 꼭지점의 좌표, 높이를 return
    def max_pos(self, input_text): 
        pos = []
        standard = {}     # '성명(한글)' x,y 좌표를 담을 변수 선언
        standard_h = 0
        for dictionary in self.local['images'][0]["fields"]:    
            # 사각형의 x, y 값들을 비교하여 큰 값을 가지고있는 좌표값을 딕셔너리로 저장.
            dictionary_sorted = sorted(dictionary['boundingPoly']['vertices'], key = itemgetter('y', 'x'))

            dictionary_sorted_max = dictionary_sorted[-1]                               # 가장 큰 값을 저장
            pos.append(dictionary_sorted_max)                                           # 저장된걸 pos 리스트에 담음

            if dictionary['inferText'] == input_text :                                  # 텍스트면 
                standard = dictionary_sorted_max                                        # standard : 우측 하단 좌표
                standard_h = abs(dictionary_sorted[0]['y'] - dictionary_sorted[2]['y']) # 높이

        return standard, pos, standard_h
    
    
    # ================텍스트 찾기==================
    #            (self, 찾을 텍스트, 사이 텍스트용, 추가 상단, 추가 하단, 좌측 넓이, 우측 넓이, 방향(가로,세로))
    def find_text(self, input_text, input_text2=None, h_up=0.7, h_down=0.5, w_left=5, w_right=3, direction=0):
        i = 0
        i_list = []
        text = ''
        one_max, all_max, h = self.max_pos(input_text)

        # ================가로 방향================
        if direction == 0:
            if input_text2:                     # 기준이 2개일때(사이의 텍스트를 찾을 때)
                two_max, _, _ = self.max_pos(input_text2)
                for pos in all_max:
                    # 첫번째 단어의 우측하단의 x 값이 첫번째 단어의 각 모서리의 x값보다 작고
                    # 두번째 단어의 우측하단의 x 값이 첫번째 단어의 각 모서리의 x값보다 크고
                    # 첫번째 단어의 우측하단의 [y값 - (높이 * 상단비율)]이 첫번째 단어의 각 모서리의 y값보다 작고
                    # 두번째 단어의 우측하단의 [y값 + (높이 * 하단비율)]이 첫번째 단어의 각 모서리의 y값보다 크다면
                    if one_max['x'] < pos['x'] and two_max['x'] > pos['x'] and one_max['y'] - (h * h_up) < pos['y'] and one_max['y'] + (h * h_down) > pos['y']:
                            i_list.append(i)
                    i+=1
            else:
                for pos in all_max:
                    # 첫번째 단어의 우측하단의 x 값이 첫번째 단어의 각 모서리의 x값보다 작고
                    # 첫번째 단어의 우측하단의 [y값 - (높이 * 상단비율)]이 첫번째 단어의 각 모서리의 y값보다 작고
                    # 첫번째 단어의 우측하단의 [y값 + (높이 * 하단비율)]이 첫번째 단어의 각 모서리의 y값보다 크다면
                    if one_max['x'] < pos['x'] and one_max['y'] - (h * h_up) < pos['y'] and one_max['y'] + (h * h_down) > pos['y']:
                        i_list.append(i)
                    i+=1

        # ================세로 방향================
        elif direction == 1:
            if input_text2:                     # 기준이 2개일때(사이의 텍스트를 찾을 때)
                two_max, _, _ = self.max_pos(input_text2)
                for pos in all_max:
                    # 첫번째 단어의 우측하단의 y 값이 첫번째 단어의 각 모서리의 y값보다 작고
                    # 첫번째 단어의 우측하단의 y 값이 두번째 단어의 각 모서리의 y값보다 크다면
                    if one_max['y'] < pos['y'] and two_max['y'] > pos['y']: 
                            i_list.append(i)
                    i+=1
            else:
                for pos in all_max:
                    # 첫번째 단어의 우측하단의 y 값이 첫번째 단어의 각 모서리의 y값보다 작고
                    # 첫번째 단어의 우측하단의 [y값 + (높이 * 하단비율)]이 첫번째 단어의 각 모서리의 y값보다 크고
                    # 첫번째 단어의 우측하단의 [x값 - (높이 * 좌측넓이비율)]이 첫번째 단어의 각 모서리의 x값보다 작고
                    # 첫번째 단어의 우측하단의 [x값 + (높이 * 우측넓이비율)]이 첫번째 단어의 각 모서리의 x값보다 크다면
                    if one_max['y'] < pos['y'] and one_max['y'] + (h * h_down) > pos['y'] and one_max['x'] - (h * w_left) < pos['x'] and one_max['x'] + (h * w_right) > pos['x']:
                        i_list.append(i)
                    i+=1

        for i in i_list:
            # ================주소일 경우================
            if input_text == "주소":
                text += self.local['images'][0]["fields"][i]['inferText'] + " "
            else:
                text += self.local['images'][0]["fields"][i]['inferText']
        return text.replace('\n','')

    # ====================신청서====================
    def result_application (self, sentences:dict):
        result = {}
        for k,v in sentences.items():
            if type(k) == tuple:
                text = self.find_text(k[0], k[1])
                result[v] = text.strip()
            else :
                if k == '주소':
                    text = self.find_text(k,h_up=1.5, h_down=1.5)
                else :
                    text = self.find_text(k)
                result[v] = text.strip() 
        return result  
    
    
    # =================주민등록등본=================
    def result_IDcard(self, input_text):
    
        name_li = []

        while True:
            name_dic = {}
            text = self.find_text(input_text, h_down=3, direction=1)

            if text : 
                name_dic['name'] = re.findall('^[가-힣]+',text)[0]
                name_dic['code'] = re.findall('([0-9]{6}-[0-9]{7})',text)[0]
                input_text = text[-14:]     # ⭐input_text 업데이트
                name_li.append(name_dic)    # ⭐namve_li에 추가
            else:
                break
        return name_li

    # ================가족관계증명서=================
    def result_family(self, input_text):
        family_li = []
        while True:
            text = self.find_text(input_text, h_down=4, direction=1)
            if text : 
                family_li.append(text)
                input_text = text
            else:
                break
        return family_li[:-1]

    # ================혼인관계증명서===============
    def result_marry (self, sentences:dict):
        result_dic = {}
        
        for k, v in sentences.items():
            text = self.find_text(k)
            result_dic['name'+v] = re.findall('^[가-힣]+',text)[0]
            result_dic['code'+v] = re.findall('([0-9]{6}-[0-9]{7})',text)[0]
                
        return result_dic