"""
This is starter code to demonstrate a working example of the Gradient Recalled Echo as a pure Python implementation.
"""
from math import pi

import numpy as np

from pulseq.core.Sequence.sequence import Sequence
from pulseq.core.calc_duration import calc_duration
from pulseq.core.make_adc import makeadc
from pulseq.core.make_delay import make_delay
from pulseq.core.make_sinc import make_sinc_pulse
from pulseq.core.make_trap import make_trapezoid
from pulseq.core.opts import Opts

kwargs_for_opts = {"rf_ring_down_time": 0, "rf_dead_time": 0}
system = Opts(kwargs_for_opts)
seq = Sequence(system)

#####################
fov = 0.32
Nx = 15
Ny = 15
slice_thickness = 0.32/15
flip = 90*pi/180
####################
kwargs_for_sinc = {"flip_angle": flip, "system": system, "duration": 4e-3, "slice_thickness": slice_thickness,
                   "apodization": 0.5, "time_bw_product": 4}
rf, gz = make_sinc_pulse(kwargs_for_sinc, 2)
# plt.plot(rf.t[0], rf.signal[0])
# plt.show()

delta_k = 1 / fov
kWidth = Nx * delta_k
readoutTime = 6.4e-3
kwargs_for_gx = {"channel": 'x', "system": system, "flat_area": kWidth, "flat_time": readoutTime}
gx = make_trapezoid(kwargs_for_gx)
kwargs_for_adc = {"num_samples": Nx, "duration": gx.flat_time, "delay": gx.rise_time}
adc = makeadc(kwargs_for_adc)

kwargs_for_gxpre = {"channel": 'x', "system": system, "area": -gx.area / 2, "duration": 2e-3}
gx_pre = make_trapezoid(kwargs_for_gxpre)
kwargs_for_gz_reph = {"channel": 'z', "system": system, "area": -gz.area / 2, "duration": 2e-3}
gz_reph = make_trapezoid(kwargs_for_gz_reph)
phase_areas = (np.arange(Ny) - (Ny / 2)) * delta_k

#TE, TR = 10e-3, 1000e-3
TE,TR = 0.05, 0.5
delayTE = TE - calc_duration(gx_pre) - calc_duration(gz) / 2 - calc_duration(gx) / 2
delayTR = TR - calc_duration(gx_pre) - calc_duration(gz) - calc_duration(gx) - delayTE
delay1 = make_delay(delayTE)
delay2 = make_delay(delayTR)

for i in range(Ny):
    seq.add_block(rf, gz)
    kwargsForGyPre = {"channel": 'y', "system": system, "area": phase_areas[i], "duration": 2e-3}
    gyPre = make_trapezoid(kwargsForGyPre)
    seq.add_block(gx_pre, gyPre, gz_reph)
    seq.add_block(delay1)
    seq.add_block(gx, adc)
    seq.add_block(delay2)

# The .seq file will be available inside the /gpi/<user>/imr_framework folder
seq.write("gre_python_forsim_15.seq")