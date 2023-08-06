#Standard python libraries
import os

#Dependencies
import numpy as np
import yaml
import matplotlib.pyplot as plt
from pyfftw.interfaces.numpy_fft import fft, fftshift, ifft, ifftshift, fftfreq

#TransientAbsorption implemented using UF2
from ultrafastultrafast.signals import TransientAbsorption

"""The following definitions of I4_mat and kdelvec are based
upon the formulas given in Appendix B of Molecular Quantum 
Electrodynamics, by Akbar Salam
"""

I4_mat = np.array([[4,-1,-1],[-1,4,-1],[-1,-1,4]])/30

def kdel(x,y):
    """Kronecker Delta"""
    if x == y:
        return 1
    else:
        return 0

def kdel2(a,b,c,d):
    """Product of 2 Kronecker Deltas"""
    return kdel(a,b)*kdel(c,d)

def kdelvec(i,j,k,l):
    """Length 3 vector of Kronecker Delta products, as defined in """
    vec = [kdel2(i,j,k,l),
           kdel2(i,k,j,l),
           kdel2(i,l,j,k)]
    return np.array(vec)

class TransientAbsorptionIsotropicAverage(object):
    """This class performs the isotropic average of the 4th order tensor
        which is the material response produced by 4-wave mixing process"""
    def __init__(self,parameter_file_path,efield_polarization,*, num_conv_points=138,
                 initial_state=0,dt=0.1,total_num_time_points = 3686):
        # This is the object that will actually calculate all of the signals
        self.TA = TransientAbsorption(parameter_file_path,
                                      num_conv_points=num_conv_points,
                                      initial_state=initial_state, dt=dt,
                                      total_num_time_points=total_num_time_points)
        # Lab frame polarization sequence for pulses
        self.efield_polarization = efield_polarization
        # Working directory
        self.base_path = self.TA.base_path

    def set_homogeneous_linewidth(self,*args,**kwargs):
        self.TA.set_homogeneous_linewidth(*args,**kwargs)

    def set_inhomogeneous_linewidth(self,*args,**kwargs):
        self.TA.set_inhomogeneous_linewidth(*args,**kwargs)

    def recenter(self,*args,**kwargs):
        self.TA.recenter(*args,**kwargs)

    def set_pulse_shapes(self,*args,**kwargs):
        # Pass pulse shapes on to the self.TA object
        self.TA.set_pulse_shapes(*args,**kwargs)

    def calculate_spectra(self,delay_times):
        # The isotropic averaging is performed based upon the real orientation of the lab frame pulses
        # The calculation will differ depending on whether the pump and probe are aligned or crossed
        left_vec = kdelvec(*self.efield_polarization)

        xyz = ['x','y','z']

        pol_options = []
        for i in range(3):
            # Check to see if the dipole operator has any non-zero components along the given
            # molecular frame axis, if the dipole exists only in the x-y plane, for example,
            # then we can avoid doing quite a few unnecessary calculations!
            if not np.allclose(self.TA.mu_GSM_to_SEM[:,:,i],0):
                pol_options.append(xyz[i])
        
        signal = np.zeros((self.TA.w.size,delay_times.size))

        for i in pol_options:
            for j in pol_options:
                for k in pol_options:
                    for l in pol_options:
                        # generate the vector of kronecker delta products
                        right_vec = kdelvec(i,j,k,l)
                        if np.allclose(right_vec,0):
                            # If the vector is 0, don't bother!
                            pass
                        else:
                            # If not, set the polarization sequence, do the calculation, and
                            # add the weight given by the isotropic weight matrix, I4_mat
                            # Note the the polarization sequences are not the lab frame
                            # polarization sequence of the pulses.
                            self.TA.set_polarization_sequence([i,j,k,l])
                            weight = I4_mat.dot(right_vec)
                            weight = np.dot(left_vec,weight)
                            signal += weight * self.TA.calculate_pump_probe_spectra_vs_delay_time(delay_times)
                            
        # Full isotorpically averaged signal
        self.signal_vs_delay_times = signal
        self.delay_times = delay_times
        self.w = self.TA.w
        
        # Center frequency of pulses in the RWA
        self.center = self.TA.center

        return signal

    def save(self,**kwargs):
        self.save_pump_probe_spectra_vs_delay_time(**kwargs)

    def save_pump_probe_spectra_vs_delay_time(self,*,save_file_name='default'):
        if save_file_name == 'default':
            save_name = os.path.join(self.base_path,'TA_spectra_iso_ave.npz')
        else:
            save_name = os.path.join(self.base_path,save_file_name)
        np.savez(save_name,signal = self.signal_vs_delay_times, delay_times = self.delay_times, frequencies = self.w, pulse_center = self.center)
        
    def load_pump_probe_spectra_vs_delay_time(self):
        load_name = self.base_path + 'TA_spectra_iso_ave.npz'
        arch = np.load(load_name)
        self.signal_vs_delay_times = arch['signal']
        self.delay_times = arch['delay_times']
        self.w = arch['frequencies']
        try:
            self.center = arch['pulse_center']
        except KeyError:
            warnings.warn('Pulse center was not saved in archive, setting center = 0')
            self.center = 0

    def plot_pump_probe_spectra(self,*,frequency_range=[-1000,1000], subtract_DC = True, create_figure=True,
               color_range = 'auto',draw_colorbar = True,save_fig=True):
        """Plots the transient absorption spectra with detection frequency on the
        y-axis and delay time on the x-axis.

        Args:
            frequency_range (list): sets the min (list[0]) and max (list[1]) detection frequency for y-axis
            subtract_DC (bool): if True subtract the DC component of the TA
            color_range (list): sets the min (list[0]) and max (list[1]) value for the colorbar
            draw_colorbar (bool): if True add a colorbar to the plot
            save_fig (bool): if True save the figure that is produced
        """
        # Cut out unwanted detection frequency points
        w_ind = np.where((self.w > frequency_range[0]) & (self.w < frequency_range[1]))[0]
        w = self.w[w_ind]
        sig = self.signal_vs_delay_times[w_ind,:]

        if subtract_DC:
            sig_fft = fft(sig,axis=1)
            sig_fft[:,0] = 0
            sig = np.real(ifft(sig_fft))
        ww, tt = np.meshgrid(self.delay_times,w)
        if create_figure:
            plt.figure()
        if color_range == 'auto':
            plt.pcolormesh(ww,tt,sig)
        else:
            plt.pcolormesh(ww,tt,sig,vmin=color_range[0],vmax=color_range[1])
        if draw_colorbar:
            plt.colorbar()
        plt.xlabel('Delay time ($\omega_0^{-1}$)',fontsize=16)
        plt.ylabel('Detection Frequency ($\omega_0$)',fontsize=16)
        if save_fig:
            plt.savefig(self.base_path + 'TA_spectra_iso_ave')
                                    


if __name__=='__main__':
    print(kdelvec('x','x','x','x','x','x'))
    print(kdelvec('x','x','x','x','y','y'))
    print(kdelvec('x','x','x','y','y','y'))
    right = kdelvec('x','x','x','x','y','y')
    left = kdelvec('x','x','x','x','x','x')
    print(left)
    rightprod = I6_mat.dot(right)
    print(rightprod)
    prod = np.dot(left,rightprod)
    print(prod)
