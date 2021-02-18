from animateCurbel import animateCurbel
from curbelswingDGL import simulate

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#                   AUFGABENSTELLUNG
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# (a) Geben Sie die Koordinaten der Punkte B und C in Abhängigkeit von φ und ψ an.

# (b) Stellen Sie eine Gleichung auf, die die Bestimmung des Winkels ψ in Abhängigkeit vom Winkel φ erlaubt. Warum
# gibt es einen Zusammenhang zwischen beiden Größen, i. a. W. warum kann ψ nicht unabhängig von φ frei gewählt
# werden? 

# (c) Berechnen Sie numerisch die Größen ψ, ψ' und ψ'' als Funktion von φ fü̈r konstante Winkelgeschwindigkeit φ 
# ̇ = ω. Erstellen Sie folgende Diagramme: ψ, ψ' und ψ'' ü̈ber φ. 

# (d) Geben Sie die Koordinaten des Punktes P in Abhängigkeit von φ und ψ an.

# (e) Berechnen Sie die Größen xP, yP als Funktion von φ fü̈r konstante Winkelgeschwindigkeit φ' = ω. Erstellen Sie
# folgendes Diagramm: yP ü̈ber xP mit gleicher Achsenskalierung (die sogenannte Koppelkurve). Markieren Sie in der
# Koppelkurve die zugehörige Lage von P fü̈r φ = 0, φ = π/2, φ = π und φ = 3π/2.

# (f) Vereinfachend wird im Folgenden angenommen, dass nur die Massenträgheit und das Gewicht von Körper 2 fü̈r
# die Bewegungsgleichung relevant sind. Das liegt daran, dass Körper 1 und 3 sehr kleine Massen haben im Vergleich 
# zum Körper 2. Wie groß muss das Antriebsmoment Ma in sein, um die Bewegung mit konstanter Winkelgeschwindigkeit
# φ ̇ = ω aufrechtzuerhalten. Zeichnen Sie ein Diagramm, das Ma in Abhängigkeit vom Drehwinkel φ zeigt.

# (g) Jetzt ist das Antriebsmoment Ma gegeben. Berechnen Sie den Zeitverlauf des Winkels φ und erstellen Sie ein 
# Diagramm, das φ als Funktion der Zeit t zeigt. 


phiArr, phi_Arr, timeArr = simulate(stopTime=5)
animateCurbel(phiArr, timeArr)
