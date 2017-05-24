'''Test the optics module.'''

import sys

THEIAPATH = '/home/dev0/theia/theia'    # path to access modules of theia
sys.path.append(THEIAPATH)

from helpers import settings
from helpers.units import *
from optics import beam, beamdump, thinlens, thicklens, mirror

# initialize globals
dic = {'info': True, 'warning': True, 'text': True, 'cad': True,
		'fname': 'test_optics'}

settings.init(dic)

# input data
bd = beamdump.BeamDump()
mr = mirror.Mirror(HRr = .8, HRt = .3, HRK = 1./0.6, ARK = 1./.6,
					Thickness = 1., Diameter = 1.2, N = .9)

mr2 = mirror.Mirror(Diameter = 3., HRK = 1., ARK = 1., Thickness = 5.)
lens = thinlens.ThinLens(Focal = -.5*cm)
lens2 = thicklens.ThickLens()

print mr.lines()
print lens.lines()
print lens2.lines()
print bd.lines()
