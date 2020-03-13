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
        'CH1_CTLE_MFSR'         :   0xb,
        'CH1_CTLE_HFSR'         :   0xb,
        'CH1_Dis_LPF'           :   0,
        'CH1_Dis_DFF'           :   1,
        'CH1_Disable'           :   0,
        'CH2_CML_AmplSel'       :   0x7,
        'CH2_EQ_ATT'            :   0x3,
        'CH2_Dis_EQ_LF'         :   0,
        'CH2_CTLE_MFSR'         :   0xb,
        'CH2_CTLE_HFSR'         :   0xb,
        'CH2_Dis_LPF'           :   0,
        'CH2_Dis_DFF'           :   1,
        'CH2_Disable'           :   0,
        'CH3_CML_AmplSel'       :   0x7,
        'CH3_EQ_ATT'            :   0x3,
        'CH3_Dis_EQ_LF'         :   0,
        'CH3_CTLE_MFSR'         :   0xb,
        'CH3_CTLE_HFSR'         :   0xb,
        'CH3_Dis_LPF'           :   0,
        'CH3_Dis_DFF'           :   1,
        'CH3_Disable'           :   0,
        'CH4_CML_AmplSel'       :   0x7,
        'CH4_EQ_ATT'            :   0x3,
        'CH4_Dis_EQ_LF'         :   0,
        'CH4_CTLE_MFSR'         :   0xb,
        'CH4_CTLE_HFSR'         :   0xb,
        'CH4_Dis_LPF'           :   0,
        'CH4_Dis_DFF'           :   1,
        'CH4_Disable'           :   0,
        'CH5_CML_AmplSel'       :   0x7,
        'CH5_EQ_ATT'            :   0x3,
        'CH5_Dis_EQ_LF'         :   0,
        'CH5_CTLE_MFSR'         :   0xb,
        'CH5_CTLE_HFSR'         :   0xb,
        'CH5_Dis_LPF'           :   0,
        'CH5_Dis_DFF'           :   1,
        'CH5_Disable'           :   0,
        'CH6_CML_AmplSel'       :   0x7,
        'CH6_EQ_ATT'            :   0x3,
        'CH6_Dis_EQ_LF'         :   0,
        'CH6_CTLE_MFSR'         :   0xb,
        'CH6_CTLE_HFSR'         :   0xb,
        'CH6_Dis_LPF'           :   0,
        'CH6_Dis_DFF'           :   1,
        'CH6_Disable'           :   0,
        'CH7_CML_AmplSel'       :   0x7,
        'CH7_EQ_ATT'            :   0x3,
        'CH7_Dis_EQ_LF'         :   0,
        'CH7_CTLE_MFSR'         :   0xb,
        'CH7_CTLE_HFSR'         :   0xb,
        'CH7_Dis_LPF'           :   0,
        'CH7_Dis_DFF'           :   1,
        'CH7_Disable'           :   0,

        'dllCapReset'           :   0,
        'dllEnable'             :   1,
        'dllChargePumpCurrent'  :   0xf,
        'dllForceDown'          :   0,

        'dllClockDelay_CH7'     :   0x5,
        'dllClockDelay_CH6'     :   0x5,
        'dllClockDelay_CH5'     :   0x5,
        'dllClockDelay_CH4'     :   0x5,
        'dllClockDelay_CH3'     :   0x5,
        'dllClockDelay_CH2'     :   0x5,
        'dllClockDelay_CH1'     :   0x5,
        'dllClockDelay_CH0'     :   0x5,

        'Dis_Tx'                :   0,
        'Rx_Equa'               :   0x0,
        'Rx_invData'            :   0,
        'Rx_enTermination'      :   1,
        'Rx_setCM'              :   1,
        'Rx_Enable'             :   1,

        'Tx1_DL_SR'             :   0x5,
        'Tx1_Dis_DL_Emp'        :   0,
        'Tx1_DL_ATT'            :   0x0,
        'Tx1_Dis_DL_LPF_BIAS'   :   0,
        'Tx1_Dis_DL_BIAS'       :   1,

        'Tx2_DL_SR'             :   0x5,
        'Tx2_Dis_DL_Emp'        :   0,
        'Tx2_DL_ATT'            :   0x0,
        'Tx2_Dis_DL_LPF_BIAS'   :   0,
        'Tx2_Dis_DL_BIAS'       :   1,
        }
    ## @var register map local to the class
    _regMap = {}

    def __init__(self):
        self._regMap = copy.deepcopy(self._defaultRegMap)

    def set_CH1_CML_AmplSel(self, val):
        self._regMap['CH1_CML_AmplSel'] = val & 0x7

    def set_CH1_EQ_ATT(self, val):
        self._regMap['CH1_EQ_ATT'] = val & 0x3

    def set_CH1_Dis_EQ_LF(self, val):
        self._regMap['CH1_Dis_EQ_LF'] = val & 0x1

    def set_CH1_CTLE_MFSR(self, val):
        self._regMap['CH1_CTLE_MFSR'] = val & 0xf

    def set_CH1_CTLE_HFSR(self, val):
        self._regMap['CH1_CTLE_HFSR'] = val & 0xf

    def set_CH1_Dis_LPF(self, val):
        self._regMap['CH1_Dis_LPF'] = val & 0x1

    def set_CH1_Dis_DFF(self, val):
        self._regMap['CH1_Dis_DFF'] = val & 0x1

    def set_CH1_Disable(self, val):
        self._regMap['CH1_Disable'] = val & 0x1

    def set_CH2_CML_AmplSel(self, val):
        self._regMap['CH2_CML_AmplSel'] = val & 0x7

    def set_CH2_EQ_ATT(self, val):
        self._regMap['CH2_EQ_ATT'] = val & 0x3

    def set_CH2_Dis_EQ_LF(self, val):
        self._regMap['CH2_Dis_EQ_LF'] = val & 0x1

    def set_CH2_CTLE_MFSR(self, val):
        self._regMap['CH2_CTLE_MFSR'] = val & 0xf

    def set_CH2_CTLE_HFSR(self, val):
        self._regMap['CH2_CTLE_HFSR'] = val & 0xf

    def set_CH2_Dis_LPF(self, val):
        self._regMap['CH2_Dis_LPF'] = val & 0x1

    def set_CH2_Dis_DFF(self, val):
        self._regMap['CH2_Dis_DFF'] = val & 0x1

    def set_CH2_Disable(self, val):
        self._regMap['CH2_Disable'] = val & 0x1

    def set_CH3_CML_AmplSel(self, val):
        self._regMap['CH3_CML_AmplSel'] = val & 0x7

    def set_CH3_EQ_ATT(self, val):
        self._regMap['CH3_EQ_ATT'] = val & 0x3

    def set_CH3_Dis_EQ_LF(self, val):
        self._regMap['CH3_Dis_EQ_LF'] = val & 0x1

    def set_CH3_CTLE_MFSR(self, val):
        self._regMap['CH3_CTLE_MFSR'] = val & 0xf

    def set_CH3_CTLE_HFSR(self, val):
        self._regMap['CH3_CTLE_HFSR'] = val & 0xf

    def set_CH3_Dis_LPF(self, val):
        self._regMap['CH3_Dis_LPF'] = val & 0x1

    def set_CH3_Dis_DFF(self, val):
        self._regMap['CH3_Dis_DFF'] = val & 0x1

    def set_CH3_Disable(self, val):
        self._regMap['CH3_Disable'] = val & 0x1

    def set_CH4_CML_AmplSel(self, val):
        self._regMap['CH4_CML_AmplSel'] = val & 0x7

    def set_CH4_EQ_ATT(self, val):
        self._regMap['CH4_EQ_ATT'] = val & 0x3

    def set_CH4_Dis_EQ_LF(self, val):
        self._regMap['CH4_Dis_EQ_LF'] = val & 0x1

    def set_CH4_CTLE_MFSR(self, val):
        self._regMap['CH4_CTLE_MFSR'] = val & 0xf

    def set_CH4_CTLE_HFSR(self, val):
        self._regMap['CH4_CTLE_HFSR'] = val & 0xf

    def set_CH4_Dis_LPF(self, val):
        self._regMap['CH4_Dis_LPF'] = val & 0x1

    def set_CH4_Dis_DFF(self, val):
        self._regMap['CH4_Dis_DFF'] = val & 0x1

    def set_CH4_Disable(self, val):
        self._regMap['CH4_Disable'] = val & 0x1

    def set_CH5_CML_AmplSel(self, val):
        self._regMap['CH5_CML_AmplSel'] = val & 0x7

    def set_CH5_EQ_ATT(self, val):
        self._regMap['CH5_EQ_ATT'] = val & 0x3

    def set_CH5_Dis_EQ_LF(self, val):
        self._regMap['CH5_Dis_EQ_LF'] = val & 0x1

    def set_CH5_CTLE_MFSR(self, val):
        self._regMap['CH5_CTLE_MFSR'] = val & 0xf

    def set_CH5_CTLE_HFSR(self, val):
        self._regMap['CH5_CTLE_HFSR'] = val & 0xf

    def set_CH5_Dis_LPF(self, val):
        self._regMap['CH5_Dis_LPF'] = val & 0x1

    def set_CH5_Dis_DFF(self, val):
        self._regMap['CH5_Dis_DFF'] = val & 0x1

    def set_CH5_Disable(self, val):
        self._regMap['CH5_Disable'] = val & 0x1

    def set_CH6_CML_AmplSel(self, val):
        self._regMap['CH6_CML_AmplSel'] = val & 0x7

    def set_CH6_EQ_ATT(self, val):
        self._regMap['CH6_EQ_ATT'] = val & 0x3

    def set_CH6_Dis_EQ_LF(self, val):
        self._regMap['CH6_Dis_EQ_LF'] = val & 0x1

    def set_CH6_CTLE_MFSR(self, val):
        self._regMap['CH6_CTLE_MFSR'] = val & 0xf

    def set_CH6_CTLE_HFSR(self, val):
        self._regMap['CH6_CTLE_HFSR'] = val & 0xf

    def set_CH6_Dis_LPF(self, val):
        self._regMap['CH6_Dis_LPF'] = val & 0x1

    def set_CH6_Dis_DFF(self, val):
        self._regMap['CH6_Dis_DFF'] = val & 0x1

    def set_CH6_Disable(self, val):
        self._regMap['CH6_Disable'] = val & 0x1

    def set_CH7_CML_AmplSel(self, val):
        self._regMap['CH7_CML_AmplSel'] = val & 0x7

    def set_CH7_EQ_ATT(self, val):
        self._regMap['CH7_EQ_ATT'] = val & 0x3

    def set_CH7_Dis_EQ_LF(self, val):
        self._regMap['CH7_Dis_EQ_LF'] = val & 0x1

    def set_CH7_CTLE_MFSR(self, val):
        self._regMap['CH7_CTLE_MFSR'] = val & 0xf

    def set_CH7_CTLE_HFSR(self, val):
        self._regMap['CH7_CTLE_HFSR'] = val & 0xf

    def set_CH7_Dis_LPF(self, val):
        self._regMap['CH7_Dis_LPF'] = val & 0x1

    def set_CH7_Dis_DFF(self, val):
        self._regMap['CH7_Dis_DFF'] = val & 0x1

    def set_CH7_Disable(self, val):
        self._regMap['CH7_Disable'] = val & 0x1

    def set_dllCapReset(self, val):
        self._regMap['dllCapReset'] = val & 0x1

    def set_dllEnable(self, val):
        self._regMap['dllEnable'] = val & 0x1

    def set_dllChargePumpCurrent(self, val):
        self._regMap['dllChargePumpCurrent'] = val & 0xf

    def set_dllForceDown(self, val):
        self._regMap['dllForceDown'] = val & 0x1

    def set_dllClockDelay_CH7(self, val):
        self._regMap['dllClockDelay_CH7'] = val & 0xf

    def set_dllClockDelay_CH6(self, val):
        self._regMap['dllClockDelay_CH6'] = val & 0xf

    def set_dllClockDelay_CH5(self, val):
        self._regMap['dllClockDelay_CH5'] = val & 0xf

    def set_dllClockDelay_CH4(self, val):
        self._regMap['dllClockDelay_CH4'] = val & 0xf

    def set_dllClockDelay_CH3(self, val):
        self._regMap['dllClockDelay_CH3'] = val & 0xf

    def set_dllClockDelay_CH2(self, val):
        self._regMap['dllClockDelay_CH3'] = val & 0xf

    def set_dllClockDelay_CH1(self, val):
        self._regMap['dllClockDelay_CH1'] = val & 0xf

    def set_dllClockDelay_CH0(self, val):
        self._regMap['dllClockDelay_CH0'] = val & 0xf

    def set_Dis_Tx(self, val):
        self._regMap['Dis_Tx'] = val & 0x1

    def set_Rx_Equa(self, val):
        self._regMap['Rx_Equa'] = val & 0x3

    def set_Rx_invData(self, val):
        self._regMap['Rx_invData'] = val & 0x1

    def set_Rx_enTermination(self, val):
        self._regMap['Rx_enTermination'] = val & 0x1

    def set_Rx_setCM(self, val):
        self._regMap['Rx_setCM'] = val & 0x1

    def set_Rx_Enable(self, val):
        self._regMap['Rx_Enable'] = val & 0x1

    def set_Tx1_DL_SR(self, val):
        self._regMap['Tx1_DL_SR'] = val & 0x7

    def set_Tx1_Dis_DL_Emp(self, val):
        self._regMap['Tx1_Dis_DL_Emp'] = val & 0x1

    def set_Tx1_DL_ATT(self, val):
        self._regMap['Tx1_DL_ATT'] = val & 0x3

    def set_Tx1_Dis_DL_LPF_BIAS(self, val):
        self._regMap['Tx1_Dis_DL_LPF_BIAS'] = val & 0x1

    def set_Tx1_Dis_DL_BIAS(self, val):
        self._regMap['Tx1_Dis_DL_BIAS'] = val & 0x1

    def set_Tx2_DL_SR(self, val):
        self._regMap['Tx2_DL_SR'] = val & 0x7

    def set_Tx2_Dis_DL_Emp(self, val):
        self._regMap['Tx2_Dis_DL_Emp'] = val & 0x1

    def set_Tx2_DL_ATT(self, val):
        self._regMap['Tx2_DL_ATT'] = val & 0x3

    def set_Tx2_Dis_DL_LPF_BIAS(self, val):
        self._regMap['Tx2_Dis_DL_LPF_BIAS'] = val & 0x1

    def set_Tx2_Dis_DL_BIAS(self, val):
        self._regMap['Tx2_Dis_DL_BIAS'] = val & 0x1

    ## get I2C register value
    def get_config_vector(self):
        reg_value = []
        reg_value += [self._regMap['CH1_Dis_EQ_LF'] << 5 | self._regMap['CH1_EQ_ATT'] << 3 | self._regMap['CH1_CML_AmplSel']]
        reg_value += [self._regMap['CH1_CTLE_HFSR'] << 4 | self._regMap['CH1_CTLE_MFSR']]
        reg_value += [self._regMap['CH1_Disable'] << 2 | self._regMap['CH1_Dis_DFF'] << 1 | self._regMap['CH1_Dis_LPF']]
        reg_value += [self._regMap['CH2_Dis_EQ_LF'] << 5 | self._regMap['CH2_EQ_ATT'] << 3 | self._regMap['CH2_CML_AmplSel']]
        reg_value += [self._regMap['CH2_CTLE_HFSR'] << 4 | self._regMap['CH2_CTLE_MFSR']]
        reg_value += [self._regMap['CH2_Disable'] << 2 | self._regMap['CH2_Dis_DFF'] << 1 | self._regMap['CH2_Dis_LPF']]
        reg_value += [self._regMap['CH3_Dis_EQ_LF'] << 5 | self._regMap['CH3_EQ_ATT'] << 3 | self._regMap['CH3_CML_AmplSel']]
        reg_value += [self._regMap['CH3_CTLE_HFSR'] << 4 | self._regMap['CH3_CTLE_MFSR']]
        reg_value += [self._regMap['CH3_Disable'] << 2 | self._regMap['CH3_Dis_DFF'] << 1 | self._regMap['CH3_Dis_LPF']]
        reg_value += [self._regMap['CH4_Dis_EQ_LF'] << 5 | self._regMap['CH4_EQ_ATT'] << 3 | self._regMap['CH4_CML_AmplSel']]
        reg_value += [self._regMap['CH4_CTLE_HFSR'] << 4 | self._regMap['CH4_CTLE_MFSR']]
        reg_value += [self._regMap['CH4_Disable'] << 2 | self._regMap['CH4_Dis_DFF'] << 1 | self._regMap['CH4_Dis_LPF']]
        reg_value += [self._regMap['CH5_Dis_EQ_LF'] << 5 | self._regMap['CH5_EQ_ATT'] << 3 | self._regMap['CH5_CML_AmplSel']]
        reg_value += [self._regMap['CH5_CTLE_HFSR'] << 4 | self._regMap['CH5_CTLE_MFSR']]
        reg_value += [self._regMap['CH5_Disable'] << 2 | self._regMap['CH5_Dis_DFF'] << 1 | self._regMap['CH5_Dis_LPF']]
        reg_value += [self._regMap['CH6_Dis_EQ_LF'] << 5 | self._regMap['CH6_EQ_ATT'] << 3 | self._regMap['CH6_CML_AmplSel']]
        reg_value += [self._regMap['CH6_CTLE_HFSR'] << 4 | self._regMap['CH6_CTLE_MFSR']]
        reg_value += [self._regMap['CH6_Disable'] << 2 | self._regMap['CH6_Dis_DFF'] << 1 | self._regMap['CH6_Dis_LPF']]
        reg_value += [self._regMap['CH7_Dis_EQ_LF'] << 5 | self._regMap['CH7_EQ_ATT'] << 3 | self._regMap['CH7_CML_AmplSel']]
        reg_value += [self._regMap['CH7_CTLE_HFSR'] << 4 | self._regMap['CH7_CTLE_MFSR']]
        reg_value += [self._regMap['CH7_Disable'] << 2 | self._regMap['CH7_Dis_DFF'] << 1 | self._regMap['CH7_Dis_LPF']]
        reg_value += [self._regMap['dllEnable'] << 1 | self._regMap['dllCapReset']]
        reg_value += [self._regMap['dllForceDown'] << 4 | self._regMap['dllChargePumpCurrent']]
        reg_value += [self._regMap['dllClockDelay_CH7'] << 4 | self._regMap['dllClockDelay_CH6']]
        reg_value += [self._regMap['dllClockDelay_CH5'] << 4 | self._regMap['dllClockDelay_CH4']]
        reg_value += [self._regMap['dllClockDelay_CH3'] << 4 | self._regMap['dllClockDelay_CH2']]
        reg_value += [self._regMap['dllClockDelay_CH1'] << 4 | self._regMap['dllClockDelay_CH0']]
        reg_value += [self._regMap['Rx_Enable'] << 6 | self._regMap['Rx_setCM'] << 5 | self._regMap['Rx_enTermination'] << 4 | self._regMap['Rx_invData'] << 3 | self._regMap['Rx_Equa'] << 1 | self._regMap['Dis_Tx']]
        reg_value += [self._regMap['Tx1_DL_ATT'] << 4 | self._regMap['Tx1_Dis_DL_Emp'] << 3 | self._regMap['Tx1_DL_SR']]
        reg_value += [self._regMap['Tx1_Dis_DL_BIAS'] << 1 | self._regMap['Tx1_Dis_DL_LPF_BIAS']]
        reg_value += [self._regMap['Tx2_DL_ATT'] << 4 | self._regMap['Tx2_Dis_DL_Emp'] << 3 | self._regMap['Tx2_DL_SR']]
        reg_value += [self._regMap['Tx2_Dis_DL_BIAS'] << 1 | self._regMap['Tx2_Dis_DL_LPF_BIAS']]
        return reg_value
