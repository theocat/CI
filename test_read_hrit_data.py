# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 13:40:44 2017

@author: nriet
"""
# a function for get kuihua8 data set

import numpy as np
import matplotlib.pyplot as plt
from u_read_hrit import read_hrit
import os
import struct
path_in='D:/python_project/HRIT/data/'

path_out0='D:/python_project/HRIT/data4CI/'

time_c='201804020820'
# B07
brands=['B04','B05','B06','B09','B10','B11','B12',
        'B14','B16','IR1','IR2','IR3','IR4','VIS']

#brands=['B04']
areas=['001','002','003','004','005','006','007','008','009','010']


for brand in brands:
    
    path_out=path_out0+brand+'/'+time_c[0:8]+'/'
    
#    path_out=path_out0
    file_out='H8_HRIT_FLDK_'+brand+'_'+time_c+'.dat'
    
    if os.path.exists(path_out)==False:
        os.makedirs(path_out)
    
    file0='IMG_DK01'+brand+'_'+time_c
    TB1=read_hrit(path_in+file0+'_001')
    TB2=read_hrit(path_in+file0+'_002')
    TB3=read_hrit(path_in+file0+'_003')
    TB4=read_hrit(path_in+file0+'_004')
    TB5=read_hrit(path_in+file0+'_005')
    TB6=read_hrit(path_in+file0+'_006')
    TB7=read_hrit(path_in+file0+'_007')
    TB8=read_hrit(path_in+file0+'_008')
    TB9=read_hrit(path_in+file0+'_009')
    TB10=read_hrit(path_in+file0+'_010')
    
    TB=np.row_stack((TB1,TB2,TB3,TB4,TB5,TB6,TB7,TB8,TB9,TB10))
    TB=TB*10
    TB=np.array(TB,'short')
    f=open(path_out+file_out,'wb')
    f.write(TB)
    f.close()
    print(file_out)

#
#filename=path_out+file_out
#
#binfile=open(filename,'rb')
#    
##filename='D:\CI\CINS_win_test\HRIT_0\B04\H8_HRIT_FLDK_B04_201801110100.dat'
##binfile=open(filename,'rb')
#data0 = struct.unpack("7562500h",binfile.read(2750*2750*2))
#data1=np.array(data0,'float')
#data2=np.reshape(data1,[2750,2750])
#data2=data2/10.0
