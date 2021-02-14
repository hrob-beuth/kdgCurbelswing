# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#           PARAMETER &  DATENSÄTZE
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––


# DATENSÄTZE
DS1 = (1.0, 0.3, 0.8, 0.7, 0.3, 0.3, 50, 2.5, 0.3)  # Datensatz 1
DS2 = (1.2, 0.4, 1.2, 0.6, 0.6, 0.3, 70, 3.0, 0.2)  # Datensatz 2
DS3 = (1.5, 0.5, 1.5, 1.0, 0.8, 0.2, 90, 4.0, 0.1)  # Datensatz 3
# Hier Datensätze ändern
currentDS = DS2
l0, l1, l2, l3, a, b, ms, Js, omega = currentDS


# GLOBALE PARAMETER
g = 9.81
muR = 12 # Reibkoeffizient
GuterStartWertPsi = 1.9727750240970996  # Durchscnittswert von Psi
