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
    
    image_path = "{}_resized_pre.jpg".format(img_path)

    cv2.imwrite(image_path, dst)
    
    return image_path


# 웹 페이지 바운딩 이미지 올릴 자료

import numpy as np
import cv2

def bounding_img(image_file, json_file):
    file = image_file
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    file = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    with open(json_file, encoding = 'UTF8' ) as data_file:
        local = json.load(data_file)

    copy_img = img.copy()
    for i in local['images'][0]["fields"]:
        point=i['boundingPoly']['vertices']

        x=int(point[0]['x'])
        y=int(point[0]['y'])
        h=int(point[2]["x"])
        w=int(point[2]['y'])

        cv2.rectangle(copy_img,pt1=(x, y), pt2=(h,w), color=(0, 255, 0), thickness=3)
        
    plt_imshow_bgr(copy_img)
    
    
    # 바운딩 이미지 저장
#     image_path = "{}_bounding.jpg".format(image_file)
#     cv2.imwrite(image_path, copy_img)
    
#     return image_path
    
bounding_img(image_file, json_file)