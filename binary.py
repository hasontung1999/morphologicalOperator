import numpy as np

def normBin2Bin(srcImg):
     dstImg=255*srcImg
     dstImg=dstImg.astype(np.uint8)
     return dstImg

def complement(img):
    if img is None:
        return None
    complement=np.zeros((img.shape[0],img.shape[1]))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j]==0:
                complement[i,j]=1
    return complement

def subtraction(window,kernel):
    if window is None:
        return None
    if kernel is None:
        return window
    subtractImg=window
    windowCenter=(window.shape[0]//2,window.shape[1]//2)
    kernelCenter=(kernel.shape[0]//2,kernel.shape[1]//2)
    for kerX in range(kernel.shape[0]):
        for kerY in range(kernel.shape[1]):
            if kernel[kerX,kerY]==1:
                windowX=windowCenter[0]+kerX-kernelCenter[0]
                windowY=windowCenter[1]+kerY-kernelCenter[1]
                if windowX>=0 and windowX<window.shape[0] and windowY>=0 and windowY<window.shape[1]:
                    if window[windowX,windowY]==1:
                        subtractImg[windowX,windowY]=0
    return subtractImg

def intersection(imgA,imgB):
    if imgA is None and imgB is None:
        return None
    if imgA is None:
        return imgB
    if imgB is None:
        return imgA
    intersectImg=np.zeros((imgA.shape[0],imgA.shape[1]))
    imgACenter=(imgA.shape[0]//2,imgA.shape[1]//2)
    imgBCenter=(imgB.shape[0]//2,imgB.shape[1]//2)
    for imgBX in range(imgB.shape[0]):
        for imgBY in range(imgB.shape[1]):
            if imgB[imgBX,imgBY]==1:
                imgAX = imgACenter[0] + imgBX - imgBCenter[0]
                imgAY = imgACenter[1] + imgBY - imgBCenter[1]
                if imgAX >= 0 and imgAX < imgA.shape[0] and imgAY >= 0 and imgAY < imgA.shape[1]:
                    if imgA[imgAX,imgAY]==1:
                        intersectImg[imgAX,imgAY]=1
    return intersectImg
def union(imgA,imgB):
    if imgA is None and imgB is None:
        return None
    if imgA is None:
        return imgB
    if imgB is None:
        return imgA
    unionImg=imgA
    for imgBX in range(imgB.shape[0]):
        for imgBY in range(imgB.shape[1]):
            if imgB[imgBX,imgBY]==1:
                unionImg[imgBX,imgBY]=1
    return unionImg

def erode(img, kernel):
    if kernel is None:
        return None
    kernel_center = (kernel.shape[0] // 2, kernel.shape[1] // 2)
    kernel_ones_count = kernel.sum()
    eroded_img = np.zeros((img.shape[0] + kernel.shape[0] - 1, img.shape[1] + kernel.shape[1] - 1))
    img_shape = img.shape

    x_append = np.zeros((img.shape[0], kernel.shape[1] - 1))
    img = np.append(img, x_append, axis=1)

    y_append = np.zeros((kernel.shape[0] - 1, img.shape[1]))
    img = np.append(img, y_append, axis=0)

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            i_ = i + kernel.shape[0]
            j_ = j + kernel.shape[1]
            if kernel_ones_count == (kernel * img[i:i_, j:j_]).sum():
                eroded_img[i + kernel_center[0], j + kernel_center[1]] = 1
    return eroded_img[:img_shape[0], :img_shape[1]]

def dilate(img, kernel):
    if kernel is None:
        return None
    kernelShape=kernel.shape
    imgShape=img.shape
    kernel_center = (kernelShape[0] // 2, kernelShape[1] // 2)
    dilated_img = np.zeros((imgShape[0], imgShape[1]))

    for i in range(imgShape[0]):
        for j in range(imgShape[1]):
            if img[i,j]==1:
                for iKer in range(kernelShape[0]):
                    for jKer in range(kernelShape[1]):
                        if kernel[iKer,jKer]==1:
                            dilateX=i+iKer-kernel_center[0]
                            dilateY=j+jKer-kernel_center[1]
                            if dilateX>=0 and dilateX<imgShape[0] and dilateY>=0 and dilateY<imgShape[1]:
                                dilated_img[dilateX,dilateY]=1
    return dilated_img

def opening(img,kernel):
    if kernel is None:
        return None
    openImg=erode(img,kernel)
    #openImg=normBin2Bin(openImg)
    return dilate(openImg,kernel)

def closing(img,kernel):
    if kernel is None:
        return None
    closeImg=dilate(img,kernel)
    #closeImg=normBin2Bin(closeImg)
    return erode(closeImg,kernel)

def hit_or_miss(img,kernel,window=None):
    if kernel is None:
       return None
    erosionImg=erode(img,kernel)
    imgComplement=complement(img)
    erosionImgComplement=erode(imgComplement,subtraction(window,kernel))
    hitmiss=intersection(erosionImg,erosionImgComplement)
    return hitmiss

def boundary_extraction(img,kernel):
    if kernel is None:
        return None
    erosionImg=erode(img,kernel)
    boundary=subtraction(img,erosionImg)
    return boundary

def hole_filling(img,kernel,pointInBound):
    if kernel is None:
        return None
    X0=np.zeros((img.shape[0],img.shape[1]))
    X0[pointInBound[0],pointInBound[1]]=1
    imgC=complement(img)

    while 1:
        flag = 0
        Xk=intersection(dilate(X0,kernel),imgC)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if Xk[i,j] != X0[i,j]:
                    flag =1
                    break
            if flag==1:
                break
        if flag==0:
            break
        X0=Xk
    return union(img,Xk)

def connected_component(img,kernel,pointInBound):
    if kernel is None:
        return None
    X0 = np.zeros((img.shape[0], img.shape[1]))
    X0[pointInBound[0], pointInBound[1]] = 1

    while 1:
        flag = 0
        Xk = intersection(dilate(X0, kernel), img)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if Xk[i, j] != X0[i, j]:
                    flag = 1
                    break
            if flag == 1:
                break
        if flag == 0:
            break
        X0 = Xk
    return Xk

def convex_hull(img,kernel):
    if kernel is None:
        return None
    temp1=np.zeros((kernel.shape[0],kernel.shape[1]))
    temp2=np.zeros((kernel.shape[0],kernel.shape[1]))
    temp3=np.zeros((kernel.shape[0],kernel.shape[1]))
    temp4=np.zeros((kernel.shape[0],kernel.shape[1]))
    for i in range(kernel.shape[0]):
        temp1[i,0]=1
        temp3[i,kernel.shape[1]-1]=1
    for j in range(kernel.shape[1]):
        temp2[0,j]=1
        temp4[kernel.shape[0]-1,j]=1
    baseKernel=[temp1,temp2,temp3,temp4]
    D=[]
    for nLoop in range(4):
        X0=img
        while 1:
            flag = 0
            Xk = union(hit_or_miss(X0, baseKernel[nLoop]), img)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if Xk[i, j] != X0[i, j]:
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 0:
                break
            X0 = Xk
        D.append(Xk)
    result=np.zeros((img.shape[0],img.shape[1]))
    for i in range(len(D)):
        result=union(result,D[i])
    return result

def thinning(img,kernel):
    if kernel is None:
        return None
    hitmissImg=hit_or_miss(img,kernel)
    thinningImg=subtraction(img,hitmissImg)
    return thinningImg

def thickening(img,kernel):
    if kernel is None:
        return None
    hitmissImg=hit_or_miss(img,kernel)
    thickeningImg=union(img,hitmissImg)
    return thickeningImg

def checkZeros(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i,j]==1:
                return 0
    return 1

def skeleton(img,kernel):
    if kernel is None:
        return None
    tempImg=img
    K=0
    while checkZeros(tempImg)==0:
        K+=1
        tempImg=erode(tempImg,kernel)
    S0=subtraction(img,opening(img,kernel))
    Sx=[S0]
    for i in range(1,K+1):
        erodeImg=img
        for j in range(1,i+1):
            erodeImg=erode(erodeImg,kernel)
        Si=subtraction(erodeImg,opening(erodeImg,kernel))
        Sx.append(Si)
    result=Sx[0]
    for i in range(1,len(Sx)):
        result=union(result,Sx[i])
    return result

def reconstruction(img,kernel):
    if kernel is None:
        return None
    tempImg = img
    K = 0
    while checkZeros(tempImg) == 0:
        K += 1
        tempImg = erode(tempImg, kernel)
    S0 = subtraction(img, opening(img, kernel))
    Sx = [S0]
    for i in range(1, K + 1):
        erodeImg = img
        for j in range(1, i + 1):
            erodeImg = erode(erodeImg, kernel)
        Si = subtraction(erodeImg, opening(erodeImg, kernel))
        Sx.append(Si)
    result=Sx[0]
    for i in range(1,K+1):
        Si=Sx[i]
        for j in range(i):
            Si=dilate(Si,kernel)
        result=union(result,Si)
    return result

def pruning(img,kernel):
    if kernel is None:
        return None
    kernelCenter=(kernel.shape[0]//2,kernel.shape[1]//2)
    B=[]
    for i in range(8):
        Bi=np.zeros((kernel.shape[0],kernel.shape[1]))
        B.append(Bi)
    for i in range(kernelCenter[0]):
        B[0][kernelCenter[0],kernelCenter[1]-i]=1
        B[1][kernelCenter[0]-i,kernelCenter[1]]=1
        B[2][kernelCenter[0],kernelCenter[1]+i]=1
        B[3][kernelCenter[0]+i,kernelCenter[1]]=1
        B[4][kernelCenter[0]-i,kernelCenter[1]-i]=1
        B[5][kernelCenter[0]-i,kernelCenter[1]+i]=1
        B[6][kernelCenter[0]+i,kernelCenter[1]+i]=1
        B[7][kernelCenter[0]+i,kernelCenter[1]-i]=1
    X1=img
    for i in range(len(B)):
        X1=thinning(X1,B[i])
    X2=hit_or_miss(X1,B[0])
    for i in range(1,len(B)):
        X2=union(X2,hit_or_miss(X1,B[i]))
    H=np.ones((kernel.shape[0],kernel.shape[1]))
    X3=intersection(dilate(X2,H),img)
    return union(X1,X3)



