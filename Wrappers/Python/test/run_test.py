import unittest
import numpy as np
import os
from ccpi.filters.regularisers import ROF_TV, FGP_TV
import matplotlib.pyplot as plt

def rmse(im1, im2):
    rmse = np.sqrt(np.sum((im1 - im2) ** 2) / float(im1.size))
    return rmse

class TestRegularisers(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_cpu_regularisers(self):
        filename = os.path.join(".." , ".." , ".." , "data" ,"lena_gray_512.tif")
        
        # read noiseless image
        Im = plt.imread(filename)
        Im = np.asarray(Im, dtype='float32')

        Im = Im/255
        tolerance = 1e-05
        rms_rof_exp = 0.006812507 #expected value for ROF model
        rms_fgp_exp = 0.019152347 #expected value for FGP model
        
        # set parameters for ROF-TV
        pars_rof_tv = {'algorithm': ROF_TV, \
                            'input' : Im,\
                            'regularisation_parameter':0.04,\
                            'number_of_iterations': 50,\
                            'time_marching_parameter': 0.0025
                            }
        # set parameters for FGP-TV
        pars_fgp_tv = {'algorithm' : FGP_TV, \
                            'input' : Im,\
                            'regularisation_parameter':0.04, \
                            'number_of_iterations' :50 ,\
                            'tolerance_constant':1e-08,\
                            'methodTV': 0 ,\
                            'nonneg': 0 ,\
                            'printingOut': 0 
                            }
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print ("_________testing ROF-TV (2D, CPU)__________")
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        res = True
        rof_cpu = ROF_TV(pars_rof_tv['input'],
             pars_rof_tv['regularisation_parameter'],
             pars_rof_tv['number_of_iterations'],
             pars_rof_tv['time_marching_parameter'],'cpu')
        rms_rof = rmse(Im, rof_cpu)
        # now compare obtained rms with the expected value
        self.assertLess(abs(rms_rof-rms_rof_exp) , tolerance)
        """
        if abs(rms_rof-self.rms_rof_exp) > self.tolerance:
            raise TypeError('ROF-TV (2D, CPU) test FAILED')
        else:
            print ("test PASSED")
        """
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print ("_________testing FGP-TV (2D, CPU)__________")
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        fgp_cpu = FGP_TV(pars_fgp_tv['input'], 
              pars_fgp_tv['regularisation_parameter'],
              pars_fgp_tv['number_of_iterations'],
              pars_fgp_tv['tolerance_constant'], 
              pars_fgp_tv['methodTV'],
              pars_fgp_tv['nonneg'],
              pars_fgp_tv['printingOut'],'cpu')  
        rms_fgp = rmse(Im, fgp_cpu)
        # now compare obtained rms with the expected value
        self.assertLess(abs(rms_fgp-rms_fgp_exp) , tolerance)
        """
        if abs(rms_fgp-self.rms_fgp_exp) > self.tolerance:
            raise TypeError('FGP-TV (2D, CPU) test FAILED')
        else:
            print ("test PASSED")
        """
        self.assertTrue(res)
    def test_gpu_regularisers(self):
        filename = os.path.join(".." , ".." , ".." , "data" ,"lena_gray_512.tif")
        
        # read noiseless image
        Im = plt.imread(filename)
        Im = np.asarray(Im, dtype='float32')

        Im = Im/255
        tolerance = 1e-05
        rms_rof_exp = 0.006812507 #expected value for ROF model
        rms_fgp_exp = 0.019152347 #expected value for FGP model
        
        # set parameters for ROF-TV
        pars_rof_tv = {'algorithm': ROF_TV, \
                            'input' : Im,\
                            'regularisation_parameter':0.04,\
                            'number_of_iterations': 50,\
                            'time_marching_parameter': 0.0025
                            }
        # set parameters for FGP-TV
        pars_fgp_tv = {'algorithm' : FGP_TV, \
                            'input' : Im,\
                            'regularisation_parameter':0.04, \
                            'number_of_iterations' :50 ,\
                            'tolerance_constant':1e-08,\
                            'methodTV': 0 ,\
                            'nonneg': 0 ,\
                            'printingOut': 0 
                            }
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print ("_________testing ROF-TV (2D, GPU)__________")
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        res = True
        rof_gpu = ROF_TV(pars_rof_tv['input'],
             pars_rof_tv['regularisation_parameter'],
             pars_rof_tv['number_of_iterations'],
             pars_rof_tv['time_marching_parameter'],'gpu')
        rms_rof = rmse(Im, rof_gpu)
        # now compare obtained rms with the expected value
        self.assertLess(abs(rms_rof-rms_rof_exp) , tolerance)
        """
        if abs(rms_rof-self.rms_rof_exp) > self.tolerance:
            raise TypeError('ROF-TV (2D, GPU) test FAILED')
        else:
            print ("test PASSED")
        """
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print ("_________testing FGP-TV (2D, GPU)__________")
        print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        fgp_gpu = FGP_TV(pars_fgp_tv['input'], 
              pars_fgp_tv['regularisation_parameter'],
              pars_fgp_tv['number_of_iterations'],
              pars_fgp_tv['tolerance_constant'], 
              pars_fgp_tv['methodTV'],
              pars_fgp_tv['nonneg'],
              pars_fgp_tv['printingOut'],'gpu')  
        rms_fgp = rmse(Im, fgp_gpu)
        # now compare obtained rms with the expected value
        self.assertLess(abs(rms_fgp-rms_fgp_exp) , tolerance)
        """
        if abs(rms_fgp-self.rms_fgp_exp) > self.tolerance:
            raise TypeError('FGP-TV (2D, GPU) test FAILED')
        else:
            print ("test PASSED")
        """
        self.assertTrue(res)
if __name__ == '__main__':
    unittest.main()