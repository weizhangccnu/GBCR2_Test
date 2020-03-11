#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Wei Zhang
@date: 2019-12-11
ETROC1 TDC Test Block class
'''
#--------------------------------------------------------------------------#
## Manage GBCR2 chip's internal registers map
# Allow combining and disassembling individual registers
class GBCR2_Reg(object):
    ## @var _defaultRegMap default register values
    _defaultRegMap = {
        'CH1_CML_AmplSel'       :   0x7,
        'CH1_EQ_ATT'            :   0x3,
        'CH1_Dis_EQ_LF'         :   0,
        'CH1_CTLE_MFSR'         :   0xa,
        'CH1_CTLE_HFSR'         :   0xa,
        'CH1_Dis_LPF'           :   0,
        'CH1_Dis_DFF'           :   1,
        'CH1_Disable'           :   0,
        'CH2_CML_AmplSel'       :   0x7,
        'CH2_EQ_ATT'            :   0x3,
        'CH2_Dis_EQ_LF'         :   0,
        'CH2_CTLE_MFSR'         :   0xa,
        'CH2_CTLE_HFSR'         :   0xa,
        'CH2_Dis_LPF'           :   0,
        'CH2_Dis_DFF'           :   1,
        'CH2_Disable'           :   0,
        'CH3_CML_AmplSel'       :   0x7,
        'CH3_EQ_ATT'            :   0x3,
        'CH3_Dis_EQ_LF'         :   0,
        'CH3_CTLE_MFSR'         :   0xa,
        'CH3_CTLE_HFSR'         :   0xa,
        'CH3_Dis_LPF'           :   0,
        'CH3_Dis_DFF'           :   1,
        'CH3_Disable'           :   0,
        'CH4_CML_AmplSel'       :   0x7,
        'CH4_EQ_ATT'            :   0x3,
        'CH4_Dis_EQ_LF'         :   0,
        'CH4_CTLE_MFSR'         :   0xa,
        'CH4_CTLE_HFSR'         :   0xa,
        'CH4_Dis_LPF'           :   0,
        'CH4_Dis_DFF'           :   1,
        'CH4_Disable'           :   0,
        'CH5_CML_AmplSel'       :   0x7,
        'CH5_EQ_ATT'            :   0x3,
        'CH5_Dis_EQ_LF'         :   0,
        'CH5_CTLE_MFSR'         :   0xa,
        'CH5_CTLE_HFSR'         :   0xa,
        'CH5_Dis_LPF'           :   0,
        'CH5_Dis_DFF'           :   1,
        'CH5_Disable'           :   0,
        'CH6_CML_AmplSel'       :   0x7,
        'CH6_EQ_ATT'            :   0x3,
        'CH6_Dis_EQ_LF'         :   0,
        'CH6_CTLE_MFSR'         :   0xa,
        'CH6_CTLE_HFSR'         :   0xa,
        'CH6_Dis_LPF'           :   0,
        'CH6_Dis_DFF'           :   1,
        'CH6_Disable'           :   0,
        'CH7_CML_AmplSel'       :   0x7,
        'CH7_EQ_ATT'            :   0x3,
        'CH7_Dis_EQ_LF'         :   0,
        'CH7_CTLE_MFSR'         :   0xa,
        'CH7_CTLE_HFSR'         :   0xa,
        'CH7_Dis_LPF'           :   0,
        'CH7_Dis_DFF'           :   1,
        'CH7_Disable'           :   0,

        }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [self._regMap['GROout_AmplSel'] << 1 | self._regMap['GROout_disCMLDriverBIAS']]
        return reg_value

