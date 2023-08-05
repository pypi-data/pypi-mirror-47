"""
The utils module provides tools for diffusion data processing and analysis.
"""

import numpy as np
from scipy.interpolate import splev, splrep
from pydiffusion.core import DiffProfile, DiffSystem


def mesh(start=0, end=500, n=200, a=0):
    """
    Meshing for diffusion grids

    Parameters
    ----------
    start, end : float
        Start & end location for diffusion grids.
    n : int
        Grid number of meshing.
    a : float
        Parameter for nonlinear meshing.
        = 0 : Linear meshing with equal grid size.
        > 0 : Nonlinear meshing with increasing grid size.
        < 0 : Nonlinear meshing with decreasing grid size.

    Returns
    -------
    dis : numpy.array
        Meshed grids information.

    Examples
    --------
    Create a meshed 400 grids in 1000 microns with increasing grid sizes:

    >>> dis = mesh(0, 1000, n=400, a=0.5)

    """
    if a == 0:
        dis = np.linspace(start, end, n)
    elif a > 0:
        dis = np.array([start+(end-start)*np.sinh(i*a/(n-1))/np.sinh(a) for i in range(n)])
    else:
        dis = np.array([end-(end-start)*np.sinh(i*a/(1-n))/np.sinh(-a) for i in range(n-1, -1, -1)])
    d = dis[1:]-dis[:-1]
    print('Meshing completed. Grid min=%.3f, max=%.3f' % (min(d), max(d)))
    return dis


def meshfunc_default(x, alpha=0.3):
    """
    Default meshing size vs. DC function in automesh()

    """
    return x**alpha


def automesh(profile, diffsys, n=[400, 500], f=None, alpha=0.3):
    """
    Meshing for fast simulation similar to existing profile.
    This is usually used for a fast and accurate simulation of difficult systems.

    Parameters
    ----------
    profile : DiffProfile
        The profile meshing is based on. It should be similar to final
        simulated profile. e.g. Smoothed experimental profile.
    diffsys : DiffSystem
        The diffusion coefficients for simulation.
    n : list
        meshing number range, default = [400, 500]
    f : function of meshing
        Meshing grid size is proportional to f(DC), default = DC**alpha
        DC is diffusion coefficients.
    alpha : float
        argument of meshfunc_default

    Returns
    -------
    dism: numpy.array
        Distance information after meshing.

    Examples
    --------
    Create an efficient meshing grids with known diffusion profile (profile)
    and diffusion coefficients (dsys). Grid number is about 500~600:

    >>> dis = automesh(profile, dsys, [500, 600])

    In FSA, profile is the smoothed profile from experimental data.
    If profile is unknown, you can simulate one with mphSim() before automesh().

    To perform an accurate simulation on a 600 micron grid, with known diffusion
    coefficients (dsys) and simulation time (100 hours):

    >>> dis = mesh(0, 600, 300)
    >>> init_profile = step(dis, 300, dsys)
    >>> profile = mphSim(init_profile, dsys, time=3600*100)
    >>> dis = automesh(profile, dsys)

    Then use new grids to perform accurate simulation:

    >>> init_profile = step(dis, 300, dsys)
    >>> profile = mphSim(init_profile, dsys, time=3600*100)

    """
    dis, X = profile.dis, profile.X
    Xr, fD = diffsys.Xr, diffsys.Dfunc
    nmin, nmax = n
    dmin = dis[-1]/nmax/2

    if f is None:
        def f(x):
            return meshfunc_default(x, alpha)

    # Create profile function fX
    fX = profilefunc(profile)

    # Create universal D function fDC
    Xf, Df = np.array([]), np.array([])
    for i in range(len(fD)):
        Xnew = np.linspace(Xr[i, 0], Xr[i, 1], 20)
        Xf = np.append(Xf, Xnew)
        Df = np.append(Df, np.exp(splev(Xnew, fD[i])))
    fDC = splrep(Xf, np.log(Df), k=1)

    # Meshing
    while True:
        dism = [dis[0]]
        dseed = dmin/min(f(np.exp(splev(X, fDC))))
        while dism[-1] < dis[-1]:
            disDC = np.exp(splev(splev(dism[-1], fX), fDC))
            dnew = dmin if disDC < 1e-17 else dseed*f(disDC)
            dism += [dism[-1]+dnew]
        dism += [dis[-1]+dnew]
        meshnum = len(dism)
        if meshnum < nmin:
            dmin /= 2
        elif meshnum < nmax:
            break
        else:
            dmin *= 1.1
    print('Meshing Num=%i, Minimum grid=%f um' % (meshnum, dmin))
    return np.array(dism)


def step(dis, matano, diffsys, Xlim=[], name=''):
    """
    Create a step profile at the Matano Plane.

    Parameters
    ----------
    dis : numpy.array
        Distance information.
    matano : float
        Matano plane location (micron).
    diffsys : DiffSystem
        The diffusion system information for initial setups before simulation.
    Xlim : list (float), optional
        Indicates the left and right concentration limits for step profile.
        Default value = [diffsys.Xr[0][0], diffsys.Xr[-1][1]].
    name : str, optional
        Name the output DiffProfile

    Returns
    -------
    profile : DiffProfile
        Step profile can be used for input of pydiffusion.simulation.mphSim

    Examples
    --------
    Create a step profile on a meshed grid:

    >>> dis = mesh()
    >>> init_profile = step(dis, 200, dsys, Xlim=[0, 1])

    """
    Np = diffsys.Np
    if Xlim == []:
        XL, XR = diffsys.Xr[0][0], diffsys.Xr[-1][1]
    else:
        [XL, XR] = Xlim
    X = np.ones(len(dis))*XL
    X[dis > matano] = XR
    if name == '':
        name = diffsys.name+'_step'
    if Np == 1:
        return DiffProfile(dis, X, name=name)
    else:
        If = [0]*(Np-1)
        Ip = np.where(X == XR)[0][0]
        d = dis[Ip] - dis[Ip-1]
        for i in range(Np-1):
            If[i] = dis[Ip-1] + d/(Np+1)*(i+1)
        return DiffProfile(dis, X, If, name=name)


def profilefunc(profile):
    "Create a tck interpolation (k=1) of the diffusion profile"
    disn, Xn = profile.dis.copy(), profile.X.copy()
    for i in range(len(disn)-1):
        if disn[i] == disn[i+1]:
            disn[i] -= (disn[i]-disn[i-1])/1e5
            disn[i+1] += (disn[i+2]-disn[i+1])/1e5
    return splrep(disn, Xn, k=1)


def disfunc(dis, X):
    "Create a tck interpolation (k=1) of the dis vs. X profile"
    Xmin, Xmax = (X[0], X[-1]) if X[0] < X[-1] else (X[-1], X[0])
    if list(X).count(Xmin) > 1 and list(X).count(Xmax) > 1:
        pid = np.where((X > Xmin) & (X < Xmax))[0]
    elif list(X).count(Xmin) > 1:
        pid = np.where((X > Xmin))[0]
    elif list(X).count(Xmax) > 1:
        pid = np.where((X < Xmax))[0]
    else:
        pid = np.arange(len(X))
    if X[-1] < X[0]:
        pid = pid[::-1]
    return splrep(X[pid], dis[pid], k=1)


def matanocalc(profile, Xlim=[]):
    """
    Matano Plane calculation.

    Parameters
    ----------
    profile : DiffProfile
        Diffusion Profile.
    Xlim : list
        The left and right end concentration of the profile.

    Returns
    -------
    matano : float
        Matano Plane location.
    """
    dis, X = profile.dis, profile.X
    if Xlim == []:
        XL, XR = X[0], X[-1]
    elif isinstance(Xlim, list) and len(Xlim) == 2:
        XL, XR = Xlim
    else:
        raise ValueError('Xlim is a list with length = 2')
    return (np.trapz(X, dis)-dis[-1]*XR+dis[0]*XL)/(XL-XR)


def SF(profile, time, Xlim=[]):
    """
    Use Sauer-Freise method to calculate diffusion coefficients from profile.

    Parameters
    ----------
    profile : DiffProfile
        Diffusion profile.
    time : float
        Diffusion time in seconds.
    Xlim : list (float), optional
        Indicates the left and right concentration limits for calculation.
        Default value = [profile.X[0], profile.X[-1]].

    Returns
    -------
    DC : numpy.array
        Diffusion coefficients.
    """
    try:
        time = float(time)
    except TypeError:
        print('Cannot convert time to float')

    dis, X = profile.dis, profile.X
    [XL, XR] = [X[0], X[-1]] if Xlim == [] else Xlim
    Y1 = (X-XL)/(XR-XL)
    Y2 = 1-Y1
    dYds = (Y1[2:]-Y1[:-2])/(dis[2:]-dis[:-2])
    dYds = np.append(dYds[0], np.append(dYds, dYds[-1]))
    intvalue = np.array([Y2[i]*np.trapz(Y1[:i+1], dis[:i+1])+Y1[i]*(np.trapz(Y2[i:], dis[i:])) for i in range(len(dis))])
    DC = intvalue/dYds/2/time*1e-12
    DC[0], DC[-1] = DC[1], DC[-2]
    return DC


def check_mono(dis, X):
    """
    Check the monotonicity of a profile.
    Return True if profile is monotonic.

    Parameters
    ----------
    dis : Distance data
    X : Concentration data
    """
    if X[-1] < X[0]:
        X = 1-X
    ip = np.where(X[1:] < X[:-1])[0]
    if len(ip) == 0:
        return True
    else:
        d1, d2 = dis[ip[0]], dis[ip[-1]+1]
        print('Non-monotonicity found between %.2f and %.2f micron!' % (d1, d2))
        return False


def error_profile(profilesim, profileexp, w=None):
    """
    Calculate the difference (in mole fraction) between experimental profile
    and simulated profile. This function take profilesim as reference, i.e.
    compare profileexp against profilesim.

    Parameters
    ----------
    profilesim : DiffProfile
        Simulated diffusion profile.
    profileexp : DiffProfile
        Experiemntal measured profile.
    w : list, optional
        Weights of each phase, default is equal weights.

    Returns
    -------
    error : float
        Averaged difference in mole fraction.
    """
    fX = profilefunc(profilesim)
    dissim, Xsim = profilesim.dis, profilesim.X
    disexp, Xexp = profileexp.dis, profileexp.X
    If = []
    for i in range(len(dissim)-1):
        if dissim[i] == dissim[i+1]:
            If += [dissim[i]]
    Np = len(If)+1
    if w is not None and len(w) != Np:
        raise ValueError('Length of w must equal to number of phases.')
    if w is None:
        w = [1]*Np
    If += [disexp[-1]+1]
    error, n = 0, 0
    for i in range(len(disexp)):
        for j in range(Np):
            if disexp[i] < If[j]:
                wi = w[j]
                break
        n += wi
        if disexp[i] < dissim[0]:
            error += abs(Xexp[i]-Xsim[0])*wi
        elif disexp[i] > dissim[-1]:
            error += abs(Xexp[i]-Xsim[-1])*wi
        else:
            error += abs(Xexp[i]-splev(disexp[i], fX))*wi
    return error / n


def efunc_default(X, Xf, r):
    "Default efunc to create bias for diffusion coefficients"
    if abs(Xf-X) <= r/2:
        deltae = 1-2*(X-Xf)**2/r**2
    elif Xf < X-r/2:
        deltae = 2*(Xf-X+r)**2/r**2
    else:
        deltae = 2*(Xf-X-r)**2/r**2
    return deltae


def DCbias(diffsys, X, deltaD, r=0.3, efunc=None):
    """
    This function creates bias for a diffusion coefficients profile

    Parameters
    ----------
    diffsys : DiffSystem
        Original diffusion coefficients.
    X : float
        Concentration location which has largest bias.
    deltaD : float
        Scale of the bias. D *= 10**deltaD is the maximum of bias.
    r : float, optional
        Bias at X will create smaller bias in range of (X-r, X+r)
    efunc : function, optional
        Function to create bias on diffusion coefficients.
        Default = pydiffusion.utils.efunc
        efunc(X, Xf, r)
        efunc should return 1 as the maximum when X == Xf,
        and return 0 when abs(X-Xf) == r.

    Returns
    -------
    fDbias : DiffSystem
        Diffusion coefficients with bias.

    """
    Xr, Np, fD = diffsys.Xr, diffsys.Np, diffsys.Dfunc
    efunc = efunc_default if efunc is None else efunc
    fDbias = []
    for i in range(Np):
        if X >= Xr[i, 0] and X <= Xr[i, 1]:
            Xf = np.linspace(Xr[i, 0], Xr[i, 1], 30)
            Df = np.exp(splev(Xf, fD[i]))
            eid = np.where((Xf >= X-r) & (Xf <= X+r))[0]
            for j in eid:
                Df[j] *= 10**(deltaD * efunc(X, Xf[j], r))
            fDbias += [splrep(Xf, np.log(Df))]
        else:
            fDbias += [fD[i]]
    return DiffSystem(Xr, fDbias)
