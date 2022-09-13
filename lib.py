#Author : Fang Kong @ Tsinghua Univ.
import numpy as np
#import mrcfile
import time
from glob import glob
import os






 
def map2uint8(arr):
  amin=np.min(arr)
  amax=np.max(arr)
  return np.uint8(255*(arr-amin)/(amax-amin))


class method(object):
  def test(ins):
    return 0
  @staticmethod
  def map2uint8(arr):
    amin=np.min(arr)
    amax=np.max(arr)
    return np.uint8(255*(arr-amin)/(amax-amin))

  @staticmethod
  def write_pix_file(imgdata,filename,pix):
    print('writing...'+filename)
    try:
      with mrcfile.open(filename,mode='r+') as mrc:
        mrc.voxel_size=pix
        mrc.set_data(imgdata)
        mrc.close()
    except:
      with mrcfile.new(filename,overwrite=True) as mrc:
        mrc.set_data(imgdata)
        mrc.close()
      with mrcfile.open(filename,mode='r+') as mrc:
        mrc.voxel_size=pix
        #mrc.set_data(imgdata)
        mrc.close()

  @staticmethod 
  def star_read(file):
    file_p=open(file)
    lines=file_p.read()
    #print(lines)
    file_p=None
    line_sp=lines.split('\n')
    line_sp.remove('')
    #print(line_sp)
    return line_sp   



 
  @staticmethod
  def write_file(imgdata,filename):
    print('writing...'+filename) 
    with mrcfile.new(filename,overwrite=True) as mrc:
        mrc.set_data(imgdata)
        mrc.close()


  @staticmethod
  def read_mrc(filename):
    mrc=mrcfile.open(filename)
    data=mrc.data
    arr=np.zeros(shape=data.shape,dtype=np.uint8)
    arr[:]=data[:]
    data=0 
    return arr


  @staticmethod
  def read_float_mrc(filename):
    mrc=mrcfile.open(filename)
    data=mrc.data
    arr=np.zeros(shape=data.shape,dtype=np.float32)
    arr[:]=data[:]
    data=0 
    return arr

  @staticmethod
  def read_pix_mrc(filename):
    mrc=mrcfile.open(filename)
    data=mrc.data
    arr=np.zeros(shape=data.shape,dtype=np.float32)
    arr[:]=data[:]
    data=0 
    return arr,mrc.voxel_size

  @staticmethod
  def time_clock(t1):
    print('time cost: ',"%.3f"%(time.time()-t1),' s')
    t1=time.time()
    return t1


  @staticmethod
  def Input_read(dir,suffix):
    files=glob(dir+'/*.'+suffix)
    L=len(files)
    if L==0:
      print('no file exists')
      return -1,-1,-1,-1,-1
    else:
      print(str(len(files))+' files in ',dir)
      (x,y,z)=mrcfile.mmap(files[0]).data.shape
      raw_input=np.zeros(dtype=np.uint8,shape=[L,x,y,z,1])
      for filei in range(L):
        mrc=mrcfile.mmap(files[filei])
        content=np.array(mrc.data)
        mrc=0
        rshape=np.array(content).reshape([1,x,y,z,1])
     #   print(rshape)
        raw_input[filei,:]=rshape[:]
      return raw_input,L,files

  @staticmethod
  def file_read(dir,suffix):
    files=glob(dir+'/*.'+suffix)
    L=len(files)
    return files,L

  @staticmethod
  def dir_read(dir,suffix):
    files=glob(dir+'/*.'+suffix)
    L=len(files)
    if L==0:
      print('no file exists')
      return -1,-1,-1
    else:
      print(str(len(files))+' files in ',dir)
      (x,y,z)=mrcfile.mmap(files[0]).data.shape
      raw_input=[]
      #raw_input=np.zeros(dtype=np.uint8,shape=[L,x,y,z,1])
      for filei in range(L):
        mrc=mrcfile.mmap(files[filei])
        content=np.array(mrc.data,dtype=np.uint8)
        mrc=0
       # rshape=np.array(content).reshape([1,x,y,z,1])
     #   print(rshape)
        raw_input.append(content)
      return raw_input,L,files

  @staticmethod
  def Particles_read(dir,suffix):
    files=glob(dir+'/*.'+suffix)
    L=len(files)
    if L==0:
      print('no file exists')
      return -1,-1,-1,-1
    else:
      print(str(len(files))+' files in ',dir)
      (x,y,z)=mrcfile.mmap(files[0]).data.shape
      raw_input=np.zeros(dtype=np.uint8,shape=[L,x,y,z])
      for filei in range(L):
        mrc=mrcfile.mmap(files[filei])
        content=np.array(mrc.data)
        mrc=0
        rshape=map2uint8(np.array(content).reshape([x,y,z]))
        rbw=BW(rshape)
     #   print(rshape)
        raw_input[filei,:]=rbw[:]
      return raw_input,L

  @staticmethod
  def get_name(filename):
    filename_split=filename.split('/')
    mrcname=filename_split[len(filename_split)-1]
    mrc=mrcname.split('.')
    return mrc[0]


  @staticmethod
  def create_newdir(path):
    if os.path.exists(path):
      os.system('rm -rf '+path+'/')
    print('mkdir',path)
    os.system('mkdir '+path)


  @staticmethod
  def create_dir(path):
    if os.path.exists(path):
      return
    print('mkdir',path)
    os.system('mkdir '+path)

  @staticmethod
  def raw(filename):
    mrc=mrcfile.open(filename,permissive=True)
    data=mrc.data
    arr=np.zeros(shape=data.shape,dtype=data.dtype)
    arr[:]=data[:]
    data=0 
    return arr

  @staticmethod
  def dist(arra,arrb):
    return np.sqrt(np.square(arra[0]-arrb[0])+np.square(arra[1]-arrb[1])+np.square(arra[2]-arrb[2]))

  @staticmethod
  def draw_box(x,y,z,sigma,mean):
    image_box=np.uint8(np.random.randn(x,y,z)*sigma+mean)
    return image_box


  @staticmethod
  def draw_empty(x,y,z):
    image_box=np.zeros(shape=(x,y,z),dtype=np.uint8)
    return image_box

  @staticmethod
  def single_2d(img):
    if len(img.shape)==3:
      return img[:,:,0]
    else:
      return img
  @staticmethod 
  def cmd_exec(cmd,mode=0):
    if mode==0:
      print(cmd)
      return 0
    elif mode==1:
      res=os.popen(cmd).read()
      return res

  

