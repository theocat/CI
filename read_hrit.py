# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 13:40:44 2017

@author: nriet
"""
# a function for get kuihua8 data set

import numpy as np
import struct
#import os
#import matplotlib.pyplot as plt
import bz2file

path_in='D:/python_project/HRIT/data/'

filename=path_in+'IMG_DK01B07_201804020810_003'

#def read_hrit(filename):
def read_hrit(filename):
    if 'bz2' in filename:
        binfile=bz2file.open(filename,'rb')
    else:
        binfile=open(filename,'rb')
        #### Hearder Type #0 Primary Header
    Header_Type,    = struct.unpack(">B",binfile.read(1))
    Header_Record_Length,    = struct.unpack(">H",binfile.read(2))
    File_Type_Code, = struct.unpack(">B",binfile.read(1))
    Total_Header_Length, = struct.unpack(">L",binfile.read(4))
    Data_Filed_Length,   = struct.unpack(">Q",binfile.read(8))
    if File_Type_Code ==0 :
        #### Hearder Type #1 Image Structure 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        NB,             = struct.unpack(">B",binfile.read(1))
        NC,NL,          = struct.unpack(">2H",binfile.read(4))
        Compression_Flag, = struct.unpack(">B",binfile.read(1))
        #### Hearder Type #2 Image Navigation 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        Projection_Name, = struct.unpack("32s",binfile.read(32))
        CFAC,LFAC,COFF,LOFF,  = struct.unpack(">4i",binfile.read(16))
        #### Hearder Type #3 Image Data Function
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        ll=Header_Record_Length-3
        Data_Definition_Block,= struct.unpack(str(ll)+"s",binfile.read(ll))
        #### Hearder Type #4 Annotation 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        ll=Header_Record_Length-3
        Annotation_Text,= struct.unpack(str(ll)+"s",binfile.read(ll))
        #### Hearder Type #5 Time Stamp 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        CDS_P_Field,    = struct.unpack(">B",binfile.read(1))
        CDS_T_Field1,CDS_T_Field2,  = struct.unpack(">HI",binfile.read(6))
        ### Hearder Type #128 Image Segment Identification
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        Image_Segm_Seq_No,Total_No_Image_Segm,Line_No_Image_Segm, = \
            struct.unpack(">BBH",binfile.read(4))
        ### Hearder Type #130 Ancillary Text 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        ll=Header_Record_Length-3
        Image_Compensation_Information,= struct.unpack(str(ll)+"s",binfile.read(ll))
        ### Hearder Type #131 Ancillary Text 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        ll=Header_Record_Length-3
        Image_Observation_Time,= struct.unpack(str(ll)+"s",binfile.read(ll))
         ### Hearder Type #132 Image_Observation_Time 
        Header_Type,    = struct.unpack(">B",binfile.read(1))
        Header_Record_Length, = struct.unpack(">H",binfile.read(2))
        ll=Header_Record_Length-3
        Image_Quality_Information,= struct.unpack(str(ll)+"s",binfile.read(ll))

        nn=NC*NL
        Data0 =struct.unpack(">"+str(nn)+"h",binfile.read(nn*2))
        Data     =  np.array(Data0,float)
        Data     =  Data.reshape(NL,NC)
        data_def=Data_Definition_Block.split("\r")
        l=len(data_def)
        if data_def[2]=='_UNIT:=ALBEDO(%)':
            for i in range(3,l-1): 
                temp_c=np.array(data_def[i].split(':='),float)
                Data[np.where(Data==temp_c[0])]=temp_c[1]
            Data=Data*0.1
        elif data_def[2]=='_UNIT:=KELVIN':
            temp_c=np.array(data_def[3].split(':='),float)
            Data[np.where(Data<=temp_c[0])]=temp_c[1]
            temp_c=np.array(data_def[-2].split(':='),float)
            Data[np.where(Data>=temp_c[0])]=temp_c[1]
            for i in range(3,l-2):           
                temp_c1=np.array(data_def[i].split(':='),float)
                temp_c2=np.array(data_def[i+1].split(':='),float)
                aa=np.where((Data>=temp_c1[0]) & (Data<temp_c2[0]))
                Data[aa]=temp_c1[1]+(temp_c1[1]-temp_c2[1])/(temp_c1[0]-temp_c2[0])*(Data[aa]-temp_c1[0])            
    binfile.close()
    return Data 