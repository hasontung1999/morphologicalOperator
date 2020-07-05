import numpy as np
import copy

def erode_gray(img,kernel):
    center = (kernel.shape[0]//2,kernel.shape[1]//2)#lấy tâm kernel
    res = np.zeros((img.shape[0],img.shape[1]),np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            minindex_x = max((0,i - center[0]))#trích ra vùng lân cận để lấy min
            maxindex_x = min((i+center[0]+1),img.shape[0])
            minindex_y = max((0,j - center[1]))
            maxindex_y = min((j+center[1]+1),img.shape[1])
            windows = copy.deepcopy(img[minindex_x:maxindex_x,minindex_y:maxindex_y]) - kernel[0:(maxindex_x-minindex_x),0:(maxindex_y-minindex_y)]#công thức
            res[i][j]= np.amin(windows)#lấy min
    return res

'''
dilate ảnh xám
input: ảnh xám, kernel
output: ảnh đã dilate
'''
def dilate_gray(img,kernel):
    kernel_center = (kernel.shape[0] // 2, kernel.shape[1] // 2)
    kernel_flip = np.zeros((kernel.shape[0], kernel.shape[1]))#đối xứng qua tâm như định nghĩa trong sách
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            kernel_flip[i, j] = kernel[2 * kernel_center[0] - i, 2 * kernel_center[1] - j]
    center = (kernel.shape[0]//2,kernel.shape[1]//2)
    res = np.zeros((img.shape[0],img.shape[1]),np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):#lấy các tọa độ lân cận để lấy max
            minindex_x = max((0,i - center[0]))
            maxindex_x = min((i+center[0]+1),img.shape[0])
            minindex_y = max((0,j - center[1]))
            maxindex_y = min((j+center[1]+1),img.shape[1])
            windows = copy.deepcopy(img[minindex_x:maxindex_x,minindex_y:maxindex_y]) + kernel[0:(maxindex_x-minindex_x),0:(maxindex_y-minindex_y)]
            res[i][j]= np.amax(windows)
    return res

'''
open ảnh xám
input: ảnh xám, kernel
output: ảnh đã open
'''
def open_gray(img,kernel):
    return dilate_gray(erode_gray(img,kernel),kernel)#erode rồi dilate

'''
close ảnh xám
input: ảnh xám, kernel
output: ảnh đã close
'''
def close_gray(img,kernel):
    return erode_gray(dilate_gray(img,kernel),kernel)#dilate rồi erode

'''
gradient ảnh xám
input: ảnh xám, kernel
output: ảnh gradient
'''
def Morphological_Gradient(img,kernel):
    return dilate_gray(img,kernel) - erode_gray(img,kernel)#dilate - erode

'''
tophat
input: ảnh xám
out put: ảnh top hat
'''
def top_hat_gray(img,kernel):
    f = open_gray(img,kernel)
    t = copy.deepcopy(img)
    t.astype('float32')# chỉnh qua dạng float để đề phòng trường hợp xoay vòng 0 255 của uint 8
    f.astype('float32')
    res = t-f#ảnh gốc trừ ảnh open
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            if res[i][j] < 0 : res[i][j] = 0#kiểm tra pixel nhỏ hơn 0 và lớn hơn 255.
            elif res[i][j]>255: res[i][j] = 255
            else: res[i][j]=np.round(res[i][j])
    res.astype('uint8')#đưa lại về uint8
    return res

'''
black hat
input: ảnh xám
out put: ảnh black hat
tương tự top hat khác chỗ lấy ảnh close trừ ảnh gốc
'''
def black_hat_gray(img,kernel):
    f = close_gray(img,kernel)
    t = copy.deepcopy(img)
    t.astype('float32')
    f.astype('float32')
    res = f-t
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            if res[i][j] < 0 : res[i][j] = 0
            elif res[i][j]>255: res[i][j] = 255
            else: res[i][j]=np.round(res[i][j])
    res.astype('uint8')
    return res


'''gray reconstruction (dùng công thức tạo tạo marker = cách liên tục dilate rồi and với ảnh gốc)
input: marker,mask,kernel
output: ảnh đã tái tạo
'''
def gray_reconstruction(marker,mask,kernel):
    prev = marker
    while True:#làm các tác vụ như mô tả bên dưới tới khi hội tụ.
        marker = dilate_gray(marker,kernel)#dilate ảnh
        marker = np.minimum(marker,mask)#minimum pixel wise thay cho phép và ảnh
        #t = np.equal(marker,prev)
        if(np.all(np.equal(marker,prev)==True)):return marker
        else: prev = marker