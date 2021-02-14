from curbelCoords import CurbelSwing
from impicitSolveForPsi import solveForPsi, fImpDerivative
from params import *
from numpy import sin, cos, diff

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#            MOTOR-ANTRIEBSMOMENT mit VIRTUELLE
#               VERRÜCKUNG á la d'ALEMBERT
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# BENÖTIGTES MOTOR-ANTRIEBSMOMENT
# der Moter ist an Gelenk A befässtigt und dreht den Winkel Phi,
# calcMotorMoment berechnet das Moment, das der Motor aufbringen muss,
# um ein bestimmtes phiArr in einem bestimmten timeArr zu halten.
# default: phiArr ist einfach konstantes omega * timeArr
def calcMotorMoment(timeArr, phiArr=None, reibKoeff=muR):
    if phiArr is None:
        phiArr = omega * timeArr  # default: konsate Winkelgescheindigkeit

    # 1. Psi Winkel ermitteln
    psiArr = solveForPsi(phiArr)  # Newton verfahren um Psi-Arrsy zu finden


    # 2. alle numerischen Ableitungen bilden (durch 2mal ableiten fallen letzten zwei Werte im Array weg)
    phi, phi_, phi__, _ = doubelDerivative(phiArr, timeArr)
    psi, psi_, psi__, t = doubelDerivative(psiArr, timeArr)

    # 3. doppelte Ableitung des Schwerpunktes
    xS__, yS__ = CurbelSwing(currentDS).S__(phi, phi_, phi__, psi, psi_, psi__)

    # 3. virtuelle Verrückung, D'Alembert Beziehung aufstellen
    # Motormoment = Trägheiten - Reibung
    FArr = fImpDerivative(phi, psi)
    term1 = Js * psi__ * FArr - reibKoeff * phi_
    term2 = -ms * xS__ * (l1 * sin(phi) - a * FArr * cos(psi) + b / 2 * FArr * sin(psi))
    term3 = ms * (yS__ + g) * (l1 * cos(phi) + a * FArr * sin(psi) + b / 2 * FArr * cos(psi))
    return term1 + term2 + term3, t


#   DOPPELTE ABLEITUNG ÜBER ZEIT
# berechnen der numerischen Ableitung durch die Differenz
# Achtung: durch jedes Ableiten fällt der letzte Wert im Array weg
#          deshalb haben rÜckgabe-werte alle n-2 Einträge
def doubelDerivative(f, t):
    f_ = diff(f) / diff(t)
    f__ = diff(f_) / diff(t[:-1])
    return f[:-2], f_[:-1], f__, t[:-2]

