# import numpy as np
# import cv2 as cv
#
# test=[[2,3,4,5,6,7,8,9],[3,4,5,6,7,8,9,10,11]]
# i=0
# i_=1
# j=1
# j_=3
# arr=test[i:i_,j:j_]
# print(arr)
#
# #Chuyển ảnh xám thành ảnh nhị phân
# img_gray = cv.imread('input.jpg', 0)
# #cv.imshow('input image',img_gray)
# (thresh, img) = cv.threshold(img_gray, 128, 255,cv.THRESH_BINARY | cv.THRESH_OTSU)
# thresh = 127
# im_bw = cv.threshold(img_gray, thresh, 255, cv.THRESH_BINARY)
# cv.imshow('Binary image', img)
#
# # #Toán tử dãn nở nhị phân
# kernel = np.ones((3,3),np.uint8)
# # img_dilation = cv.dilate(img, kernel, iterations=1)
# # #cv.imshow('Dilation image',img_dilation)
# # #Toán tử co nhị phân
# # img_erosion = cv.erode(img, kernel)
# # #cv.imshow('Erosion',img_erosion)
# # #Toán tử mở nhị phân
# # img_opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
# # #cv.imshow('Opening',img_opening)
# # #Toán tử đóng nhị phân
# # img_closing=cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
# # #cv.imshow('Closing',img_closing)
# # #Toán tử Hit-or-miss
# # img_hit_or_miss=cv.morphologyEx(img, cv.MORPH_HITMISS, kernel)
# # #cv.imshow('Hit miss',img_hit_or_miss)
# # #Thinning
# # img_thinning = cv.ximgproc.thinning(img)
# # #cv.imshow('Thinning',img_thinning)
#
# #Ảnh xám
# # img_gradient = cv.morphologyEx(img, cv.MORPH_GRADIENT,kernel)
# # # cv.imshow('Gradient',img_gradient)
# # img_tophat = cv.morphologyEx(img, cv.MORPH_TOPHAT, kernel)
# # #cv.imshow('TOPHAT',img_tophat)
# # img_blackhat = cv.morphologyEx(img, cv.MORPH_BLACKHAT,kernel)
# # cv.imshow('BlackHat',img_blackhat)
#
# cv.waitKey(0)
# #input()

import cv2
import numpy as np
import binary

wait_key_time = 0

'''
hard code test
'''
img_test = np.zeros((5, 4), np.uint8)
img_test[0, 1] = 1
img_test[1, 0] = 1
img_test[1, 1] = 1
img_test[1, 2] = 1
img_test[2, 1] = 1
img_test[3, 1] = 1
img_test[4, 1] = 1


cv2.imshow('hard code test', img_test)

kernel_1 = np.zeros((1, 2), np.uint8)
kernel_1[0, 1] = 1
test_erode = cv2.erode(img_test, kernel_1, iterations=1)
test_dilate = cv2.dilate(img_test, kernel_1, iterations=1)
# cv2.imwrite('D:\\hard_code_test_original.png', img_test)
# cv2.waitKey(wait_key_time)

kernel_2 = np.ones((1, 2), np.uint8)
test_erode_2 = cv2.erode(img_test, kernel_2, iterations=1)
test_dilate_2 = cv2.dilate(img_test, kernel_2, iterations=1)

kernel_3 = np.zeros((2, 1), np.uint8)
kernel_3[1, 0] = 1
test_erode_3 = cv2.erode(img_test, kernel_3, iterations=1)
test_dilate_3 = cv2.dilate(img_test, kernel_3, iterations=1)

kernel_4 = np.ones((2, 1), np.uint8)
test_erode_4 = cv2.erode(img_test, kernel_4, iterations=1)
test_dilate_4 = cv2.dilate(img_test, kernel_4, iterations=1)

cv2.waitKey(wait_key_time)

