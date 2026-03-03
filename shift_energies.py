import numpy as np
import sys

def lire_fichier_donnees(nom_fichier):
    donnees_nettoyees = []
    
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            for ligne in fichier:
                # 1. On retire les espaces inutiles au début et à la fin (strip)
                ligne = ligne.strip()
                
                # 2. On ignore les lignes vides ou celles qui commencent par '#'
                if not ligne or ligne.startswith('#'):
                    continue
                
                # 3. .split() sans argument gère "un ou plusieurs" espaces
                valeurs = [float(i) for i in ligne.split()]
                donnees_nettoyees.append(valeurs)

        return donnees_nettoyees

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        return []

def decalage(nom_fichier, decalage):
	donnees = lire_fichier_donnees(nom_fichier)
	h=6.626*10**(-34)
	c=3*10**8
	energies = []
	energies_decalees = []
	lambdas_decalees = []


	for i in range (len(donnees)):
		energies.append(h*c*10**(9)/donnees[i][0]/(1.6*10**(-19)))
		energies_decalees.append(energies[i]+decalage)
		lambdas_decalees.append(h*c*10**(9)/(1.6*(10**(-19)*energies_decalees[i])))
		donnees[i][0]=lambdas_decalees[i]
	return donnees

try:
    shift = float(sys.argv[1])
    print(f"shift = {shift} eV")
except (IndexError, ValueError):
    # Valeur par défaut si tu oublies de taper le chiffre
    shift = -0.5
    print(f"Aucune valeur saisie, utilisation du shift par défaut : {shift} eV")
    
donnees_decalees=decalage("cdspectrum", shift)
print (donnees_decalees)
np.savetxt("cdspectrum_shifted", donnees_decalees, delimiter=" ")

