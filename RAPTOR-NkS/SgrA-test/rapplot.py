import sys
import numpy as np
import matplotlib
#matplotlib.use('TkAgg')
matplotlib.use('Agg')
from pathlib import Path
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import scipy.interpolate as spi

G = 6.674e-8
MSUN = 1.989e33
SPEED_OF_LIGHT = 2.998e10

KPC = 3.086e21
SEC_IN_DAY = 86400.
MAS_IN_DEG = 206264.806*1000.

def read_data_id(folder,ind):
    file_name = folder+'/img_data_%d.h5'%ind
    print("Reading keys from: ", file_name)
    images = h5py.File(file_name,'r')
    keys = [key for key in images.keys()]
    print(keys)
    images.close()
    return keys

def read_data(folder,ind,data_id):

    file_name = folder+'/img_data_%d.h5'%ind

    print("Reading in: ", file_name)

    images = h5py.File(file_name,'r')
    print(images.keys())
    min = [-100.,-100.,-100.,-100.]
    max = [100.,100.,100,100.]
    print(len(data_id))
    for j in range(0,len(data_id)-4):
        for i in range(0,len(images[data_id[j]])):
            current=np.max(images[data_id[j]][i])
            max[j]=np.maximum(max[j],np.max(images[data_id[j]][i]))
            min[j]=np.minimum(min[j],np.min(images[data_id[j]][i]))


    return min,max,images


def regrid_AMR(image,data_id,mas,Npix=200,method="linear"):
    alpha=[]
    beta=[]
    I=[]
    Q=[]
    U=[]
    V=[]
    
    
    #read in blocks of RAPTOR data(provided as 10x10 Pix blocks) and create singular array to regrid
    for i in range(0,len(image[data_id[0]])):
        alpha=np.append(alpha,(image['alpha'][i])*mas)
        beta=np.append(beta,(image['beta'][i])*mas)
        
        
        I=np.append(I,np.array(image[data_id[0]][i]))
        Q=np.append(Q,np.array(image[data_id[1]][i]))
        U=np.append(U,np.array(image[data_id[2]][i]))
        V=np.append(V,np.array(image[data_id[3]][i]))
    
    a_min=np.min(alpha)
    a_max=np.max(alpha)
    b_min=np.min(beta)
    b_max=np.max(beta)
    
    #create Npix x Npix grid on which to regrid amr data
    lin_alpha=np.linspace(a_min,a_max,Npix)
    lin_beta=np.linspace(b_min,b_max,Npix)
    
    a_mesh,b_mesh=np.meshgrid(lin_alpha,lin_beta)
    
    newpoints=(a_mesh,b_mesh)
    print(alpha.shape)
    print(beta.shape)

    points=np.vstack((alpha, beta)).T#reshape old pixels into single array
    
    #method="nearest"
    new_grid_I=spi.griddata(points,I,newpoints,method)
    new_grid_Q=spi.griddata(points,Q,newpoints,method)
    new_grid_U=spi.griddata(points,U,newpoints,method)
    new_grid_V=spi.griddata(points,V,newpoints,method)
    
    return a_mesh,b_mesh,new_grid_I,new_grid_Q,new_grid_U,new_grid_V




def plot_data_tau(image,data_id,ind,fig,ax,halfrange=40,mas=1,label="Stokes",cmap="CMRmap",vmin=-8,vmax=2):

    for i in range(0,len(image[data_id[ind]])):
        pixels=int(np.sqrt(len(image[data_id[ind]][i])))
        array=((np.reshape(image[data_id[ind]][i],(pixels,pixels))))
        alpha=((np.reshape(image['alpha'][i],(pixels,pixels))))*mas
        beta=((-np.reshape(image['beta'][i],(pixels,pixels))))*mas

        figure=ax.pcolormesh(alpha,beta,np.log10(array+1e-10),vmin=vmin,vmax=vmax,cmap=cmap,shading='auto')
        ax.set_aspect('equal')
        
    fig.colorbar(figure,label=label,ax=ax)

    ax.set_xlim(-halfrange*mas,halfrange*mas)
    ax.set_ylim(-halfrange*mas,halfrange*mas)

def plot_data_stokes(image,min,max,stokes_ind,data_id,fig,ax,halfrange=40,mas=1,label="Stokes",cmap="afmhot"):
    
    for i in range(0,len(image[data_id[stokes_ind]])):
        pixels=int(np.sqrt(len(image[data_id[stokes_ind]][i])))
        array=((np.reshape(image[data_id[stokes_ind]][i],(pixels,pixels))))
        alpha=((np.reshape(image['alpha'][i],(pixels,pixels))))*mas
        beta=((np.reshape(image['beta'][i],(pixels,pixels))))*mas
        
        ax.set_aspect('equal')
        if(stokes_ind==0): 
            figure=ax.pcolormesh(alpha,beta,(array/max[stokes_ind])**0.5,vmin=0,vmax=1,cmap=cmap,shading='auto')
        else:
            figure=ax.pcolormesh(alpha,beta,(array/max[stokes_ind]),vmin=-1,vmax=1,cmap=cmap,shading='auto')
    
    fig.colorbar(figure,label=label,ax=ax)
    
    ax.set_xlim(-halfrange*mas,halfrange*mas)
    ax.set_ylim(-halfrange*mas,halfrange*mas)

def plot_data_stokes_mesh(image,min,max,stokes_ind,data_id,fig,ax,Npix=200,halfrange=40,mas=1,label="Stokes",cmap="afmhot",scale="lin"):
    
    
    alpha,beta,I,Q,U,V = regrid_AMR(image,data_id,mas=mas,Npix=Npix,method="nearest")
    array=[I,Q,U,V]
    ax.set_aspect('equal')
    if(stokes_ind==0):
            if scale == "log":
                #datpoints = np.log10(array/max[stokes_ind])
                figure=ax.pcolormesh(alpha,beta,np.log10((array[stokes_ind]+1.e-20)/np.max(array[stokes_ind])),vmin=-5,vmax=0.,cmap=cmap,shading='auto')
            elif scale == "sqr":
                #datpoints =(array/max[stokes_ind])**0.5
                figure=ax.pcolormesh(alpha,beta,(array[stokes_ind]/np.max(array[stokes_ind]))**0.5,vmin=0,vmax=1,cmap=cmap,shading='auto')
            else:
                #datpoints=(array/max[stokes_ind])
                figure=ax.pcolormesh(alpha,beta,(array[stokes_ind]/np.max(array[stokes_ind])),vmin=0,vmax=1,cmap=cmap,shading='auto')

    else:
            figure=ax.pcolormesh(alpha,beta,(array[stokes_ind]/np.max(array[stokes_ind])),vmin=-1,vmax=1,cmap=cmap,shading='auto')
    
    fig.colorbar(figure,label=label,ax=ax)

    ax.set_xlim(-halfrange*mas,halfrange*mas)
    ax.set_ylim(-halfrange*mas,halfrange*mas)

#new quiver plot function, regrids AMR data to Npix x Npix image
def plot_data_quiver_mesh(image,min,max,stokes_ind,data_id,fig,ax,Npix=200,halfrange=40,mas=1,label="Stokes",cmap="afmhot",quiver=True):
    
    a_mesh,b_mesh,I,Q,U,V = regrid_AMR(image,data_id,mas=mas,Npix=Npix,method="nearest")
    ax.set_aspect('equal')

    #plot stokes I
    figure = ax.pcolormesh(a_mesh,b_mesh,(I/np.max(I)),vmin=0,vmax=1,cmap=cmap,shading='auto')
    
    
    
    ###pol quiver####
    if quiver == True:
        #Q=new_grid_Q
        #U=new_grid_U
        evpa = (180./np.pi)*0.5*np.arctan2(U,Q)
        evpa += 90.
        evpa[evpa > 90.] -= 180.
        
        npix = 10 #pixel to skip between quivers
        lpscal = np.max(np.sqrt(Q*Q+U*U))
     
        vxp = np.sqrt(Q*Q+U*U)*np.sin(evpa*3.14159/180.)/lpscal
        vyp = -np.sqrt(Q*Q+U*U)*np.cos(evpa*3.14159/180.)/lpscal
        fig = ax.quiver(a_mesh[::npix,::npix], b_mesh[::npix,::npix], vxp[::npix,::npix], vyp[::npix,::npix],pivot='mid',headwidth=0,headlength=0,headaxislength=0,color='white', scale_units='xy', scale=0.35,width=0.002)
    
    
    
    

def plot_data_quiver_reshaped(image,min,max,stokes_ind,data_id,fig,ax,halfrange=40,mas=1,label="Stokes",cmap="afmhot"):
    
    alpha=[]
    #alpha=np.array(alpha)
    beta=[]
    #beta=np.array(beta)
    I=[]#np.array([])
    Q=[]
    U=[]
    
    for i in range(0,len(image[data_id[stokes_ind]])):
        I_temp=image[data_id[0]][i] #np.array(image[data_id[0]][i])
        #print(image[data_id[0]][i])
        array=image[data_id[stokes_ind]][i]
        alpha2=image['alpha'][i]*mas
        beta2=image['beta'][i]*mas
        """
        print("block"+str(i))
        #print(array)
        #print(alpha)
        #print(beta)
        print('array min max ='+str(np.min(array))+' '+str(np.max(array)) )
        print('alpha min max ='+str(np.min(alpha))+' '+str(np.max(alpha)) )
        print('beta min max ='+str(np.min(beta))+' '+str(np.max(beta)) )
        """
        
        I=np.append(I,I_temp)
        print(len(I))
        alpha=np.append(alpha,(image['alpha'][i])*mas)
        beta=np.append(beta,(image['beta'][i])*mas)
        Q=np.append(Q,(image[data_id[1]][i]))
        U=np.append(U,np.array(image[data_id[2]][i]))
        print("block"+str(i))
        """
        array_I = ((np.reshape(image[data_id[0]][i],(pixels,pixels))))
        array_Q = ((np.reshape(image[data_id[1]][i],(pixels,pixels))))
        array_U = ((np.reshape(image[data_id[2]][i],(pixels,pixels))))

        Q = array_Q
        U = array_U
        """
    """
    pixels=int(np.sqrt(len(I)))
    I=(np.reshape(I,(pixels,pixels)))
    alpha=(np.reshape(alpha,(pixels,pixels)))
    beta=(np.reshape(beta,(pixels,pixels)))
    Q=(np.reshape(Q,(pixels,pixels)))
    U=(np.reshape(U,(pixels,pixels)))
    evpa = (180./3.14159)*0.5*np.arctan2(U,Q)
    """
    
    ordered_index=np.lexsort((beta,alpha))
    print(ordered_index)
    print(alpha)
    print(beta)
    
    alpha=alpha[ordered_index]
    beta=beta[ordered_index]
    array=I[ordered_index]
    
    pixels= int(np.sqrt(len(array)))
    array=((np.reshape(array,(pixels,pixels))))
    beta=((np.reshape(beta,(pixels,pixels))))
    alpha=((np.reshape(alpha,(pixels,pixels))))
    Q=((np.reshape(Q,(pixels,pixels))))
    U=((np.reshape(U,(pixels,pixels))))

    evpa = (180./3.14159)*0.5*np.arctan2(U,Q)
    evpa += 90.
    evpa[evpa > 90.] -= 180.
    
    figure = ax.pcolormesh(alpha,beta,(array/max[stokes_ind])**0.5,vmin=0,vmax=1,cmap=cmap,shading='auto')
    skip = 10
    Xs = alpha
    Ys = beta
    lpscal = np.max(np.sqrt(Q*Q+U*U))
    vxp = np.sqrt(Q*Q+U*U)*np.sin(evpa*3.14159/180.)/lpscal
    vyp = -np.sqrt(Q*Q+U*U)*np.cos(evpa*3.14159/180.)/lpscal
    #skip = int(npix/32)
    figure = ax.quiver(Xs[::skip,::skip], Ys[::skip,::skip], vxp[::skip,::skip], vyp[::skip,::skip],pivot='mid',headwidth=0,headlength=0,headaxislength=0,color='white', scale_units='xy', scale=50,width=0.002)
    

def plot_data_polfrac(image,max,data_id,fig,ax,halfrange=10,mas=1,label="|m|",cmap="afmhot"):

    for i in range(0,len(image[data_id[0]])):
        pixels=int(np.sqrt(len(image[data_id[0]][i])))

        array_I=((np.reshape(image[data_id[0]][i],(pixels,pixels))))
        array_Q=((np.reshape(image[data_id[1]][i],(pixels,pixels))))
        array_U=((np.reshape(image[data_id[2]][i],(pixels,pixels))))

        array = np.sqrt(array_Q**2.+array_U**2)/array_I
        array[array_I/max[0]<1e-7]=0

        alpha=((np.reshape(image['alpha'][i],(pixels,pixels))))*mas
        beta=((np.reshape(-image['beta'][i],(pixels,pixels))))*mas

        figure=ax.pcolormesh(alpha,beta,(array),vmin=0,vmax=1,cmap=cmap,shading='auto')


    fig.colorbar(figure,label=label,ax=ax)

    ax.set_xlim(-halfrange*mas,halfrange*mas)
    ax.set_ylim(-halfrange*mas,halfrange*mas)

def plot_data_RM(image,min,max,ind_1,ind_2,data_id,lam1,lam2,fig,ax,halfrange=10,mas=1,label="RM",cmap="RdBu"):

    lam1*=1e-3
    lam2*=1e-3
    for i in range(0,len(image[data_id[0]])):
        pixels=int(np.sqrt(len(image[data_id[0]][i])))

       	array_I_1=((np.reshape(image[data_id[ind_1]][i],(pixels,pixels))))
        array_Q_1=((np.reshape(image[data_id[ind_1 + 20]][i],(pixels,pixels))))
        array_U_1=((np.reshape(image[data_id[ind_1+ 40]][i],(pixels,pixels))))

        array_I_2=((np.reshape(image[data_id[ind_2]][i],(pixels,pixels))))
        array_Q_2=((np.reshape(image[data_id[ind_2+20]][i],(pixels,pixels))))
        array_U_2=((np.reshape(image[data_id[ind_2+40]][i],(pixels,pixels))))

        LP_1 = np.sqrt(array_Q_1**2. + array_U_1**2)
        LP_2 = np.sqrt(array_Q_2**2. + array_U_2**2)

        EVPA_1 = 0.5*np.angle(array_Q_1+1j*array_U_1)

        EVPA_2 = 0.5*np.angle(array_Q_2+1j*array_U_2)
        EVPA_2[EVPA_1==0.0]=0
        EVPA_1[EVPA_2==0.0]=0

        array= EVPA_2
        for j in range(0,pixels):
           for k in range(0,pixels):
             array[j,k] = EVPA_2[j,k]-EVPA_1[j,k]
             if(np.abs(array[j,k])>0.75*np.pi):
                 array[j,k]=array[j,k]-np.sign(array[j,k])*np.pi

        RM = (array) #/(lam2**2-lam1**2)

        RM[array_I_1/max[0]<1e-6]=0
        RM[array_I_2/max[0]<1e-6]=0

        alpha=((np.reshape(image['alpha'][i],(pixels,pixels))))*mas
        beta=((np.reshape(-image['beta'][i],(pixels,pixels))))*mas

        figure=ax.pcolormesh(alpha,beta,np.sign(RM)*np.abs(RM)**0.25,vmin=-1,vmax=1,cmap=cmap,shading='auto')

        ax.set_xlim(-halfrange*mas,halfrange*mas)
        ax.set_ylim(-halfrange*mas,halfrange*mas)


    fig.colorbar(figure,label=label,ax=ax)

    ax.set_xlim(-halfrange*mas,halfrange*mas)
    ax.set_ylim(-halfrange*mas,halfrange*mas)
