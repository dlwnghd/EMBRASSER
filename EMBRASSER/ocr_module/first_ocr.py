import numpy as np
import cv2
import matplotlib.pyplot as plt

def cv2_imshow(image):
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def plt_imshow_bgr(bgr_img):
    cvtImg = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(20, 15))
    plt.imshow(cvtImg)
    plt.show()
    
# 신청서 전처리 함수

def preprocessing(img_path):
    
    print("여기들어옴!")
    img = cv2.imread(img_path)

    height, width, channel = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_blurred = cv2.GaussianBlur(
        gray,
        ksize = (3, 3),   # 색을 뭉개는 범위??
        sigmaX = 0,   # x방향 sigma
    )

    img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred, 
        maxValue=255.0, 
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        thresholdType=cv2.THRESH_BINARY, 
        blockSize=19, 
        C=9
    )

    contours, _ = cv2.findContours(
        img_blur_thresh, 
        mode=cv2.RETR_LIST, 
        method=cv2.CHAIN_APPROX_SIMPLE
    )


    temp_result = np.zeros((height, width, channel), dtype=np.uint8)

    # ★★★★★★★★★
    contours_dict = []   # <- 여기다가 contours 들의 정보를 다 저장하겠습니다.


    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)


        # 위 boundindRect 도 그려도 보구..
        cv2.rectangle(temp_result, pt1=(x, y), pt2=(x+w, y+h), color=(255, 255, 255), thickness=2)

        # 데이터를 만들고 insert to dict
        contours_dict.append({
            'contour': contour,
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'cx': x + (w / 2),  # center X
            'cy': y + (h / 2)   # center Y
        })



    MIN_AREA = 400000 # 최소 넓이
    MIN_WIDTH, MIN_HEIGHT = 2, 8  # 최소 너비, 높이
    MIN_RATIO, MAX_RATIO = 0.25, 1.0  # 너비-높이 비율의 최대/최소


    # ★★★★★★★★★★
    possible_contours = []  # 위 조건에 맞는 것들을 걸러낸 것들을 담아보겠습니다

    cnt = 0
    for d in contours_dict:  # 위에서 저장했었던 contours_dict 를 순환하면서

        area = d['w'] * d['h']   # 넓이 계산
        ratio = d['w'] / d['h']  # 너비-높이 비율 계산


        # 조건에 맞는 것들만 골라서 possible_contours 에 담는다.
        if area > MIN_AREA \
        and d['w'] > MIN_WIDTH and d['h'] > MIN_HEIGHT \
        and MIN_RATIO < ratio < MAX_RATIO:
            d['idx'] = cnt     # 조건에 맞는 각 contour 에 idx 값을 매겨놓기
                               # 나중에 조건에 맞는 윤곽선들의 idx 만 따로 빼놓음

            cnt += 1
            possible_contours.append(d)


    x = possible_contours[0]['x']
    y = possible_contours[0]['y']
    w = possible_contours[0]['w']
    h = possible_contours[0]['h']

    top_left = (x, y)
    top_right = (x+w, y)

    bottom_left = (x, y+h)
    bottom_right = (x+w, y+h)


    pts1 = np.float32([top_left, top_right, 
                      bottom_right, bottom_left])

    w1 = abs(bottom_right[0] - bottom_left[0])
    w2 = abs(top_right[0] - top_left[0])
    h1 = abs(top_right[1] - bottom_right[1])
    h2 = abs(top_left[1] - bottom_left[1])

    max_width = max([w1, w2])
    max_height = max([h1, h2])

    pts2 = np.float32([[0, 0], 
                      [max_width-1, 0], 
                      [max_width-1, max_height-1], 
                      [0, max_height-1]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (max_width, max_height))
    
    image_path = "{}_pre.jpg".format(img_path)

    # 프리프로세싱한 이미지 저장
    cv2.imwrite(image_path, dst)

    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    print("image_path : ", image_path)
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    
    return image_path

from operator import itemgetter
import re

class OCR:
    # from operator import itemgetter
    # import re

    def __init__(self, local):
        self.local = local
        self.main_sentences = []

    # ===========================================
    def main_sentences(self):
        for i in range(len(self.local['images'][0]['fields'])):
            self.main_sentences.append(self.local['images'][0]['fields'][i]['inferText'])
        
        return self.main_sentences
    
    # ===========================================
    def max_pos(self, input_text):
        pos = []
        standard = {}     # '성명(한글)' x,y 좌표를 담을 변수 선언
        standard_h = 0
        for dictionary in self.local['images'][0]["fields"]:    
            # 사각형의 x, y 값들을 비교하여 큰 값을 가지고있는 좌표값을 딕셔너리로 저장.
            dictionary_sorted = sorted(dictionary['boundingPoly']['vertices'], key = itemgetter('y', 'x'))

            dictionary_sorted_max = dictionary_sorted[-1]
            pos.append(dictionary_sorted_max)    # 저장된걸 pos 리스트에 담음

            if dictionary['inferText'] == input_text :            # 텍스트면 
                standard = dictionary_sorted_max                            # 변수에 담기.
                standard_h = abs(dictionary_sorted[0]['y'] - dictionary_sorted[2]['y'])

        return standard, pos, standard_h
    
    
    # ===========================================
    def find_text(self, input_text, input_text2=None, h_up=0.7, h_down=0.5, w_left=5, w_right=3, direction=0):
        i = 0
        i_list = []
        text = ''
        one_max, all_max, h = self.max_pos(input_text)

        if direction == 0:                    # 가로 방향
            if input_text2:                     # 기준이 2개일때
                two_max, _, _ = self.max_pos(input_text2)
                for pos in all_max:
                    if one_max['x'] < pos['x'] and two_max['x'] > pos['x'] and one_max['y'] - (h * h_up) < pos['y'] and one_max['y'] + (h * h_down) > pos['y']:
                            i_list.append(i)
                    i+=1
            else:
                for pos in all_max:
                    if one_max['x'] < pos['x'] and one_max['y'] - (h * h_up) < pos['y'] and one_max['y'] + (h * h_down) > pos['y']:
                        i_list.append(i)
                    i+=1

        elif direction == 1:                # 세로 방향
            if input_text2:                     # 기준이 2개일때
                two_max, _, _ = self.max_pos(input_text2)
                for pos in all_max:
                    if one_max['y'] < pos['y'] and two_max['y'] > pos['y']:     # 아직 안만듬.
                            i_list.append(i)
                    i+=1
            else:
                for pos in all_max:
                    if one_max['y'] < pos['y'] and one_max['y'] + (h * h_down) > pos['y'] and one_max['x'] - (h * w_left) < pos['x'] and one_max['x'] + (h * w_right) > pos['x']:
                        i_list.append(i)
                    i+=1

        for i in i_list:
            text += self.local['images'][0]["fields"][i]['inferText']

        return text.replace('\n','')
    
    
    # ===========================================
    # def result_application (self, sentences:list, sentences_dic:list):
    #     result = {}
    #     for sentence, sentence_dic in zip(sentences, sentences_dic):
    #         if type(sentence) == tuple:
    #             text = self.find_text(sentence[0], sentence[1])
    #             result[sentence_dic] = text.strip()
    #         else :
    #             if sentence == '주소':
    #                 text = self.find_text(sentence,h_up=1.5, h_down=1.5)
    #             else :
    #                 text = self.find_text(sentence)

    #             result[sentence_dic] = text.strip() 
    #     return result 


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
    
    
    # ===========================================
    def result_IDcard(self, input_text):
    
    
        name_li = []


        while True:
            name_dic = {}
            text = self.find_text(input_text, h_down=3, direction=1)

            if text : 
                name_dic['name'] = re.findall('^[가-힣]+',text)[0]
                name_dic['code'] = re.findall('([0-9]{6}-[0-9]{7})',text)[0]
                input_text = text[-14:]
                name_li.append(name_dic)
            else:
                break
        return name_li


    # ===========================================
    def result_family(self, input_text):
        family_li = []
        while True:
            text = self.find_text(input_text, h_down=3, direction=1)
            if text : 
                family_li.append(text)
                input_text = text
            else:
                break
        return family_li[:-1]