#%%
import numpy as np
import time
import urllib.request
from scipy import ndimage
from matplotlib import pyplot as plt

#%%
#function definitions

def print_properties(x):
    """print all properties of an array"""
    print("\n type : " + str(type(x))
    + "\n size : " + str(x.size)
    + "\n shape : " + str(x.shape)
    + "\n dtype : " + str(x.dtype)
    + "\n ndim : " + str(x.ndim)
    + "\n itemsize : " + str(x.itemsize)
    + "\n nbytes : " + str(x.nbytes))
    
# visualisatino while developing comparing image and
# it's transform and specified slices
def plot_comp(data, slice_index=15):
    """plot image and its transform to compare"""
    plt.figure()
    plt.subplot(1,2,1)
    if data.ndim ==3:
        data = data[slice_index, : ,:] 
    plt.imshow(data, cmap=plt.cm.gray)
    plt.subplot(1,2,2)
    plt.imshow(pre_built(data))
    plt.show()

def ecld_dist_alg(p,q):
    """euclidean distance between two points p,q
       np.sqrt((p[x]-qx)**2 + (py-qy)**2 + (pz-qz)**2)    """
    return np.sqrt(np.sum((p-q)**2))

def pre_built(vol_bi_img):
    """this is the in built distance transform to compare with"""
    return ndimage.distance_transform_edt(vol_bi_img)

###########################################################################

#%%
#Download data
""" 
download label_train00.npy from download link provided in course work
“label_train00.npy” loaded as lbt_data contains a binary segmentation of Pelvic MR volume image
"""

lbt_url = 'https://weisslab.cs.ucl.ac.uk/WEISSTeaching/datasets/-/raw/promise12/label_train00.npy'
urllib.request.urlretrieve(lbt_url, 'lbt_file.npy')
lbt_data = np.load('lbt_file.npy',allow_pickle=False)

"""
Euclidean transform
input = bianary image
output = distance map

each pixel contains the euclidean distance
to the closest obstacle pixel, in this case boundary pixel

ecld_dist = sqrt((p[i]-q[i]**2)+(p[j]-q[j]**2)+(p[k]-q[k]**2)))

for each 1, the distance from the nearest 0
"""

#%%
def distance_transform_np(v_b_i, dims = np.array([1,1,1])):
    """Brute force approach. Find coordinates fo all zeroes and all ones. 
    For each one compute the euclidean distance to all zeros 
    and save the minimun distance in the transform
    Inputs:
    v_b_i = volumetric binary image, input as an array
    dims = np.array([dx,dy,dz]), the dimentions of the image in each direction, also and array
    """
    zeros_coord = np.where(v_b_i == 0)                  #find the coordinates of all zeros 
    zeros = np.asarray(zeros_coord).T                   # store them
    zeros_ = zeros*dims
    ones_coord = np.where(v_b_i == 1)                   # find coordinates of all ones
    ones = np.asarray(ones_coord).T                     #store them
    ones_ = ones*dims
                                                        
                                                        
    a = -2 * np.dot(ones_, zeros_.T)                    # calculate distance 
    b = np.sum(np.square(zeros_), axis=1)               # sum of coordinates squared
    c = np.sum(np.square(ones_), axis=1)[:,np.newaxis]
    euc_dist = a + b + c                                #sqrt of sums   
    euc_dist = np.sqrt(euc_dist.min(axis=1))            #min euclidean dist of each one pixel to zero pixel
    x = v_b_i.shape[0]                          
    y = v_b_i.shape[1]
    z = v_b_i.shape[2]
    euc_d_transform = np.zeros((x,y,z))
    euc_d_transform[ones[:,0], ones[:,1], ones[:,2]] = euc_dist 
    
    return (euc_d_transform)

#%%

# In the interest of computational time I have only computed the distance_transform_np for the 
# regions around the points i've chosen to plot. 
# I have compared the array values to the distance_transform_edt[full] (for mean and std)
# and i have compared the time to the distance_transform[region]
f = 7 
g = 14
a = lbt_data[f:g]

j=19
k=26
b = lbt_data[j:k]
#%%
print("Time Comparison")
ab = ndimage.distance_transform_edt(lbt_data, sampling = [2,.5,.5])
pre_alg_time = time.time()
a1 = ndimage.distance_transform_edt(a,sampling=[2,.5,.5])
b1 = ndimage.distance_transform_edt(b,sampling=[2,.5,.5])
#a1 = pre_built(a)
#b1 = pre_built(b)
print("distance_trans_ent takes %s seconds " % (time.time() - pre_alg_time))

#print(a1[15])
my_alg_time = time.time()
a2 = distance_transform_np(a, dims=np.array([2,.5,.5]))
b2 = distance_transform_np(b, dims=np.array([2,.5,.5])) 
print("distance_transform_np takes %s seconds " % (time.time() - my_alg_time))

print("\nMy implementation is much slower than distance_transform_edt which runs through c. I have implemented a Brute Force Approach, which is known for being memory and time intensive.")

#%%
mean_voxel_difference = np.mean((ab[f:g] - a2)+(ab[j:k]-b2))
std_of_voxel_difference = np.mean((ab[f:g] - a2)+(ab[j:k]-b2))

print("\nMean voxel level difference = ", end = '')
print(mean_voxel_difference)
print("Standard deviation of voxel level difference = ", end = '')
print(std_of_voxel_difference)
#%%
# much prettier saved through matplotlib but have done through pillows too
for i in [2,4,6]:
    plt.figure()
    plt.subplot(1,3,1)
    plt.title("slice number = " + str(f+i))
    plt.imshow(a[i])
    #plt.imshow(a1[i])
    plt.subplot(1,3,2)
    plt.title("edt")
    plt.imshow(ab[f+i])
    plt.subplot(1,3,3)
    plt.title("np")
    plt.imshow(a2[i])
    #print(np.array_equal (ab[f+i], a2[i], equal_nan=False))
    #print(np.array_equal (a1[i], a2[i], equal_nan=False))
    plt.savefig('../task1/slice'+str(f+i)+'.png') 
    plt.show()

    
for i in [0,4]:
    plt.figure()
    plt.subplot(1,3,1)
    plt.title("slice number = " + str(j+i))
    plt.imshow(b[i])
    #plt.imshow(b1[i])
    plt.subplot(1,3,2)
    plt.title("edt")
    plt.imshow(ab[j+i])
    plt.subplot(1,3,3)
    plt.title("np")
    plt.imshow(b2[i])
    #print(np.array_equal (ab[j+i], b2[i], equal_nan=False))
    #print(np.array_equal (b1[i], b2[i], equal_nan=False))
    plt.savefig('../task1/slice'+str(j+i)+'.png') 
    plt.show()
#%%
def save_im(array, title):
    """Saves an array as an image using pillow, with title input including image type, ex:.png """
    dem = array.max()-array.min()
    if dem == 0:
        array = (array- array.min())*0
    else:
        array = (array-array.min()) / (dem) *255       
    #array = (array-array.min()) / (array.max()-array.min()) *255 
    im = Image.fromarray(array.astype('uint8'))
    im.save(title)

from PIL import Image
for i in [2,4,6]:
    my = a[i]
    title = '../task1/slice'+str(f+i) +'_0im.png'
    save_im(my, title)

    my = ab[f+i]
    title = '../task1/slice' + str(f+i) +'_edt.png'
    save_im(my, title)

    my=a2[i]
    title = '../task1/slice' + str(f+i) +'_np.png'
    save_im(my, title)

for i in [0,4]:
    my=b[i]
    title = '../task1/slice' + str(j+i) +'_0im.png'
    save_im(my,title)

    my=ab[j+i]
    title = '../task1/slice' + str(j+i) +'_edt.png'
    save_im(my,title)

    my=b2[i]
    title = '../task1/slice' + str(j+i) +'_np.png'
    save_im(my, title)

# %%
