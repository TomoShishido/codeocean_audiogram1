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

def Lacdata_point_df(yololabeltxtfile, namewithoutext, tumor_level, img_width, img_height):  
   
    image_frame_height_factor = 1.0
    image_frame_width_factor = 1.0
    frame_top = 0
    frame_left = 0
    ac_list_R=[]
    ac_list_L=[]
    bc_list = []


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
        if target_info[0] == '2':# in the case of frame
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
        if target_info[0] == '6':# in the case of frame
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
        if target_info[0] == '4':# in the case of frame
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
        if target_info[0] == '6':# in the case of frame
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
   
    # ac_416points_R = give416points(ac_sorted_R)
    #_Lを_Rとして処理する
    ac_416points_R = give416points(ac_sorted_L)
    
    values = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,tumor_level]]
    df_template = pd.DataFrame(values,columns=["lp0", "lp1", "lp2", "lp3", "lp4","lp5", "lp6","lp7","lbcp1","lbcp2","lbcp3","lbcp4","lbcp5","lbcp6","label"], index=[namewithoutext])
    for i in range(8):
        if i==0:
            if ac_416points_R[35] != 0:
                df_template['lp0'] = ac_416points_R[35]
            elif ac_416points_R[60] != 0:
                df_template['lp0'] = ac_416points_R[60]
            else:
                df_template['lp0'] = 0.0
        elif i==1:
            if ac_416points_R[90] != 0:
                df_template['lp1'] = ac_416points_R[90]
            else:
                df_template['lp1'] = 0.0
        elif i==2:
            if ac_416points_R[146] != 0:
                df_template['lp2'] = ac_416points_R[146]
            else:
                df_template['lp2'] = 0.0
        elif i==3:
            if ac_416points_R[207] != 0:
                df_template['lp3'] = ac_416points_R[207]
            else:
                df_template['lp3'] = 0.0
        elif i==4:
            if ac_416points_R[267] != 0:
                df_template['lp4'] = ac_416points_R[267]
            else:
                df_template['lp4'] = 0.0
        elif i==5:
            if ac_416points_R[303] != 0:
                df_template['lp5'] = ac_416points_R[303]
            else:
                df_template['lp5'] = 0.0
        elif i==6:
            if ac_416points_R[328] != 0:
                df_template['lp6'] = ac_416points_R[328]
            else:
                df_template['lp6'] = 0.0
        else:
            if ac_416points_R[378] != 0:
                df_template['lp7'] = ac_416points_R[378]
            elif ac_416points_R[350] != 0:
                df_template['lp7'] = ac_416points_R[350]
            else:
                df_template['lp7'] = 0.0

    #left blue bone conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '5':# in the case of left bone conduction
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
            # cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 5)
            bc_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            bc_list.append(bc_dic)
    bc_sorted = sorted(bc_list, key=lambda x: x['center_x'])
    bc_416points = give416points(bc_sorted)

    for i in range(6):

        if i==0:
            if bc_416points[110] != 0:
                df_template['lbcp1'] = bc_416points[110]
            elif bc_416points[120] != 0:
                df_template['lbcp1'] = bc_416points[120]
            else:
                df_template['lbcp1'] = 0.0
        elif i==1:
            if bc_416points[166] != 0:
                df_template['lbcp2'] = bc_416points[166]
            else:
                df_template['lbcp2'] = 0.0
        elif i==2:
            if bc_416points[227] != 0:
                df_template['lbcp3'] = bc_416points[227]
            else:
                df_template['lbcp3'] = 0.0
        elif i==3:
            if bc_416points[287] != 0:
                df_template['lbcp4'] = bc_416points[287]
            else:
                df_template['lbcp4'] = 0.0
        elif i==4:
            if bc_416points[323] != 0:
                df_template['lbcp5'] = bc_416points[323]
            else:
                df_template['lbcp5'] = 0.0
        elif i==5:
            if bc_416points[338] != 0:
                df_template['lbcp6'] = bc_416points[338]
            elif bc_416points[328] != 0:
                df_template['lbcp6'] = bc_416points[328]
            else:
                df_template['lbcp6'] = 0.0
        else:
            pass

    return df_template

def Racdata_point_df(yololabeltxtfile, namewithoutext, tumor_level, img_width, img_height):  
   
    image_frame_height_factor = 1.0
    image_frame_width_factor = 1.0
    frame_top = 0
    frame_left = 0
    ac_list_R=[]
    ac_list_L=[]
    bc_list=[]

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
        if target_info[0] == '2':# in the case of frame
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
        if target_info[0] == '6':# in the case of frame
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
       
    ac_416points_R = give416points(ac_sorted_R)
    
    
    values = [[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]]
    df_template = pd.DataFrame(values,columns=["rp0", "rp1", "rp2", "rp3", "rp4","rp5", "rp6","rp7","rbcp1","rbcp2","rbcp3","rbcp4","rbcp5","rbcp6"], index=[namewithoutext])
    for i in range(8):
        if i==0:
            if ac_416points_R[35] != 0:
                df_template['rp0'] = ac_416points_R[35]
            elif ac_416points_R[60] != 0:
                df_template['rp0'] = ac_416points_R[60]
            else:
                df_template['rp0'] = 0.0
        elif i==1:
            if ac_416points_R[90] != 0:
                df_template['rp1'] = ac_416points_R[90]
            else:
                df_template['rp1'] = 0.0
        elif i==2:
            if ac_416points_R[146] != 0:
                df_template['rp2'] = ac_416points_R[146]
            else:
                df_template['rp2'] = 0.0
        elif i==3:
            if ac_416points_R[207] != 0:
                df_template['rp3'] = ac_416points_R[207]
            else:
                df_template['rp3'] = 0.0
        elif i==4:
            if ac_416points_R[267] != 0:
                df_template['rp4'] = ac_416points_R[267]
            else:
                df_template['rp4'] = 0.0
        elif i==5:
            if ac_416points_R[303] != 0:
                df_template['rp5'] = ac_416points_R[303]
            else:
                df_template['rp5'] = 0.0
        elif i==6:
            if ac_416points_R[328] != 0:
                df_template['rp6'] = ac_416points_R[328]
            else:
                df_template['rp6'] = 0.0
        else:
            if ac_416points_R[378] != 0:
                df_template['rp7'] = ac_416points_R[378]
            elif ac_416points_R[350] != 0:
                df_template['rp7'] = ac_416points_R[350]
            else:
                df_template['rp7'] = 0.0

    #left blue bone conduction
    for textline in txtlines:
        target_info = textline.split() #target_info =[label, x, y, w, h]
        if target_info[0] == '3':# in the case of right bone conduction
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
            # cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 5)
            bc_dic={'center_x':int(float(left) +float(width)/2), 'center_y':int(float(top) +float(height)/2)}
            bc_list.append(bc_dic)
    bc_sorted = sorted(bc_list, key=lambda x: x['center_x'])
    bc_416points = give416points(bc_sorted)

    for i in range(6):

        if i==0:
            if bc_416points[70] != 0:
                df_template['rbcp1'] = bc_416points[70]
            elif bc_416points[80] != 0:
                df_template['rbcp1'] = bc_416points[80]
            else:
                df_template['rbcp1'] = 0.0
        elif i==1:
            if bc_416points[126] != 0:
                df_template['rbcp2'] = bc_416points[126]
            else:
                df_template['rbcp2'] = 0.0
        elif i==2:
            if bc_416points[187] != 0:
                df_template['rbcp3'] = bc_416points[187]
            else:
                df_template['rbcp3'] = 0.0
        elif i==3:
            if bc_416points[247] != 0:
                df_template['rbcp4'] = bc_416points[247]
            else:
                df_template['rbcp4'] = 0.0
        elif i==4:
            if bc_416points[283] != 0:
                df_template['rbcp5'] = bc_416points[283]
            else:
                df_template['rbcp5'] = 0.0
        elif i==5:
            if bc_416points[298] != 0:
                df_template['rbcp6'] = bc_416points[298]
            elif bc_416points[288] != 0:
                df_template['rbcp6'] = bc_416points[288]
            else:
                df_template['rbcp6'] = 0.0
        else:
            pass

    return df_template

def prepare_RL_acbc_df_point(YOLOIMG_FILE_DIR):
    values = np.zeros((1, 29))
    df_all = pd.DataFrame(values,columns=["rp0", "rp1", "rp2", "rp3", "rp4","rp5", "rp6", "rp7","rbcp1","rbcp2","rbcp3","rbcp4","rbcp5","rbcp6","lp0", "lp1", "lp2", "lp3", "lp4","lp5", "lp6", "lp7","lbcp1","lbcp2","lbcp3","lbcp4","lbcp5","lbcp6","label"], index=['initial_cont'])

    files_DIR = YOLOIMG_FILE_DIR + '/' + '*' 
    files = glob.glob(files_DIR)
    #To skip .txt files
    for file in files:
        if file.endswith('jpg'):
            dirname = os.path.dirname(file)
            namewithoutext = os.path.splitext(os.path.basename(file))[0]
            image_ext = os.path.splitext(os.path.basename(file))[1]
            yololabeltxtfile_PATH = dirname + '/labels/' + namewithoutext + '.txt' 
            tumor = int(namewithoutext.split('_')[0])
            # tumorL = int(namewithoutext.split('_')[2])              

            yoloimg = cv2.imread(file)
            yoloimg_height, yoloimg_width = yoloimg.shape[:2]

            #df creation

            R_diff = Racdata_point_df(yololabeltxtfile_PATH, namewithoutext, tumor, yoloimg_width, yoloimg_height)
            L_diff = Lacdata_point_df(yololabeltxtfile_PATH, namewithoutext, tumor, yoloimg_width, yoloimg_height)
            RL_diff =pd.concat([R_diff, L_diff], axis =1)
            df_all = pd.concat([df_all, RL_diff])


    return df_all