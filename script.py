import os
import cv2
dir = "D:\mugshot_frontal_cropped_all"
entries = os.listdir(dir)
for file_name in entries:
    path_filename = dir + '\\' + file_name
    img = cv2.imread(path_filename)
    new_dir = "D:\\dataset\\"+file_name[0:3]
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    cv2.imwrite(new_dir+"/foto.png",img)        