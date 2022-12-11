from scipy import sparse
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt
import graphCreation
import graphCutSparse
import cv2
import paint

# k = 10
# img = np.array([[[0,0,0],[30,30,30],[170,170,170]],
# [[50,50,50],[255,255,255],[200,200,200]],
# [[20,20,20],[200,200,200],[140,140,140]]])

def segment(path):
    img = cv2.imread(path)
    print(img.shape)
    img_ = img
    # img_ = cv2.pyrDown(img)
    # Select ROI, Crop image
    r = cv2.selectROI(img_)
    imgCrop = img_[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    # print(imgCrop.shape)
    # imgCrop = img[340:380, 530:580]
    imgCrop_ = imgCrop.copy()

    print('---adding scribbles---')
    painter = paint.Painter(imgCrop, 2)
    painter.paint_mask()

    print('---creating sparse matrix---')
    h,w = imgCrop.shape[:-1]
    # print(h, w)
    graph = graphCreation.img2graph(imgCrop_, imgCrop)
    # print(graph[0])
    print('---graph cutting---')
    g = graphCutSparse.Graph(graph)
    g.minCut_Fold_Fulkerson(0,h*w+1)
    # print(g.graph)
    # print(len(g.graph.data[0]))
    print('---creating mask---')
    maskCrop = g.get_mask()[1:-1]
    maskCrop = np.array(maskCrop).reshape(h,w)
    mask = np.zeros_like(img_[:,:,0])
    mask[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] = -maskCrop
    return mask

# path = '/Users/zhaosonglin/Desktop/chair.png'
# mask = segment(path)
# plt.imshow(mask, 'gray')
# plt.show()
