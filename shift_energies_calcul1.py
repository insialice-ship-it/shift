#Input: 'cdspectrum' txt file with wavelength and intensity columns
#Argument: wavelenght of the experimental first band in nm
#Output:  'cdspectrum_shifted_calcul1' txt file with a wavelength shift calculated in eV to match with the experimental first band.

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

hc_eV_nm = 1239.84193  # h*c en eV·nm

def nm_to_eV(wavelength_nm):
    """Convertit une longueur d'onde en nm vers une énergie en eV."""
    return hc_eV_nm / wavelength_nm

def eV_to_nm(energy_eV):
    """Convertit une énergie en eV vers une longueur d'onde en nm."""
    return hc_eV_nm / energy_eV

def calcul_shift(nom_fichier, pic_exp):
	donnees = lire_fichier_donnees(nom_fichier)

	ev_calc = nm_to_eV(donnees[0][0])
	ev_exp = nm_to_eV(pic_exp)
	shift = ev_exp - ev_calc
	return shift
	
def decalage(nom_fichier, decalage):
	donnees = lire_fichier_donnees(nom_fichier)
	h=6.626*10**(-34)
	c=3*10**8
	energies = []
	energies_decalees = []
	lambdas_decalees = []
	

	for i in range (len(donnees)):
		energies.append(nm_to_eV(donnees[i][0]))
		energies_decalees.append(energies[i]+decalage)
		lambdas_decalees.append(eV_to_nm(energies_decalees[i]))
		donnees[i][0]=lambdas_decalees[i]
	return donnees

try:
	premier_pic = float(sys.argv[1])
	print(f"longueur d'onde du premier pic = {premier_pic} nm")
except (IndexError, ValueError):
	print(f"Aucune valeur saisie")
	sys.exit(1)
	
shift = calcul_shift("cdspectrum", premier_pic)
print (f"On calcule un shift de {shift} eV")
donnees_decalees=decalage("cdspectrum", shift)
np.savetxt("cdspectrum_shifted_calcule", donnees_decalees, delimiter="  ")

