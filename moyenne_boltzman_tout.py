#imput : 'conf_index' txt file containing a column with the energy of the conformation and a column with the name of the corresponding cd file
#Calculates the Boltzmann weights for each conformer
#Multiplies the column intensity of the cd files with their Boltzmann weights
#Merges all transitions in a table sorted by ascending wavelength
#output : 'cdspectrum' txt file 

import numpy as np
import sys

# Paramètres
R = 8.314e-3  # Constante en kJ/mol/K
T = 298.15    # Température en Kelvin

# Lire le tableau des énergies
def lire_fichier_donnees(nom_fichier):
    donnees_nettoyees = []
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                ligne = ligne.strip()
                if not ligne or ligne.startswith('#'):
                    continue
                valeurs = [i for i in ligne.split()]
                donnees_nettoyees.append(valeurs)
        print (donnees_nettoyees)
        return np.array(donnees_nettoyees)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        sys.exit(1)

donnees_index = lire_fichier_donnees('conf_index')

energies = np.array([float(row[0]) for row in donnees_index])
fichiers_cd = [row[1] for row in donnees_index]

print(energies)
print(fichiers_cd)

# Calcul des poids de Boltzmann
E_min = np.min(energies)
poids_bruts = np.exp(-(energies - E_min) / (R * T))
poids_normalises = poids_bruts / np.sum(poids_bruts)

print(E_min)
print(poids_normalises)

# Traiter les tableaux
tous_les_spectres =[]
for i, fichier in enumerate(fichiers_cd):
    data = np.array(lire_fichier_donnees(fichier), dtype=float)
    data[:, 1] = data[:, 1] * poids_normalises[i]
    tous_les_spectres.append(data)

# Concaténer et trier par longueur d'onde croissante
tableau_final = np.vstack(tous_les_spectres)
tableau_final = tableau_final[tableau_final[:, 0].argsort()]

# Sauvegarde fichier texte
output_file = "cdspectrum"
with open(output_file, "w") as f:
    for row in tableau_final:
        wl = row[0]
        intensity = row[1]
        f.write(f"{wl:.4f}  {intensity:.8f}\n")

print(f"\n Tableau sauvegardé dans : {output_file}")

