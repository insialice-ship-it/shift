#Imput : 'cdspectrum_shifted' a txt with a wavelengh and intensity columns
#	 'exp.csv' experimental data
#Argument : FWHM parameter in eV (defaulting to 0.3 eV if not specified)
#Output : 'convolution.png' a plot with the original sticks, the gaussian convoluted curve (red line) and experimental reference (dashed black line)

import numpy as np
import matplotlib.pyplot as plt
import os
import sys #
import pandas as pd

# Parametres
hc = 1239.842  # Constante de conversion nm <-> eV
fwhm_ev = 0.3  # Ta valeur d'entrée en eV

try:
    fwhm_ev = float(sys.argv[1])
    print(f"Lancement avec FWHM = {fwhm_ev} eV")
except (IndexError, ValueError):
    # Valeur par défaut si tu oublies de taper le chiffre
    fwhm_ev = 0.3
    print(f"Aucune valeur saisie, utilisation du FWHM par défaut : {fwhm_ev} eV")

# Conversion FWHM (eV) -> Sigma (eV)
# Note : La formule standard est exp(-0.5 * (delta/sigma)**2)
sigma_ev = fwhm_ev / (2 * np.sqrt(2 * np.log(2)))

# Chargement des données
data = np.loadtxt('cdspectrum_shifted')
x_data = data[:, 0]  # Longueurs d'onde (nm)
y_data = data[:, 1]  # Intensités

# Chargement des données expérimentales (.csv) 
try:
    # sep=None avec engine='python' détecte automatiquement , ou ;
    df_exp = pd.read_csv('exp.csv', sep=None, engine='python')
    
    # On suppose que Col 0 = nm et Col 1 = Intensité
    # Si ton CSV a des noms de colonnes, remplace par df_exp['Nom_Col']
    x_exp = df_exp.iloc[:, 0] 
    y_exp = df_exp.iloc[:, 1]
    has_exp = True
except Exception as e:
    print(f"Erreur lecture CSV exp: {e}")
    has_exp = False
    
   
# Préparation de la grille
x_grid_nm = np.linspace(min(x_data) - 20, max(x_data) + 20, 1000)
# On convertit la grille en eV pour que le sigma_ev soit applicable
x_grid_ev = hc / x_grid_nm
y_convoluted = np.zeros_like(x_grid_nm)

#prefactor= 1.0 / (22.97 * sigma_ev ) 
prefactor= 1.0 / (22.97 * sigma_ev * np.sqrt(2 * np.pi)) 

# Calcul de la convolution
for lambda_i, y_i in zip(x_data, y_data):
    # Position du pic en eV
    energy_i = hc / lambda_i
    
    # Calcul de la gaussienne dans le domaine des énergies
    # On utilise le facteur -0.5 correspondant à la définition standard de sigma
    gauss = y_i * np.exp(-0.5 * ((x_grid_ev - energy_i) / sigma_ev)**2)
    y_convoluted += gauss*prefactor

# Affichage
plt.figure(figsize=(8, 6))

# Bâtons originaux
plt.vlines(x_data, 0, y_data*prefactor, color='black', alpha=0.5, label='Transitions (bâtons)')

# Courbe convoluée
plt.plot(x_grid_nm, y_convoluted, color='red', 
         label=f'Convolution (FWHM = {fwhm_ev} eV)')

nom_molecule = os.path.basename(os.path.dirname(os.getcwd()))
if has_exp:
    plt.plot(x_exp, y_exp, color='black', linestyle='--', alpha=0.7, label='Expérimental')
plt.xlim(190, 310)
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('wavelength $\lambda$ [nm]')
plt.ylabel('$\Delta\epsilon$ [M$^{-1}\cdot$cm$^{-1}$]')
plt.title(f"{nom_molecule}")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig(f"convolution", dpi=300) 
plt.show()
