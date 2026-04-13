#The same program as "convolution.py" with the exception that the imput file name is "cdspectrum_shifted_calcul2" and the output file name is 'convolution_calcul2.png'

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -----------------------------------------------------------------------------
# Parameter
hc = 1239.842  # Constant to convert nm into eV

# -----------------------------------------------------------------------------
# Read the FWHM parameter from the command line
try:
    fwhm_ev = float(sys.argv[1])
    print(f"Lancement avec FWHM = {fwhm_ev} eV")
except (IndexError, ValueError):
    fwhm_ev = 0.3 #default value if no argument provided
    print(f"Aucune valeur saisie, utilisation du FWHM par défaut : {fwhm_ev} eV")

# -----------------------------------------------------------------------------
# Convert FWHM to Gaussian standard deviation σ
# Relationship: FWHM = 2 * sqrt(2 * ln(2)) * σ  ≈  2.355 * σ

sigma_ev = fwhm_ev / (2 * np.sqrt(2 * np.log(2)))

# -----------------------------------------------------------------------------
# Normalisation prefactor of the Gaussian: 1 / (N * σ * sqrt(2π))
prefactor= 1.0 / (22.97 * sigma_ev * np.sqrt(2 * np.pi)) 

# -----------------------------------------------------------------------------
# Load the theorical stick spectrum

data = np.loadtxt('cdspectrum_shifted_calcul2')
x_data = data[:, 0]  # Wavelengths (nm)
y_data = data[:, 1]  # Intensities

# -----------------------------------------------------------------------------
# Load the experimental data
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

# -----------------------------------------------------------------------------
# Build the wavelength grid for the convolved curve

x_grid_nm = np.linspace(min(x_data) - 20, max(x_data) + 20, 1000)
# On convertit la grille en eV pour que le sigma_ev soit applicable
x_grid_ev = hc / x_grid_nm
y_convoluted = np.zeros_like(x_grid_nm)

# -----------------------------------------------------------------------------
# Convolution: sum of Gaussians centred on each theoretical transition
# Each stick (λ_i, y_i) contributes one Gaussian of width σ in the eV domain

for lambda_i, y_i in zip(x_data, y_data):
    energy_i = hc / lambda_i # Peak position converted to eV
    
    # Standard Gaussian centred on energy_i with standard deviation sigma_ev
    # exp(-0.5 * ((E - E_i) / σ)²) is the normalised Gaussian form
    gauss = y_i * np.exp(-0.5 * ((x_grid_ev - energy_i) / sigma_ev)**2)
    y_convoluted += gauss*prefactor # Accumulate each transition's contribution

# -----------------------------------------------------------------------------
# Plot

plt.figure(figsize=(8, 6))

# Sticks
plt.vlines(x_data, 0, y_data*prefactor, color='black', alpha=0.5, label='Transitions (bâtons)')

# Convolved curve:
plt.plot(x_grid_nm, y_convoluted, color='red', 
         label=f'Convolution (FWHM = {fwhm_ev} eV)')

# Retrieve the molecule name from the parent directory (two levels up)
nom_molecule = os.path.basename(os.path.dirname(os.getcwd()))

# Overlay experimental spectrum if available
if has_exp:
    plt.plot(x_exp, y_exp, color='black', linestyle='--', alpha=0.7, label='Expérimental')
plt.xlim(190, 310)
plt.axhline(0, color='black', linewidth=0.8)
plt.xlabel('wavelength $\lambda$ [nm]')
plt.ylabel('$\Delta\epsilon$ [M$^{-1}\cdot$cm$^{-1}$]')
plt.title(f"{nom_molecule}")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("convolution_calcul2.png", dpi=300) 
plt.show()
