import numpy as np
import sys

# Paramètres
R = 8.314e-3  # Constante en kJ/mol/K
T = 298.15    # Température en Kelvin

# Energie des conformères en kJ/mol
try:
    E1 = float(input("Énergie du conformère 1 (E1) en kJ/mol: "))
    E2 = float(input("Énergie du conformère 2 (E2) en kJ/mol: "))
except ValueError:
    print("Erreur : veuillez entrer des valeurs numériques.")
    sys.exit(1)

# Lire les tableaux
def lire_fichier_donnees(nom_fichier):
    donnees_nettoyees = []
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if not ligne or ligne.startswith('#'):
                    continue
                valeurs = [float(i) for i in ligne.split()]
                donnees_nettoyees.append(valeurs)
        return np.array(donnees_nettoyees)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        sys.exit(1)

tableau1 = lire_fichier_donnees('cdspectrum1')
tableau2 = lire_fichier_donnees('cdspectrum2')

# Calcul des poids de Boltzmann
E_min = min(E1, E2)
w1_brut = np.exp(-(E1 - E_min) / (R * T))
w2_brut = np.exp(-(E2 - E_min) / (R * T))

# Normalisation
w1 = w1_brut / (w1_brut + w2_brut)
w2 = w2_brut / (w1_brut + w2_brut)

print(f"  Conformère 1 : w1 = {w1:.4f}")
print(f"  Conformère 2 : w2 = {w2:.4f}")

# Pondération
t1_weighted = tableau1.copy()
t1_weighted[:, 1] = tableau1[:, 1] * w1

t2_weighted = tableau2.copy()
t2_weighted[:, 1] = tableau2[:, 1] * w2

# Combiner les deux tableaux (toutes les barres)
tableau_combined = np.vstack([t1_weighted, t2_weighted])

# Trier par longueur d'onde croissante
tableau_combined = tableau_combined[tableau_combined[:, 0].argsort()]

# Sauvegarde fichier texte
output_file = "cdspectrum"
with open(output_file, "w") as f:
    for row in tableau_combined:
        wl = row[0]
        intensity = row[1]
        f.write(f"{wl:.4f}  {intensity:.8f}\n")

print(f"\n Tableau sauvegardé dans : {output_file}")

