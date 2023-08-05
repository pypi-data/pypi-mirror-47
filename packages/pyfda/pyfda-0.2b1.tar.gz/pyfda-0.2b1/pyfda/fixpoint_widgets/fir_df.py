# -*- coding: utf-8 -*-
#
# This file is part of the pyFDA project hosted at https://github.com/chipmuenk/pyfda
#
# Copyright © pyFDA Project Contributors
# Licensed under the terms of the MIT License
# (see file LICENSE in root directory for details)

"""
Widget for specifying the parameters of a direct-form DF1 FIR filter
"""
import sys
import logging
logger = logging.getLogger(__name__)

import pyfda.filterbroker as fb

from ..compat import QWidget, QVBoxLayout

#import pyfda.pyfda_fix_lib as fx
from .fixpoint_helpers import UI_W, UI_W_coeffs, UI_Q, UI_Q_coeffs

#####################
from functools import reduce
from operator import add

from math import cos, pi
#from scipy import signal

from migen import Signal, Module, run_simulation
from migen.fhdl import verilog
################################

classes = {'FIR_DF':'DF'} #: Dict containing widget class name : display name

# =============================================================================

class FIR_DF(QWidget):
    """
    Widget for entering word formats & quantization, also instantiates fixpoint
    filter class :class:`FilterFIR`.
    """
    def __init__(self, parent):
        super(FIR_DF, self).__init__(parent)

        self.title = ("<b>Direct-Form (DF) FIR Filter</b><br />"
                      "Standard FIR topology.")
        self.img_name = "fir_df.png"

        self._construct_UI()
        # Construct an instance of the HDL filter object
        self.construct_hdlfilter() # construct instance self.hdlfilter with dummy data
#------------------------------------------------------------------------------

    def _construct_UI(self):
        """
        Intitialize the UI with widgets for coefficient format and input and 
        output quantization
        """
        self.wdg_w_coeffs = UI_W_coeffs(self, label='Coefficient Format:', enabled=False,
                                        tip_WI='Number of integer bits - edit in the "b,a" tab',
                                        tip_WF='Number of fractional bits - edit in the "b,a" tab',
                                        WI = fb.fil[0]['q_coeff']['WI'],
                                        WF = fb.fil[0]['q_coeff']['WF'])
        self.wdg_q_coeffs = UI_Q_coeffs(self, enabled=False,
                                        cur_ov=fb.fil[0]['q_coeff']['ovfl'], 
                                        cur_q=fb.fil[0]['q_coeff']['quant'])
        self.wdg_w_accu = UI_W(self, label='Accumulator Format <i>Q<sub>A </sub></i>:', WF=30)
        self.wdg_q_accu = UI_Q(self)
#------------------------------------------------------------------------------

        layVWdg = QVBoxLayout()
        layVWdg.setContentsMargins(0,0,0,0)
        
        layVWdg.addWidget(self.wdg_w_coeffs)
        layVWdg.addWidget(self.wdg_q_coeffs)

        layVWdg.addWidget(self.wdg_w_accu)
        layVWdg.addWidget(self.wdg_q_accu)

        layVWdg.addStretch()

        self.setLayout(layVWdg)
        
#------------------------------------------------------------------------------
    def dict2ui(self, fxqc_dict):
        """
        Update all parts of the UI that need to be updated when specs have been
        changed outside this class, e.g. coefficients and coefficient wordlength.
        This also provides the initial setting for the widgets when the filter has
        been changed.

        This is called from one level above by 
        :class:`pyfda.input_widgets.input_fixpoint_specs.Input_Fixpoint_Specs`.
        """
        if not 'QA' in fxqc_dict:
            fxqc_dict.update({'QA':{}}) # no accumulator settings in dict yet 
            
        if not 'QC' in fxqc_dict:
            fxqc_dict.update({'QC':{}}) # no coefficient settings in dict yet 
            
        self.wdg_w_coeffs.dict2ui(fxqc_dict['QC']) # update coefficient wordlength
        self.wdg_q_coeffs.dict2ui(fxqc_dict['QC']) # update coefficient quantization settings
        
        self.wdg_w_accu.dict2ui(fxqc_dict['QA'])
        
#------------------------------------------------------------------------------
    def ui2dict(self):
        """
        Read out the subwidgets and return a dict with their settings
        
        Return a dictionary with infos for the fixpoint implementation
        concerning coefficients and their quantization format.
        
        This dictionary is merged with the input and output quantization settings
        that are entered in ``input_fixpoint_specs``.

        
        Parameters
        ----------
        
        None
        
        Returns
        -------
        fxqc_dict : dict

           containing the following keys:

               :'QC': dictionary with coefficients quantization settings
                
        """
        fxqc_dict = {}    
        fxqc_dict.update({'QC':self.wdg_w_coeffs.c_dict})
        
        fxqc_dict.update({'QA': self.wdg_w_accu.ui2dict()})
        
        return fxqc_dict
    
#------------------------------------------------------------------------------
    def construct_hdlfilter(self, fxqc_dict=None):
        """
        Construct an instance of the HDL filter object using the settings from
        the quantizer dict
        """
        # TODO: This is clumsy, dict should contain all keys by default
        if not fxqc_dict:
            fxqc_dict = {'QI':{'W':16}, 'QC':{'b':[18,3,0,-3,-18]}, 
                         'QO':{'W':16}, 'QA':{'W':16}} # create dummy dict

        self.hdlfilter = FIR(fxqc_dict) # construct HDL filter instance
#------------------------------------------------------------------------------
    def get_response(self):
        """
        Return filter output.

        Returns
        -------
        response(numpy int array) : returns filter output as numpy array
        """
        return self.response

#------------------------------------------------------------------------------
    def to_verilog(self, fxqc_dict):
        """
        Convert the HDL description to Verilog
        """
        return verilog.convert(self.hdlfilter,
                               ios={self.hdlfilter.i, self.hdlfilter.o}) 

    def fir_tb_stim(self, stimulus, inputs, outputs):
        """ use stimulus list from widget as input to filter """
        for x in stimulus:
            yield self.hdlfilter.i.eq(int(x)) # pass one stimulus value to filter
            inputs.append(x) # and append it to input list
            outputs.append((yield self.hdlfilter.o)) # append filter output to output list
            yield # ??


    def fir_tb_sin(self, stimulus, inputs, outputs):
        """ sinusoidal test signal """
        f = 2**(self.hdlfilter.wsize - 1)
        for t in range(len(stimulus)):
            v = 0.1*cos(2*pi*0.1*t)
            yield self.hdlfilter.i.eq(int(f*v))
            inputs.append(v)
            outputs.append((yield self.hdlfilter.o))
            yield

#------------------------------------------------------------------------------           
    def run_sim(self, stimulus):
        """
        Pass stimuli and run filter simulation, see 
        https://reconfig.io/2018/05/hello_world_migen
        https://github.com/m-labs/migen/blob/master/examples/sim/fir.py        
        """
        inputs = []
        response = []
        
        testbench = self.fir_tb_stim(stimulus, inputs, response) 
            
        run_simulation(self.hdlfilter, testbench)
        
        return response
###############################################################################
# A synthesizable FIR filter.
class FIR(Module):
    def __init__(self, fxqc_dict):
        logger.debug(fxqc_dict)
        if 'QC' in fxqc_dict and 'W' in fxqc_dict['QC']: # coeff. format  
            self.wsize_c = fxqc_dict['QC']['W']
        else:
            self.wsize_c = 16
            logger.warning("Key 'fxqc_dict['QC']['W']' undefined, using default value.")
        self.coef    = fxqc_dict['QC']['b'] # list with coefficients
        self.wsize_i = fxqc_dict['QI']['W'] # input format
        self.wsize_o = fxqc_dict['QO']['W'] # output format
        self.wsize_a = fxqc_dict['QA']['W'] # accumulator format
        
        self.i = Signal((self.wsize_i, True)) # input signal
        self.o = Signal((self.wsize_o, True)) # output signal
        self.response = []

        ###
        muls = []
        src = self.i
        for c in self.coef:
            sreg = Signal((self.wsize_i, True)) # registers for input signal 
            self.sync += sreg.eq(src)
            src = sreg
            muls.append(c*sreg)
        sum_full = Signal((self.wsize_a, True))
        self.sync += sum_full.eq(reduce(add, muls)) # sum of multiplication products
        self.comb += self.o.eq(sum_full >> (self.wsize_a-self.wsize_o)) # rescale for output width

#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = FIR_DF(None)
    mainw.show()

    app.exec_()
    
    # test using "python -m pyfda.fixpoint_widgets.fir_df_migen"