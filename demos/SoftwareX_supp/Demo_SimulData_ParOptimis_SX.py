#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This demo scripts support the following publication: 
"CCPi-Regularisation Toolkit for computed tomographic image reconstruction with 
proximal splitting algorithms" by Daniil Kazantsev, Edoardo Pasca, Martin J. Turner,
 Philip J. Withers; Software X, 2019
____________________________________________________________________________
* Reads data which is previosly generated by TomoPhantom software (Zenodo link)
--- https://doi.org/10.5281/zenodo.2578893
* Optimises for the regularisation parameters which later used in the script:
Demo_SimulData_Recon_SX.py
____________________________________________________________________________
>>>>> Dependencies: <<<<<
1. ASTRA toolbox: conda install -c astra-toolbox astra-toolbox
2. tomobar: conda install -c dkazanc tomobar
or install from https://github.com/dkazanc/ToMoBAR

@author: Daniil Kazantsev, e:mail daniil.kazantsev@diamond.ac.uk
GPLv3 license (ASTRA toolbox)
"""
# import timeit
import matplotlib.pyplot as plt
import numpy as np
import h5py
from ccpi.supp.qualitymetrics import QualityTools

# loading the data
h5f = h5py.File("data/TomoSim_data1550671417.h5", "r")
phantom = h5f["phantom"][:]
projdata_norm = h5f["projdata_norm"][:]
proj_angles = h5f["proj_angles"][:]
h5f.close()

[Vert_det, AnglesNum, Horiz_det] = np.shape(projdata_norm)
N_size = Vert_det

sliceSel = 128
# plt.gray()
plt.figure()
plt.subplot(131)
plt.imshow(phantom[sliceSel, :, :], vmin=0, vmax=1)
plt.title("3D Phantom, axial view")

plt.subplot(132)
plt.imshow(phantom[:, sliceSel, :], vmin=0, vmax=1)
plt.title("3D Phantom, coronal view")

plt.subplot(133)
plt.imshow(phantom[:, :, sliceSel], vmin=0, vmax=1)
plt.title("3D Phantom, sagittal view")
plt.show()

intens_max = 240
plt.figure()
plt.subplot(131)
plt.imshow(projdata_norm[:, sliceSel, :], vmin=0, vmax=intens_max)
plt.title("2D Projection (erroneous)")
plt.subplot(132)
plt.imshow(projdata_norm[sliceSel, :, :], vmin=0, vmax=intens_max)
plt.title("Sinogram view")
plt.subplot(133)
plt.imshow(projdata_norm[:, :, sliceSel], vmin=0, vmax=intens_max)
plt.title("Tangentogram view")
plt.show()
# %%
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("Reconstructing with ADMM method using tomobar software")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
# initialise tomobar ITERATIVE reconstruction class ONCE
from tomobar.methodsIR import RecToolsIR

RectoolsIR = RecToolsIR(
    DetectorsDimH=Horiz_det,  # DetectorsDimH # detector dimension (horizontal)
    DetectorsDimV=Vert_det,  # DetectorsDimV # detector dimension (vertical) for 3D case only
    AnglesVec=proj_angles,  # array of angles in radians
    ObjSize=N_size,  # a scalar to define reconstructed object dimensions
    datafidelity="LS",  # data fidelity, choose LS, PWLS (wip), GH (wip), Student (wip)
    nonnegativity="ENABLE",  # enable nonnegativity constraint (set to 'ENABLE')
    OS_number=None,  # the number of subsets, NONE/(or > 1) ~ classical / ordered subsets
    tolerance=0.0,  # tolerance to stop inner (regularisation) iterations earlier
    device="gpu",
)
# %%
param_space = 30
reg_param_sb_vec = np.linspace(
    0.03, 0.15, param_space, dtype="float32"
)  # a vector of parameters
erros_vec_sbtv = np.zeros((param_space))  # a vector of errors

print("Reconstructing with ADMM method using SB-TV penalty")
for i in range(0, param_space):
    RecADMM_reg_sbtv = RectoolsIR.ADMM(
        projdata_norm,
        rho_const=2000.0,
        iterationsADMM=15,
        regularisation="SB_TV",
        regularisation_parameter=reg_param_sb_vec[i],
        regularisation_iterations=50,
    )
    # calculate errors
    Qtools = QualityTools(phantom, RecADMM_reg_sbtv)
    erros_vec_sbtv[i] = Qtools.rmse()
    print(
        "RMSE for regularisation parameter {} for ADMM-SB-TV is {}".format(
            reg_param_sb_vec[i], erros_vec_sbtv[i]
        )
    )

plt.figure()
plt.plot(erros_vec_sbtv)

# Saving generated data with a unique time label
h5f = h5py.File("Optim_admm_sbtv.h5", "w")
h5f.create_dataset("reg_param_sb_vec", data=reg_param_sb_vec)
h5f.create_dataset("erros_vec_sbtv", data=erros_vec_sbtv)
h5f.close()
# %%
param_space = 30
reg_param_rofllt_vec = np.linspace(
    0.03, 0.15, param_space, dtype="float32"
)  # a vector of parameters
erros_vec_rofllt = np.zeros((param_space))  # a vector of errors

print("Reconstructing with ADMM method using ROF-LLT penalty")
for i in range(0, param_space):
    RecADMM_reg_rofllt = RectoolsIR.ADMM(
        projdata_norm,
        rho_const=2000.0,
        iterationsADMM=15,
        regularisation="LLT_ROF",
        regularisation_parameter=reg_param_rofllt_vec[i],
        regularisation_parameter2=0.005,
        regularisation_iterations=600,
    )
    # calculate errors
    Qtools = QualityTools(phantom, RecADMM_reg_rofllt)
    erros_vec_rofllt[i] = Qtools.rmse()
    print(
        "RMSE for regularisation parameter {} for ADMM-ROF-LLT is {}".format(
            reg_param_rofllt_vec[i], erros_vec_rofllt[i]
        )
    )

plt.figure()
plt.plot(erros_vec_rofllt)

# Saving generated data with a unique time label
h5f = h5py.File("Optim_admm_rofllt.h5", "w")
h5f.create_dataset("reg_param_rofllt_vec", data=reg_param_rofllt_vec)
h5f.create_dataset("erros_vec_rofllt", data=erros_vec_rofllt)
h5f.close()
# %%
param_space = 30
reg_param_tgv_vec = np.linspace(
    0.03, 0.15, param_space, dtype="float32"
)  # a vector of parameters
erros_vec_tgv = np.zeros((param_space))  # a vector of errors

print("Reconstructing with ADMM method using TGV penalty")
for i in range(0, param_space):
    RecADMM_reg_tgv = RectoolsIR.ADMM(
        projdata_norm,
        rho_const=2000.0,
        iterationsADMM=15,
        regularisation="TGV",
        regularisation_parameter=reg_param_tgv_vec[i],
        regularisation_iterations=600,
    )
    # calculate errors
    Qtools = QualityTools(phantom, RecADMM_reg_tgv)
    erros_vec_tgv[i] = Qtools.rmse()
    print(
        "RMSE for regularisation parameter {} for ADMM-TGV is {}".format(
            reg_param_tgv_vec[i], erros_vec_tgv[i]
        )
    )

plt.figure()
plt.plot(erros_vec_tgv)

# Saving generated data with a unique time label
h5f = h5py.File("Optim_admm_tgv.h5", "w")
h5f.create_dataset("reg_param_tgv_vec", data=reg_param_tgv_vec)
h5f.create_dataset("erros_vec_tgv", data=erros_vec_tgv)
h5f.close()
# %%
