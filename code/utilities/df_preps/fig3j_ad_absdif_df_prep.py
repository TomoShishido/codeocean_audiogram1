import cv2, os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def makeLinearEquation(x1, y1, x2, y2):
	line = {}
	if y1 == y2:
		# y軸に平行な直線
		line["y"] = y1
	elif x1 == x2:
		# x軸に平行な直線
		line["x"] = x1
	else:
		# y = mx + n
		line["m"] = (y1 - y2) / (x1 - x2)
		line["n"] = y1 - (line["m"] * x1)
	return line

def give416points(ac_sorted):
    ac_416points = []
    for i in range(416):
        ac_416points.append(0)
    
    ac_count = len(ac_sorted)
    if ac_count > 1:
        for i in range(ac_count-1):
            x0 = ac_sorted[i]['center_x']
            y0 = ac_sorted[i]['center_y']
            x1 = ac_sorted[i+1]['center_x']
            y1 = ac_sorted[i+1]['center_y']
            x_diff = x1 - x0
            y_diff = y1 - y0
            if y_diff == 0:
                for j in range(x_diff):
                    ac_416points[x0+j+1] = y0
            else:
                line =makeLinearEquation(x0, y0, x1, y1)
                for j in range(x_diff):
                    point_y = int(line['m']*(x0+j+1) + line['n'])
                    ac_416points[x0+j+1] = point_y
    return ac_416points

def RLacdata_differential_df(yololabeltxtfile, namewithoutext, tumor_level, img_width, img_height):  
   
    image_frame_height_factor = 1.0
    image_frame_width_factor = 1.0
    frame_top = 0
    frame_left = 0
    ac_list_R=[]
    ac_list_L=[]
    with open(yololabeltxtfile) as f:
        txtlines = f.readlines()
    #draw a frame
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '0':# in the case of frame
            # set a processed area roi(left(x1), top(y1), right(x2), bottom(y2))
            left = int((float(target_info[1]) - float(target_info[3]) / 2)*img_width)
            top = int((float(target_info[2]) - float(target_info[4]) / 2)*img_height)
            right =int((float(target_info[1]) + float(target_info[3]) / 2)*img_width)
            bottom = int((float(target_info[2]) + float(target_info[4]) / 2)*img_height)
            width = right - left
            height = bottom - top
            image_frame_height_factor = img_height/height
            image_frame_width_factor = img_width/width
            frame_top = top
            frame_left = left
            # cv2.rectangle(img, (0, 0), (416, 416), (0, 0, 0), 5)
            #draw 0db level
            level0db = int((float(height)*0.1538)*image_frame_height_factor)
            # cv2.line(img, (0, level0db), (416, level0db), (0, 0, 0), 5)
    
    #right red air conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '2':# in the case of right air conduction
            # set a processed area roi(left(x1), top(y1), right(x2), bottom(y2))
            point_left = int((float(target_info[1]) - float(target_info[3]) / 2)*img_width)
            left = int((point_left-frame_left)*image_frame_width_factor)
            point_top = int((float(target_info[2]) - float(target_info[4]) / 2)*img_height)
            top = int((point_top-frame_top)*image_frame_height_factor)
            point_right =int((float(target_info[1]) + float(target_info[3]) / 2)*img_width)
            right = int((point_right-frame_left)*image_frame_width_factor)
            point_bottom = int((float(target_info[2]) + float(target_info[4]) / 2)*img_height)
            bottom = int((point_bottom-frame_top)*image_frame_height_factor)
            width = right - left
            height = bottom - top
            center = (int(float(left) +float(width)/2), int(float(top) +float(height)/2))
            radius = int(float(height)/2)
            # cv2.circle(img, center, radius, (0, 0, 255), 5)
            ac_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            ac_list_R.append(ac_dic)
    #overlapped air conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '6':# in the case of overlapping left and right air conductions
            # set a processed area roi(left(x1), top(y1), right(x2), bottom(y2))
            point_left = int((float(target_info[1]) - float(target_info[3]) / 2)*img_width)
            left = int((point_left-frame_left)*image_frame_width_factor)
            point_top = int((float(target_info[2]) - float(target_info[4]) / 2)*img_height)
            top = int((point_top-frame_top)*image_frame_height_factor)
            point_right =int((float(target_info[1]) + float(target_info[3]) / 2)*img_width)
            right = int((point_right-frame_left)*image_frame_width_factor)
            point_bottom = int((float(target_info[2]) + float(target_info[4]) / 2)*img_height)
            bottom = int((point_bottom-frame_top)*image_frame_height_factor)
            width = right - left
            height = bottom - top
            center = (int(float(left) +float(width)/2), int(float(top) +float(height)/2))
            radius = int(float(height)/2)
            # cv2.circle(img, center, radius, (0, 0, 255), 5)
            ac_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            ac_list_R.append(ac_dic)
    #draw lines
    ac_sorted_R = sorted(ac_list_R, key=lambda x: x['center_x'])
    
     #left blue air conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '4':# in the case of left air conduction
            # set a processed area roi(left(x1), top(y1), right(x2), bottom(y2))
            point_left = int((float(target_info[1]) - float(target_info[3]) / 2)*img_width)
            left = int((point_left-frame_left)*image_frame_width_factor)
            point_top = int((float(target_info[2]) - float(target_info[4]) / 2)*img_height)
            top = int((point_top-frame_top)*image_frame_height_factor)
            point_right =int((float(target_info[1]) + float(target_info[3]) / 2)*img_width)
            right = int((point_right-frame_left)*image_frame_width_factor)
            point_bottom = int((float(target_info[2]) + float(target_info[4]) / 2)*img_height)
            bottom = int((point_bottom-frame_top)*image_frame_height_factor)
            width = right - left
            height = bottom - top
            center = (int(float(left) +float(width)/2), int(float(top) +float(height)/2))
            radius = int(float(height)/2)
            # cv2.circle(img, center, radius, (255, 0, 0), 5)
            ac_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            ac_list_L.append(ac_dic)

    #overlapped air conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '6':# in the case of overlapping left and right air conductions
            # set a processed area roi(left(x1), top(y1), right(x2), bottom(y2))
            point_left = int((float(target_info[1]) - float(target_info[3]) / 2)*img_width)
            left = int((point_left-frame_left)*image_frame_width_factor)
            point_top = int((float(target_info[2]) - float(target_info[4]) / 2)*img_height)
            top = int((point_top-frame_top)*image_frame_height_factor)
            point_right =int((float(target_info[1]) + float(target_info[3]) / 2)*img_width)
            right = int((point_right-frame_left)*image_frame_width_factor)
            point_bottom = int((float(target_info[2]) + float(target_info[4]) / 2)*img_height)
            bottom = int((point_bottom-frame_top)*image_frame_height_factor)
            width = right - left
            height = bottom - top
            center = (int(float(left) +float(width)/2), int(float(top) +float(height)/2))
            radius = int(float(height)/2)
            # cv2.circle(img, center, radius, (255, 0, 0), 5)
            ac_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            ac_list_L.append(ac_dic)
    #draw lines
    ac_sorted_L = sorted(ac_list_L, key=lambda x: x['center_x'])
   
    ac_416points_R = give416points(ac_sorted_R)
    ac_416points_L = give416points(ac_sorted_L)
    
    values = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,tumor_level]]
    df_template = pd.DataFrame(values,columns=["d0", "d1", "d2", "d3", "d4","d5", "d6", "d7","label"], index=[namewithoutext+'_R'])
    for i in range(8):
        if i==0:
            if ac_416points_R[35] != 0 and ac_416points_L[35] != 0:
                df_template['d0'] = abs(ac_416points_R[35] - ac_416points_L[35])
            elif ac_416points_R[60] != 0 and ac_416points_L[60] != 0:
                df_template['d0'] = abs(ac_416points_R[60] - ac_416points_L[60])
            else:
                df_template['d0'] = 0.0
        elif i==1:
            if ac_416points_R[90] != 0 and ac_416points_L[90] != 0:
                df_template['d1'] = abs(ac_416points_R[90] - ac_416points_L[90])
            else:
                df_template['d1'] = 0.0
        elif i==2:
            if ac_416points_R[146] != 0 and ac_416points_L[146] != 0:
                df_template['d2'] = abs(ac_416points_R[146] - ac_416points_L[146])
            else:
                df_template['d2'] = 0.0
        elif i==3:
            if ac_416points_R[207] != 0 and ac_416points_L[207] != 0:
                df_template['d3'] = abs(ac_416points_R[207] - ac_416points_L[207])
            else:
                df_template['d3'] = 0.0
        elif i==4:
            if ac_416points_R[267] != 0 and ac_416points_L[267] != 0:
                df_template['d4'] = abs(ac_416points_R[267] - ac_416points_L[267])
            else:
                df_template['d4'] = 0.0
        elif i==5:
            if ac_416points_R[303] != 0 and ac_416points_L[303] != 0:
                df_template['d5'] = abs(ac_416points_R[303] - ac_416points_L[303])
            else:
                df_template['d5'] = 0.0
        elif i==6:
            if ac_416points_R[328] != 0 and ac_416points_L[328] != 0:
                df_template['d6'] = abs(ac_416points_R[328] - ac_416points_L[328])
            else:
                df_template['d6'] = 0.0
        else:
            if ac_416points_R[378] != 0 and ac_416points_L[378] != 0:
                df_template['d7'] = abs(ac_416points_R[378] - ac_416points_L[378])
            elif ac_416points_R[350] != 0 and ac_416points_L[350] != 0:
                df_template['d7'] = abs(ac_416points_R[350] - ac_416points_L[350])
            else:
                df_template['d7'] = 0.0

    return df_template

def prepare_RL_df_differential(YOLOIMG_FILE_DIR):
    values = np.zeros((1, 9))
    df_all = pd.DataFrame(values,columns=["d0", "d1", "d2", "d3", "d4","d5", "d6", "d7","label"], index=['initial_cont'])

    files_DIR = YOLOIMG_FILE_DIR + '/' + '*' 
    files = glob.glob(files_DIR)
    #To skip .txt files
    for file in files:
        if file.endswith('jpg'):
            dirname = os.path.dirname(file)
            namewithoutext = os.path.splitext(os.path.basename(file))[0]
            image_ext = os.path.splitext(os.path.basename(file))[1]
            yololabeltxtfile_PATH = dirname + '/labels/' + namewithoutext + '.txt' 
            tumorR = int(namewithoutext.split('_')[1])
            tumorL = int(namewithoutext.split('_')[2])              

            yoloimg = cv2.imread(file)
            yoloimg_height, yoloimg_width = yoloimg.shape[:2]

            #df creation
            if tumorR==1 or tumorL==1:
                RL_diff_tumorLR1 = RLacdata_differential_df(yololabeltxtfile_PATH, namewithoutext, 1, yoloimg_width, yoloimg_height)
                df_all = pd.concat([df_all, RL_diff_tumorLR1])
            else:
                RL_diff_tumorLR0 = RLacdata_differential_df(yololabeltxtfile_PATH, namewithoutext, 0, yoloimg_width, yoloimg_height)
                df_all = pd.concat([df_all, RL_diff_tumorLR0])

    return df_all
