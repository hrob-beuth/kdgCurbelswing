from params import *
from numpy import sin, cos, pi
import numpy as np


# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#       IMPLIZITE BEZIEHUNG VON PHI UND PSI
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# IMPLIZITE BEZIEHUNG PHI - PSI
# returned null bei richtigen phi,psi Werten
# Achtung: pro psi meist 2 phi werte möglich
def fImpl(phi, psi):
    return (l0 - l1 * cos(phi) - l2 * sin(psi)) ** 2 + (l1 * sin(phi) - l2 * cos(psi)) ** 2 - l3 ** 2


# ABLEITUNG DER IMPLIZITE BEZIEHUNG
# psi' = fImpDerivative(phi,psi) * psi'
# wichtig zum aufstellen der virtuellen Verückung mit LaGrange
def fImpDerivative(phi, psi):
    f1 = l1 * (l0 * sin(phi) - l2 * cos(phi - psi))
    f2 = l2 * (l0 * cos(psi) - l1 * cos(phi - psi))
    if np.abs(f2) < 1e-7:
        print("Achtung Polstelle.")  # wenn f2 -> gibts eine Polstelle
    return f1 / f2


# IMPLIZIT PSI ermitteln mit NEWTON-VERFAHREN
# Wahl des startwertes sehr wichtig sonst klappt newton nicht
from scipy.optimize import newton
def solveForPsi(phi):
    psiStart = goodInitialPsi(phi)
    findPsi = lambda psi: fImpl(phi, psi)
    # berechne psi mit newton verfahren
    return newton(findPsi, psiStart)


# GUTER STARTWERRT FÜR PSI FÜR NEWTON
# newton verfahren funktioniert nur mit gutem startwert psi0
# funtion kann sowohl array als auch skalare WErte in psi0 konvertieren
def goodInitialPsi(phiArr):
    # EINFACHES MAPPING PHI -> PSI0
    # hier wird phi auf 4 verschiedene psi0 werte gemappt
    # diese sind druchschnitts werte der wirklichen psis im phi-Wertebereich
    # TODO: toPsi0Mapping könnte besser sein
    def toPsi0(phi):
        mphi = phi % (2 * pi)  # modulo of phi
        if mphi < pi / 2:
            return 2.20363704
        if mphi < pi:
            return 1.96124776
        if mphi < 3 * pi / 4:
            return 2.30775339
        return 2.72965902

    if np.iterable(phiArr):  # falls array -> return einen psi0-Array
        return np.array([toPsi0(phi) for phi in phiArr])
    return toPsi0(phiArr)
