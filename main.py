import sys
import getopt
import cv2
import numpy as np
import binary

def operator(in_file, out_file, mor_op, wait_key_time=0):
    img_origin = cv2.imread(in_file)
    cv2.imshow('original image', img_origin)

    img_gray = cv2.imread(in_file, 0)
    cv2.imshow('Gray image', img_gray)

    (thresh, img) = cv2.threshold(img_gray, 128, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('Binary image', binary.normBin2Bin(img))

    kernel = np.ones((5, 5), np.uint8)
    img_out = None

    '''
    TODO: implement morphological operators
    '''
    if mor_op == 'dilate':
        img_dilation = cv2.dilate(img, kernel)
        cv2.imshow('OpenCV dilation image', binary.normBin2Bin(img_dilation))

        img_dilation_manual = binary.dilate(img, kernel)
        img_dilation_manual=binary.normBin2Bin(img_dilation_manual)
        cv2.imshow('Manual dilation image', img_dilation_manual)

        img_out = img_dilation_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'erode':
        img_erosion = cv2.erode(img, kernel)
        cv2.imshow('OpenCV erosion image', binary.normBin2Bin(img_erosion))

        img_erosion_manual = binary.erode(img, kernel)
        img_erosion_manual=binary.normBin2Bin(img_erosion_manual)
        cv2.imshow('Manual erosion image', img_erosion_manual)

        img_out = img_erosion_manual
        cv2.waitKey(wait_key_time)
    elif mor_op=='opening':
        img_opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
        cv2.imshow('OpenCV opening image', binary.normBin2Bin(img_opening))

        img_opening_manual = binary.opening(img, kernel)
        img_opening_manual=binary.normBin2Bin(img_opening_manual)
        cv2.imshow('Manual opening image', img_opening_manual)

        img_out = img_opening_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'closing':
        img_closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        cv2.imshow('OpenCV closing image', binary.normBin2Bin(img_closing))

        img_closing_manual = binary.closing(img, kernel)
        img_closing_manual=binary.normBin2Bin(img_closing_manual)
        cv2.imshow('Manual closing image', img_closing_manual)

        img_out = img_closing_manual
        cv2.waitKey(wait_key_time)
    elif mor_op=='hitmiss':
        img_hit_or_miss = cv2.morphologyEx(img, cv2.MORPH_HITMISS,kernel)
        cv2.imshow('OpenCV hit-or-miss image',binary.normBin2Bin(img_hit_or_miss))

        img_hitmiss_manual=binary.hit_or_miss(img,kernel)
        img_hitmiss_manual=binary.normBin2Bin(img_hitmiss_manual)
        cv2.imshow('Manual hit-or-miss image',img_hitmiss_manual)

        img_out=img_hitmiss_manual
        cv2.waitKey(wait_key_time)

    elif mor_op == 'boundary':
        img_boundary = cv2.subtract(img,cv2.erode(img,kernel))
        cv2.imshow('OpenCV boundary extraction image', binary.normBin2Bin(img_boundary))

        img_boundary_manual = binary.boundary_extraction(img, kernel)
        img_boundary_manual = binary.normBin2Bin(img_boundary_manual)
        cv2.imshow('Manual boundary extraction image', img_boundary_manual)

        img_out = img_boundary_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'holefill':
        point=[60,43]
        img_holefill_manual = binary.hole_filling(img, kernel,point)
        img_holefill_manual = binary.normBin2Bin(img_holefill_manual)
        cv2.imshow('Manual hole filling image', img_holefill_manual)

        img_out = img_holefill_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'connectedComp':
        point=[60,43]
        img_connect_manual = binary.connected_component(img, kernel,point)
        img_connect_manual = binary.normBin2Bin(img_connect_manual)
        cv2.imshow('Manual extraction connected component image', img_connect_manual)

        img_out = img_connect_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'convexhull':
        imgC=binary.complement(img)
        cv2.imshow('Complement of image',binary.normBin2Bin(imgC))

        img_convexhull_manual = binary.convex_hull(imgC, kernel)
        img_convexhull_manual = binary.normBin2Bin(img_convexhull_manual)
        cv2.imshow('Manual convex hull image', img_convexhull_manual)

        img_out = img_convexhull_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'thinning':
        img_thinning_manual = binary.thinning(img, kernel)
        img_thinning_manual = binary.normBin2Bin(img_thinning_manual)
        cv2.imshow('Manual thinning image', img_thinning_manual)

        img_out = img_thinning_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'thickening':
        img_thickening_manual = binary.thickening(img, kernel)
        img_thickening_manual = binary.normBin2Bin(img_thickening_manual)
        cv2.imshow('Manual thickening image', img_thickening_manual)

        img_out = img_thickening_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'skeleton':
        img_skeleton_manual = binary.skeleton(img, kernel)
        img_skeleton_manual = binary.normBin2Bin(img_skeleton_manual)
        cv2.imshow('Manual skeleton image', img_skeleton_manual)

        img_out = img_skeleton_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'reconstruction':
        img_reconstruction_manual = binary.reconstruction(img, kernel)
        img_reconstruction_manual = binary.normBin2Bin(img_reconstruction_manual)
        cv2.imshow('Manual reconstruction image', img_reconstruction_manual)

        img_out = img_reconstruction_manual
        cv2.waitKey(wait_key_time)
    elif mor_op == 'pruning':
        img_pruning_manual = binary.pruning(img, kernel)
        img_pruning_manual = binary.normBin2Bin(img_pruning_manual)
        cv2.imshow('Manual pruning image', img_pruning_manual)

        img_out = img_pruning_manual
        cv2.waitKey(wait_key_time)
    if img_out is not None:
        cv2.imwrite(out_file, img_out)


def main(argv):
    input_file = ''
    output_file = ''
    mor_op = ''
    wait_key_time = 0

    description = 'main.py -i <input_file> -o <output_file> -p <mor_operator> -t <wait_key_time>'

    try:
        opts, args = getopt.getopt(argv, "hi:o:p:t:", ["in_file=", "out_file=", "mor_operator=", "wait_key_time="])
    except getopt.GetoptError:
        print(description)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(description)
            sys.exit()
        elif opt in ("-i", "--in_file"):
            input_file = arg
        elif opt in ("-o", "--out_file"):
            output_file = arg
        elif opt in ("-p", "--mor_operator"):
            mor_op = arg
        elif opt in ("-t", "--wait_key_time"):
            wait_key_time = int(arg)

    print('Input file is ', input_file)
    print('Output file is ', output_file)
    print('Morphological operator is ', mor_op)
    print('Wait key time is ', wait_key_time)

    operator(input_file, output_file, mor_op, wait_key_time)
    cv2.waitKey(wait_key_time)


if __name__ == "__main__":
    main(sys.argv[1:])
