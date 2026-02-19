import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


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

def decalage(nom_fichier, shift):
	donnees = lire_fichier_donnees(nom_fichier)
	h=6.626*10**(-34)
	c=3*10**8
	energies = []
	energies_decalees = []
	lambdas_decalees = []


	for i in range (len(donnees)):
		energies.append(h*c*10**(9)/donnees[i][0]/(1.6*10**(-19)))
		energies_decalees.append(energies[i]+shift)
		lambdas_decalees.append(h*c*10**(9)/(1.6*(10**(-19)*energies_decalees[i])))
	return lambdas_decalees

def convolution(nom_fichier, fwhm, shift):
	longueur_onde = decalage(nom_fichier, shift)
	intensite = []
	donnees = lire_fichier_donnees(nom_fichier)
	for i in range (len(donnees)):
		intensite.append(donnees[i][1])
	pas=longueur_onde[1]-longueur_onde[0]
	sigma_pixel =fwhm/2.355/pas
	
	intensite_convoluee = gaussian_filter1d(intensite, sigma_pixel)
	
	plt.plot(longueur_onde, intensite, label="Original")
	plt.plot(longueur_onde, intensite_convoluee, label=f"Convolué (FWHM={fwhm}nm)", color='red')
	plt.xlabel("Longueur d'onde (nm)")
	plt.ylabel("Intensité")
	plt.legend()
	plt.grid(True)
	plt.show()

convolution ("cdspectrum", 2, 0.5)

