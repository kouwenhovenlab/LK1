from importlib import reload

import qcodes as qc
import broadbean as bb
from pytopo.qctools import instruments as instools
from pytopo.qctools.instruments import create_inst, add2station

from init_station import *

# set some station configuration variables
qc.config['user']['instruments'] = {
    'awg_name' : 'awg',
    'alazar_name' : 'alazar',
    'default_acquisition_controller' : 'post_iq_acq',
    }


# init instruments lives in a function (to be able to import without loading instruments.)
def init_instruments():
    inst_list = []

    # Create all instruments

    # create and setup Alazar
    from qcodes.instrument_drivers.AlazarTech import utils
    from qcodes.instrument_drivers.AlazarTech.ATS9870 import AlazarTech_ATS9870
    alazar = instools.create_inst(AlazarTech_ATS9870, 'alazar', force_new_instance=True)
    inst_list.append(alazar)

    from pytopo.rf.alazar import acquisition_tools
    acquisition_tools.simple_alazar_setup_ext_trigger(256, 1, 1)
    
    # create and setup AWG
    from qcodes.instrument_drivers.tektronix.AWG5014 import Tektronix_AWG5014
    awg = instools.create_inst(
        Tektronix_AWG5014, 'awg', 
        address='TCPIP0::169.254.193.163::inst0::INSTR',
        force_new_instance=True)
    inst_list.append(awg)

    # RF sources
    from qcodes.instrument_drivers.rohde_schwarz.SGS100A import RohdeSchwarz_SGS100A
    LO = instools.create_inst(RohdeSchwarz_SGS100A, 'LO', address="TCPIP0::169.254.2.20", force_new_instance=True)
    inst_list.append(LO)
    
    TWPA = instools.create_inst(RohdeSchwarz_SGS100A, 'TWPA', address="TCPIP0::169.254.238.193", force_new_instance=True)
    inst_list.append(TWPA)

    RF = instools.create_inst(RohdeSchwarz_SGS100A, 'RF', address="TCPIP0::169.254.248.54", force_new_instance=True)
    inst_list.append(RF)


    from qcodes.instrument_drivers.agilent.E8267C import E8267
    qubsrc = instools.create_inst(E8267, 'qubsrc', address='GPIB0::19::INSTR', force_new_instance=True)
    inst_list.append(qubsrc)

    from pytopo.rf.sources import HeterodyneSource
    hetsrc = instools.create_inst(HeterodyneSource, 'hetsrc', RF=RF, LO=LO, force_new_instance=True)
    inst_list.append(hetsrc)
    
    from qcodes.instrument_drivers.oxford.MercuryiPS_VISA import MercuryiPS
    mgnt = create_inst(MercuryiPS, 'mgnt', address='TCPIP0::169.254.111.112::7020::SOCKET', force_new_instance=True)
    inst_list.append(mgnt)
    


    # done
    station = qc.Station(*inst_list)
    return station

# Execute the script to load all instruments
if __name__ == '__main__':
    station = init_instruments()
