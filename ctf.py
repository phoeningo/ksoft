#!/usr/bin/env python 
from mrc import *
import numpy as np
import sys
import argparse
import time



def ffts(arr):
  return np.log(np.abs(np.fft.fftshift(np.fft.fft2(arr))))

def plot_fft(arr):
  return np.log(np.abs(arr))

def dff(arr):
  return np.fft.fftshift(np.fft.fft2(arr))

def idf(arr):
  return np.abs(np.fft.ifft2(np.fft.ifftshift(arr)))

def fourier_crop(arr, N, out=None):
  old_N=arr.shape[-1]

  a=int(old_N/2-N/2)
  b=int(old_N/2+N/2)

  return arr[a:b,a:b]

def filep(filename):
  fp=open(filename)
  return fp
def read_mrcfile(filename):
  return read_mrc_data(filep(filename),read_mrc_header(filep(filename)))


def norm_mrc(data):
  n_data=np.array(data)
  n_max=np.max(n_data)
  n_min=np.min(n_data)
  return (n_data-n_min)/(n_max-n_min)

#2D ZERO PADDING
def zero_padding(arr,out=None):
  ##print(arr.shape)
  # reshaped into (4092,5760)
  old_y=arr.shape[-1]
  old_x=arr.shape[-2]
  
  new_size=max(old_x,old_y)
  new_arr=np.zeros([new_size,new_size])

  startx=int(new_size/2-old_x/2)
  endx=int(new_size/2+old_x/2)

  starty=int(new_size/2-old_y/2)
  endy=int(new_size/2+old_y/2) 

#  #print(startx,endx,starty,endy)
  new_arr[startx:endx,starty:endy]=arr[:]
  return new_arr

def shape_down(arr):
  in_time=time.time()
  z,y,x=arr.shape
  if z==1:
    return arr.reshape(y,x)
  else:
    return arr
  out_time=time.time()
  #print("read cost: %.3f s" % (out_time - in_time))

def shape_up(arr):
  y,x=arr.shape
  return arr.reshape(1,y,x)


def sigma_contrast(arr,s):
  #start_time=time.time()
  x,y=arr.shape

  ori_mean=np.mean(arr)
  ori_std=np.std(arr)
  low=ori_mean-s*ori_std
  high=ori_mean+s*ori_std
  arr[arr<low]=0
  arr[arr>high]=255
  arr=(arr-low)/(high-low)*255

  #'''
  #end_time=time.time()
 # print("sigma contrast cost: %.3f s" %(start_time-end_time))
  return arr

def arr_crop(arr,nx,ny,out=None):
  old_y=arr.shape[-1]
  old_x=arr.shape[-2]
  ax=int(old_x/2-nx/2)
  bx=int(old_x/2+nx/2)
  
  ay=int(old_y/2-ny/2)
  by=int(old_y/2+ny/2)

  return (arr[ax:bx,ay:by])

def read_orimrc(input_mrc):
  return shape_down(read_mrcfile(input_mrc))

def show_mrc(input_mrc,scale=0.1,sigma=0.5):
  start_time=time.time()
  img=shape_down(read_mrcfile(input_mrc))
 # check1=time.time()
  #print("read cost: %.3f s" % (check1 - start_time))
  img=norm_mrc(img)*255
  y,x=img.shape

  pad_img=zero_padding(img)
 # check2=time.time()
  #print("zero padding cost: %.3f s" % (check2 - check1))
  ##print(pad_img.shape)
  fft_pad=dff(pad_img)
 # check3=time.time()
  #print("dff cost: %.3f s" % (check3 - check2))
  crop_length=max(x,y)*scale
  croped_fft=fourier_crop(fft_pad,crop_length)
#  check4=time.time()
  #print("fourier_crop cost: %.3f s" % (check4 - check3))
  ##print(croped_fft.shape)
  back_crop=arr_crop(idf(croped_fft),y*scale,x*scale)
#  check5=time.time()
  #print("ifft cost: %.3f s" % (check5 - check4))
  ##print(back_crop.shape)
  output=sigma_contrast(back_crop,sigma)
#  check6=time.time()
  #print("sigma contrast cost: %.3f s" % (check6 - check5))
#  end_time=time.time()
  #print("time cost: %.3f s"%(end_time-start_time))
  return output
  #return back_crop
'''
start_time=time.time()

patch_size=args.batch_size
patch_num=args.batch_num
step_size=args.step
input_mrc=args.input
scale=args.scale

img=shape_down(read_mrcfile(input_mrc))
#print(np.min(img),np.max(img))
y,x=img.shape
#outshape=int(z/10),int(y/10),int(x/10)
pad_img=zero_padding(img)

fft_pad=dff(pad_img)
croped_fft=fourier_crop(fft_pad,x*scale)

back_crop=arr_crop(idf(croped_fft),y*scale,x*scale)

output=sigma_contrast(back_crop,args.sigma)
#print(np.min(output),np.max(output))
write_mrc(args.output,shape_up(output),1)


end_time=time.time()
#print("time sot: %.3f s"%(end_time-start_time))

'''




'''
xsize,ysize=avg.shape
crop_x,crop_y=int(xsize/2),int(ysize/2)

fft_avg=dff(avg)

bin2_img=fourier_bin(fft_avg,crop_x,crop_y)



patch_img=np.zeros(shape=(patch_size,patch_size),dtype=avg.dtype)
N=patch_size
cropped_size=N
avg_ctf=np.zeros(shape=(N,N))
ori_fft=np.zeros(shape=(N,N),dtype=np.complex)
final_startx=0
final_endx=0
final_starty=0
final_endy=0

for i in range(patch_num):
  #print('Patch: '+str(i+1))
  start_index=step_size*i
  end_index=step_size*i+patch_size
  ##print(start_index,end_index)
  try:
    tmp_patch=avg[0,start_index:end_index,start_index:end_index]
    patch_img[:]=tmp_patch
  except:
    if tmp_patch.shape[0]!=N:
      if final_endx==0:
        final_endx=end_index-step_size
        final_startx=start_index-step_size
      tmp_patch=avg[0,final_startx:final_endx,start_index:end_index]
      patch_img[:]=tmp_patch
    elif tmp_patch.shape[1]!=N:
      if final_endy==0:
        final_endy=end_indey-step_size
        final_starty=start_indey-step_size
      tmp_patch=avg[0,start_index:end_index,final_starty:final_endy]
      patch_img[:]=tmp_patch
    else:
      break

  tmp_fft=dff(patch_img)
#  tmp_crop=fourier_crop(tmp_fft,N)
  tmp_crop=tmp_fft
  avg_ctf+=plot_fft(tmp_crop)
#  ori_fft+=tmp_crop
avg_ctf/=patch_num
#ori_fft/=patch_num

##print(avg_ctf.shape[-2])

write_mrc('test_ctf.mrc',avg_ctf.reshape(1,N,N),1)

#M.write_file(np.uint8(avg_ctf),'avg_ctf.mrc')


#back_img=np.abs(np.fft.ifft2(np.fft.ifftshift(bin2_img)))

##print(back_img)

M.write_file(np.float32(back_img),'avg_back.mrc')
'''
