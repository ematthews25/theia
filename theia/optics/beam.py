'''Defines the GaussianBeam class for theia.'''

# Provides:
#   class GaussianBeam
#       __init__
#       __str__
#       lineList
#       Q
#       QParam
#       ROC
#       waistPos
#       rayleigh
#       width
#       waistSize
#       gouy


import numpy as np
from helpers.units import *
from helpers import geometry
from helpers.tools import formatter

class GaussianBeam(object):
    '''

    GaussianBeam class.

    This class represents general astigmatic Gaussian beams in 3D space.
    These are the objects that are intended to interact with the optical
    components during the ray tracing and that are rendered in 3D thanks to
    FreeCAD.

    *=== Attributes ===*
    BeamCount: class attribute, counts beams. [integer]
    QTens: general astigmatic complex curvature tensor at the origin.
        [np. array of complex]
    N: Refraction index of the medium in which the beam is placed. [float]
    Wl: Wave-length in vacuum of the beam (frequency never changes). [float]
    P: Power of the beam. [float]
    Pos: Position in 3D space of the origin of the beam. [3D vector]
    Dir: Normalized direction in 3D space of the beam axis. [3D vector]
    U: A tuple of unitary vectors which along with Dir form a direct orthonormal
        basis in which the Q tensor is expressed. [tuple of 3D vectors]
    Name: Name of the beam if any. [string]
    Ref: Reference to the beam. [string]
    OptDist: Optical length. [float]
    Length: Geometrical length of the beam. [float]
    StrayOrder: Number representing the *strayness* of the beam. If the beams
        results from a transmission on a HR surface or a reflection on a AR
        surface, then its StrayOrder is the StrayOrder of the parent beam + 1.
        [integer]
    Optic: Ref of optic where the beam departs from (None if laser). [string]
    Face: face of the optic where the beam departs from. [string]

    '''
    BeamCount = 0   # counts beams

    def __init__(self, Wx = None, Wy = None, WDistx = 0., WDisty = 0.,
        Pos = None,
        Q = None, ortho = True, N = 1., Theta = np.pi/2., Phi = None, Alpha = 0.,
        Wl = 1064.*nm, P = 1*W, X = 0., Y = 0., Z = 0., Dir = [1., 0., 0.],
        Ux = None, Uy = None, Name = None, Ref = None, OptDist = 0.*m,
        Length = 0.*m, StrayOrder = 0, Optic = None, Face = None):
        '''Beam constructor.

        This constructor allows to construct *orthogonal* Gaussian beams if the
        ortho parameter is True, or a general astigmatic beam if it is False.
        If ortho is True, a pair of waists and waist distances has to be given
        and the corresponding orthogonal beam is returned.
        If it is False a general tensor attribute can directly be given.

        The Ux vector which is input is the second of the orthonormal basis.

        Returns a Gaussian beam with attributes as the parameters.

        '''

        # external params
        self.N = float(N)
        self.Wl = float(Wl)
        self.P = float(P)
        self.OptDist = float(OptDist)
        self.Length = float(Length)
        self.StrayOrder = StrayOrder

        # name
        if Name is not None:
            self.Name = Name
        else:
            self.Name = 'Beam' + str(self.__class__.BeamCount)

        if Ref is not None:
            self.Ref = Ref
        else:
            self.Ref = 'Beam' + str(self.__class__.BeamCount)

        if Pos is not None:
            self.Pos = np.array(Pos, dtype = np.float64)
        else:
            self.Pos = np.array([X, Y, Z], dtype=np.float64)


        if Theta is not None and Phi is not None:
            self.Dir = np.array([np.sin(Theta) * np.cos(Phi),
                            np.sin(Theta) * np.sin(Phi),
                            np.cos(Theta)], dtype = np.float64)
        else:
            self.Dir = np.array(Dir, dtype=np.float64)
            self.Dir = self.Dir/np.linalg.norm(self.Dir)

        # orthonormal basis in which Q is expressed
        if Ux is None and Uy is None:
            #ths happens when alpha is given, user input
            Alpha = float(Alpha)
            (u1,v1) = geometry.basis(self.Dir)
            v = np.cos(Alpha)*v1 - np.sin(Alpha)*u1
            u = np.cos(Alpha)*u1 + np.sin(Alpha)*v1
        elif Ux is not None and Uy is None:
            u = np.array(Ux, dtype = np.float64)
            u = u/np.linalg.norm(Ux)
            v = np.cross(self.Dir, u)
        elif Ux is None and Uy is not None:
            v = np.array(Uy, dtype = np.float64)
            v = v/np.linalg.norm(v)
            u = np.cross(v, self.Dir)
        elif Ux is not None and Uy is not None:
            # this happens when we know u and v, only internal use basically
            u = np.array(Ux, dtype = np.float64)
            v = np.array(Uy, dtype = np.float64)
            u = u/np.linalg.norm(u)
            v = v/np.linalg.norm(v)

        self.U = (u, v)


        # curvature tensor
        if ortho:
            lam = self.Wl/N
            Wx = float(Wx)
            Wy = float(Wy)
            qx = complex(- float(WDistx)  + 1.j * np.pi*Wx**2./lam )
            qy = complex(- float(WDisty)  + 1.j * np.pi*Wy**2./lam )
            # Q tensor for orthogonal beam
            self.QTens = np.array([[1./qx, 0.],[0., 1./qy]],
                        dtype = np.complex64)
        elif not ortho:
            self.QTens = Q

        #origin optics
        self.Optic = Optic
        self.Face = Face

        self.__class__.BeamCount = self.__class__.BeamCount + 1

    def __str__(self):
        '''String representation of the beam, when calling print(beam).

        '''
        return formatter(self.lines())

    def lines(self):
        '''Returns the list of lines necessary to print the object.

        '''
        ans = []
        ans.append("Beam: " + self.Name + " (" + self.Ref + ") " + "{")
        ans.append("Power: " + str(self.P) + "W/"\
        +"Index: " + str(self.N)\
        +"/Wavelength: "+str(self.Wl/nm)+"nm/Length: " + str(self.Length) + "m")
        ans.append("Order: " + str(self.StrayOrder))
        ans.append("Origin: " + str(self.Pos))

        sph = geometry.rectToSph(self.Dir)
        ans.append("Direction: (" + str(sph[0]/deg) + ', ' \
                + str(sph[1]/deg) + ')deg')

        sphx = geometry.rectToSph(self.U[0])
        ans.append("Ux: (" + str(sphx[0]/deg) + ', ' \
                + str(sphx[1]/deg) + ')deg')

        sphy = geometry.rectToSph(self.U[1])
        ans.append("Uy: (" + str(sphy[0]/deg) + ', ' \
                + str(sphy[1]/deg) + ')deg')
        ans.append("Waist Pos: " + str(self.waistPos()) + 'm')
        ans.append("Waist Size: (" \
            + str(self.waistSize()[0]/mm) + ', ' + str(self.waistSize()[1]/mm)\
            + ')mm')
        ans.append("Rayleigh: " + str(self.rayleigh()) + "m")
        ans.append("ROC: " + str(self.ROC()))
        ans.append("}")

        return ans


    def Q(self, d = 0.):
        '''Return the Q tensor at a distance d of origin.

        '''
        d = float(d)
        I = np.array([[1., 0.], [0., 1.]], dtype=np.float64)
        return np.matmul(np.linalg.inv(I + d * self.QTens),self.QTens)

    def QParam(self, d = 0.):
        '''Compute the complex parameters q1 and q2 and theta of beam.

            Returns a dictionary with keys:
            '1': q1 [complex]
            '2': q2 [complex]
            'theta': theta [float]
        '''
        d = float(d)

        a = self.Q(d)[0][0]
        b = self.Q(d)[0][1]
        d = self.Q(d)[1][1]

        q1inv = .5*(a + d + np.sqrt((a - d)**2. + 4.*b**2.))
        q2inv = .5*(a + d - np.sqrt((a - d)**2. + 4.*b**2.))

        if q1inv == q2inv:
            theta = 0.
        else:
            theta = .5*np.arcsin(2.*b/(q1inv - q2inv))

        try:
            a = 1/q1inv
        except ZeroDivisionError:
            a = np.inf
        try:
            b = 1/q2inv
        except ZeroDivisionError:
            b = np.inf
        return {'1': a, '2': b, 'theta':theta}

    def ROC(self, dist = 0.):
        '''Return the tuple of ROC of the beam.

        '''
        dist = float(dist)
        Q = self.QParam(dist)
        try:
            a = 1./np.real(1./Q['1'])
        except FloatingPointError:
            a = np.inf
        try:
            b = 1./np.real(1./Q['2'])
        except FloatingPointError:
            b = np.inf

        return  (a, b)

    def waistPos(self):
        '''Return the tuple of positions of the waists of the beam along Dir.

        '''
        Q = self.QParam(0.)
        return (-np.real(Q['1']), -np.real(Q['2']))

    def rayleigh(self):
        '''Return the tuple of Rayleigh ranges of the beam.

        '''
        Q = self.QParam()
        return (np.abs(np.imag(Q['1'])), np.abs(np.imag(Q['2'])))

    def width(self, d = 0.):
        '''Return the tuple of beam widths.

        '''
        d = float(d)
        lam = self.Wl/self.N
        zR = self.rayleigh()
        D = self.waistPos()

        return (np.sqrt((lam/np.pi)*((d - D[0])**2. + zR[0]**2.)/zR[0]) ,
                np.sqrt((lam/np.pi)*((d - D[1])**2. + zR[1]**2.)/zR[1]))

    def waistSize(self):
        '''Return a tuple with the waist sizes in x and y.

        '''
        pos = self.waistPos()
        return (self.width(pos[0])[0], self.width(pos[1])[1] )

    def gouy(self, d = 0.):
        '''Return the tuple of Gouy phases.

        '''
        d = float(d)
        zR = self.rayleigh()
        WDist = self.waistPos()
        return (np.arctan((d-WDist[0])/zR[0]),
                np.arctan((d-WDist[1])/zR[1]))
