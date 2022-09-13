## ---------------------------------------------------------------------------
##    Copyright (c) 2019 Structura Biotechnology Inc. All rights reserved. 
##         Do not reproduce or redistribute, in whole or in part.
##      Use of this code is permitted only under licence from Structura.
##                   Contact us at info@structura.bio.
## ---------------------------------------------------------------------------

import numpy as n
import os

# particle stack
# frame stack (single movie)
# micrograph stack (or single)
# volume
# volume stack?

# just read the entire mrc as a 3D array of whatever dims
# but it stays [z,y,x] to be in C order

# read the entire
# read page range

def compute_filesize_header(header):
    '''
    Computes the theoretical filesize of the mrc image
    using information from the header.
    '''
    mrc_header_length = 1024
    nx = header['nx']
    ny = header['ny']
    nz = header['nz']
    datatype = header['datatype']
    nsymbt = header['nsymbt']
    dtype = mrc_datatype_to_dtype(datatype)
    nbytes_per_element = dtype().itemsize

    header_size = mrc_header_length + nsymbt
    data_size = float(ny*nx*nz*nbytes_per_element)
    filesize = header_size + data_size
    
    return filesize

def read_mrc_header_raw (file_obj):
    file_obj.seek(0)
    header_int32 = n.fromfile(file_obj, dtype=n.int32, count=256)
    return header_int32

def read_mrcfile(filename):
  return read_mrc_data(filep(filename),read_mrc_header(filep(filename)))
  
def read_mrc_header (file_obj):
    hdr = {}
    file_obj.seek(0)
    header_int32 = n.fromfile(file_obj, dtype=n.int32, count=256)
    header_float32 = header_int32.view(n.float32)
    [hdr['nx'], hdr['ny'], hdr['nz'], hdr['datatype']] = header_int32[:4]
    [hdr['xlen'],hdr['ylen'],hdr['zlen']] = header_float32[10:13]
    hdr['origin'] = header_float32[49:52]
    hdr['nsymbt'] = header_int32[23:24][0]
    return hdr

def mrc_datatype_to_dtype(datatype):
    datatype_map = {0 : n.uint8,
                    1 : n.int16,
                    2 : n.float32,
                    6 : n.uint16}
    if datatype not in datatype_map: 
        assert False,'Unsupported MRC datatype: {0}'.format(datatype)
    return datatype_map[datatype]

def mrc_dtype_to_datatype(dtype):
    if dtype == n.int8 or dtype == n.uint8:
        return 0
    elif dtype == n.int16:
        return 1
    elif dtype == n.float32:
        return 2
    elif dtype == n.uint16:
        return 6
    else:
        assert False,'Unsupported MRC dtype: {0}'.format(dtype)
    
def read_mrc_data(file_obj, header, start_page=None, end_page=None, out=None):
    nx = header['nx']
    ny = header['ny']
    nz = header['nz']
    datatype = header['datatype']
    nsymbt = header['nsymbt']
    dtype = mrc_datatype_to_dtype(datatype)
    nbytes_per_element = dtype().itemsize
    # mrc file has nz,ny,nx elements
    stride_per_page = ny*nx*nbytes_per_element
    if start_page is None: start_page = 0
    if end_page is None: end_page = nz
    num_pages = end_page - start_page
    file_obj.seek(1024 + nsymbt + start_page * stride_per_page)  # seek to start of data + skip first start_page pages
    if out is None:
        # if from_zyx_to_xyz:
        #     data = n.fromfile(file_obj, dtype=dtype, count= num_pages * ny * nx) . reshape (nx, ny, num_pages, order='F')
        # else:
        data = n.fromfile(file_obj, dtype=dtype, count= num_pages * ny * nx).reshape(num_pages, ny, nx)
    else:
        assert out.dtype == dtype 
        assert out.flags['C_CONTIGUOUS'] 
        assert out.size == num_pages * ny * nx
        buf = n.getbuffer(out)
        file_obj.readinto(buf)
        data = out
    return data

class mrc_page_lazy:
    def __init__(self, fname, shape, dtype, page, nsymbt):
        self.fname = fname
        self.shape = (int(shape[0]), int(shape[1]))
        self.page = page
        self.dtype = dtype
        self.length = (n.dtype(dtype).itemsize) * shape[0] * shape[1]
        self.offset = 1024 + nsymbt + page * self.length
    def get(self):
        with open(self.fname) as file_obj:
            file_obj.seek(self.offset)
            data = n.fromfile(file_obj, dtype=self.dtype, count= n.prod(self.shape)).reshape(self.shape)
        return data
    def view(self):
        return self.get()

def read_mrc(fname, start_page=None, end_page=None, lazy=False, return_psize=False, out=None):
    with open(fname, 'rb') as file_obj:
        header = read_mrc_header(file_obj)
        if lazy:
            nz, ny, nx = header['nz'], header['ny'], header['nx']
            dtype = mrc_datatype_to_dtype(header['datatype'])
            nsymbt = header['nsymbt']
            if start_page is None: start_page = 0
            if end_page is None: end_page = nz
            data = [mrc_page_lazy(fname, (ny, nx), dtype, page, nsymbt) for page in range(start_page, end_page)]
        else:
            data = read_mrc_data(file_obj, header, start_page, end_page, out)
    if return_psize:
        return header['xlen']/header['nx'], data
    return header, data

def mrc_header_create(data, psize):
    header = n.zeros(256, dtype=n.int32) # 1024 byte header
    header_f = header.view(n.float32)

    # data is C order: nz, ny, nx
    header[:3] = data.shape[::-1] # nx, ny, nz
    header[3] = mrc_dtype_to_datatype(data.dtype)
    header[7:10] = data.shape[::-1] # mx, my, mz (grid size)
    header_f[10:13] = [psize*i for i in data.shape[::-1]] # xlen, ylen, zlen
    header_f [13:16] = 90.0 # CELLB
    header [16:19] = [1,2,3] # axis order
    header_f [19:22] = [data.min(), data.max(), data.mean()]  # data stats
    # Put the origin at the center
#    header_f [49:52] = [psz*i/2 for i in data.shape ]
    header [52] = 542130509   # 'MAP ' chars
    header [53] = 16708
    return header

def mrc_header_create_custom(nx, ny, nz, dtype, psize, dmin, dmax, dmean):
    header = n.zeros(256, dtype=n.int32) # 1024 byte header
    header_f = header.view(n.float32)

    # data is C order: nz, ny, nx
    header[:3] = nx, ny, nz
    header[3] = mrc_dtype_to_datatype(dtype)
    header[7:10] = nx, ny, nz
    header_f[10:13] = [psize*i for i in (nx, ny, nz)] # xlen, ylen, zlen
    header_f [13:16] = 90.0 # CELLB
    header [16:19] = [1,2,3] # axis order
    header_f [19:22] = [dmin, dmax, dmean]  # data stats
    # Put the origin at the center
#    header_f [49:52] = [psz*i/2 for i in data.shape ]
    header [52] = 542130509   # 'MAP ' chars
    header [53] = 16708
    return header

def write_mrc(fname, data, psize):
    #assert data.ndim == 3, "Can only write out 3-D array in MRC file"

    # MRC only supports float32
    if data.dtype.name == 'float64':
        if os.environ.get('CRYOSPARC_DEVLOP', 'false') == 'true':
            assert False, "Cannot write 64 bit float MRC. Volumes should be 32-bit float!"
        data = n.float32(data)

    header = mrc_header_create(data, psize)
    with open(fname, 'wb') as file_obj:
        header.tofile(file_obj)
        # if from_xyz_to_zyx:
        #     n.require(data, requirements='C').reshape((-1,),order='F').ravel().tofile(file_obj)
        # else:
        n.require(data, requirements='C').ravel().tofile(file_obj)

def restack(output_path_abs, imgs, N, psize, output_dtype=n.float32, callback=None):
    """ img objects just have data_input_abspath and data_input_idx properties
    imgs should be sorted by (data_input_abspath, data_input_idx) but it's optional
    imgs will be written out in the order they are given.
    """
    
    # get all path, idx pairs
    # sort by path then idx (remember sort order)
    N_D = len(imgs)
    with open(output_path_abs, 'wb') as output_file:
        header = mrc_header_create_custom(N, N, N_D, output_dtype, psize, 0, 0, 0)
        header.tofile(output_file)
        current_input_path = None
        current_input_file = None
        num_done = 0
        for img in imgs:
            if img.data_input_abspath != current_input_path:
                if current_input_file is not None: current_input_file.close()
                current_input_path = img.data_input_abspath
                current_input_file = open(current_input_path)
                current_input_header = read_mrc_header(current_input_file)
                assert current_input_header['nx'] == N and current_input_header['ny'] == N, "Not all particles are the same box size!"
                datatype = current_input_header['datatype']
                nsymbt = current_input_header['nsymbt']
                dtype = mrc_datatype_to_dtype(datatype)
                nbytes_per_element = dtype().itemsize
                stride_per_page = N * N * nbytes_per_element
            current_input_file.seek(1024 + nsymbt + img.data_input_idx * stride_per_page)
            current_data = n.fromfile(current_input_file, dtype = dtype, count = N * N).astype(output_dtype)
            current_data.tofile(output_file)
            num_done += 1
            if callback is not None:
                callback(num_done, N_D)


# C************************************************************************
# C                                   *
# C   HEADER FORMAT                           *
# C   1   NX  number of columns (fastest changing in map) *
# C   2   NY  number of rows                  *
# C   3   NZ  number of sections (slowest changing in map)    *
# C   4   MODE    data type :                 *
# C           0   image : signed 8-bit bytes range -128   *
# C                   to 127              *
# C           1   image : 16-bit halfwords        *
# C           2   image : 32-bit reals            *
# C           3   transform : complex 16-bit integers *
# C           4   transform : complex 32-bit reals    *
# C   5   NXSTART number of first column in map           *
# C   6   NYSTART number of first row in map          *
# C   7   NZSTART number of first section in map          *
# C   8   MX  number of intervals along X         *
# C   9   MY  number of intervals along Y         *
# C   10  MZ  number of intervals along Z         *
# C   11-13   CELLA   cell dimensions in angstroms            *
# C   14-16   CELLB   cell angles in degrees              *
# C   17  MAPC    axis corresp to cols (1,2,3 for X,Y,Z)      *
# C   18  MAPR    axis corresp to rows (1,2,3 for X,Y,Z)      *
# C   19  MAPS    axis corresp to sections (1,2,3 for X,Y,Z)  *
# C   20  DMIN    minimum density value               *
# C   21  DMAX    maximum density value               *
# C   22  DMEAN   mean density value              *
# C   23  ISPG    space group number 0 or 1 (default=0)       *
# C   24  NSYMBT  size of extended header (which follows main header) in bytes*
# C   25-49   EXTRA   extra space used for anything           *
# C   50-52   ORIGIN  origin in X,Y,Z used for transforms     *
# C   53  MAP character string 'MAP ' to identify file type   *
# C   54  MACHST  machine stamp                   *
# C   55  RMS rms deviation of map from mean density      *
# C   56  NLABL   number of labels being used         *
# C   57-256  LABEL(80,10) 10 80-character text labels        *
# C                                   *
# C************************************************************************