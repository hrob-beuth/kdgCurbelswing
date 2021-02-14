from scipy.integrate import solve_ivp
from impicitSolveForPsi import solveForPsi
from params import *
from numpy import sin, cos
import numpy as np

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#       DGL der KURBELSCHWINGE und ihre LÖSUNG
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# phi'' = someF( phi, phi')

# um die Bewegung (phi) bei einem bestimmten KONSTANTEN Antriebsmoment zu finden,
# muss diese DGL gelöst werden. der Zustandsvektor y = [phi, phi'].

def curbelswingDGL(t, y, motorMoment=0, reibKoeff=muR):
    # y = [phi, phi']
    phi, phi_ = y[0], y[1]
    psi = solveForPsi(phi)

    sphi, cphi = sin(phi), cos(phi)  # bisschen Schreibarbeit sparen
    spsi, cpsi = sin(psi), cos(psi)

    # ACHTUNG: Rechnung ist sehr schreib aufwendig.
    # Deshalb werden hier bestimmte Terme vorher in Buchstaben (A,B,C ...) zusammengefasst,
    # in der Hoffnung Übersichtlichkeit zu schaffen.

    # Geschwindigkeit von psi: psi' = A * phi'
    # A=f1/f2, siehe fImpDerivative
    f1 = l1 * (l0 * sphi - l2 * cos(phi - psi))
    f2 = l2 * (l0 * cpsi - l1 * cos(phi - psi))
    if np.abs(f2) < 1e-7:
        print("Achtung Polstelle.")
    A = f1 / f2  # Achtung polstelle
    psi_ = A * phi_

    # Beschleunigung von psi: psi'' = B* phi''
    # B=A' = (f1'*f2 - f2'*f1)/f2**2 Quotientenregel
    # f1'= f3, f2' = f4
    f1_ = l1 * (l0 * cphi + l2 * sin(phi - psi) * (phi_ - psi_))
    f2_ = l2 * (-l0 * spsi + l1 * sin(phi - psi) * (phi_ - psi_))
    B = (f1_ * f2 - f2_ * f1) / (f2 ** 2)

    # Kinetische Beziehung mit d'Alembert
    # Ma = I * psi'' + J * xS'' + K * ( yS''+g)
    I = Js
    J = -ms * (l1 * sphi - a * A * cpsi + b / 2 * A * spsi)
    K = ms * (l1 * cphi + a * A * spsi + b / 2 * A * cpsi)

    # Beschleunigungen von Schwerpunkt s
    # xs'' = A*phi'' + B*psi'' + C
    C = -l1 * sphi
    D = a * cpsi - b / 2 * spsi
    E = -l1 * cphi * phi_ ** 2 - (a * spsi + b / 2 * spsi) * psi_ ** 2

    # ys'' = D*phi'' + E*psi'' + F
    F = l1 * cphi
    G = a * spsi + b / 2 * cpsi
    H = -l1 * sphi * phi_ ** 2 + (a * cpsi - b / 2 * spsi) * psi_ ** 2

    # in d'Alembert einsetzen
    # Ma = L * psi'' + M * phi'' + N
    L = J * D + K * G + I
    M = J * C + K * F
    N = J * E + K * (H + g)
    # mit psi'' = B* phi''
    P = L * B + M

    # Modellieren der Reibung, zum ausschalten reibKoeff=0
    R = reibKoeff * phi_

    # Ma = P * phi'' + N
    # phi'' = (Ma - N)/P
    phi__ = (motorMoment - N - R) / P

    # y' = [ phi' , phi'' ]
    return np.array([phi_, phi__])


#   LÖST DGL FÜR ZEITRAUM
# wirkt wie echte simulation vom System
# scipy's solve_ivp (initial value problem) wird verwendet um die DGL in einem bestimmten Zeitraum zu lösen
# Achtung: zu extremen Werte machen das System eventuell instabil und
# der Integrierer muss dann sehr lange unnötig rechen
def simulate(stopTime, steps=100, phi0=0., omega0=0., motorMoment=0, reibKoeff=muR):
    timeArr = np.linspace(0, stopTime, steps) # constate Zeitintervalle

    # DGL-Löser von Scipy
    result = solve_ivp(fun=curbelswingDGL,
                       t_span=[timeArr[0], timeArr[-1]],
                       y0=[phi0, omega0],
                       t_eval=timeArr,
                       args=(motorMoment, reibKoeff,))

    return result.y[0], result.y[1], result.t
