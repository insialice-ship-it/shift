"""
DESCRIPTION:
  Calculates Boltzmann weights for molecular conformers based on absolute 
  energies (Hartree) and produces a weighted, merged CD spectrum.

INPUTS:
  1. 'conf_index' : Text file. Col 1 = CD filename (Individual spectrum files), Col 2 = Corresponding Absolute Energy (Ha).
  2. CD files     : Individual spectrum files listed in 'conf_index'.

OUTPUTS:
  1. 'cdspectrum'          : Final averaged spectrum (sorted by wavelength).
  2. 'energies_summary.txt': Summary of Delta E (Ha, kcal/mol) and weights (%).
"""

import numpy as np
import sys

# --- PARAMETERS ---
T = 298.15          # Temperature in Kelvin
KB_AU = 3.166811e-6 # Boltzmann constant in Hartree / Kelvin
HA_TO_KCAL = 627.509 # Conversion factor from Hartree to kcal/mol

def read_data_file(file_name):
    """Reads a text file and returns a numpy array of values."""
    cleaned_data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                values = [i for i in line.split()]
                cleaned_data.append(values)
        return np.array(cleaned_data)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        sys.exit(1)

# 1. Load the index file
index_data = read_data_file('conf_index')
cd_files = [row[0] for row in index_data]
energies_ha = np.array([float(row[1]) for row in index_data])

# 2. Calculate Energy Differences and Boltzmann Weights
idx_min = np.argmin(energies_ha)
e_min = energies_ha[idx_min]

# Calculate relative energies
delta_e_ha = energies_ha - e_min
delta_e_kcal = delta_e_ha * HA_TO_KCAL

# Boltzmann formula: exp(-deltaE / (kB * T))
raw_weights = np.exp(-delta_e_ha / (KB_AU * T))
normalized_weights = raw_weights / np.sum(raw_weights)

# --- CONSOLE STATUS ---
print("-" * 45)
print(f"Reference Conformer (Min): {cd_files[idx_min]}")
print(f"Minimum Energy: {e_min:.6f} Ha")
print("-" * 45)

# 3. Save Energy Summary Table
energy_summary_file = "energies_summary.txt"
with open(energy_summary_file, "w") as f:
    f.write("# File_Name                DeltaE(Ha)  DeltaE(kcal/mol)  Weight(%)\n")
    for i in range(len(cd_files)):
        f.write(f"{cd_files[i]:<25} {delta_e_ha[i]:.6f} {delta_e_kcal[i]:.4f} {normalized_weights[i]*100:.2f}%\n")

# 4. Process CD files and apply weights
all_spectra = []
for i, filename in enumerate(cd_files):
    data = np.array(read_data_file(filename), dtype=float)
    # Apply weight to the intensity (second column)
    data[:, 1] *= normalized_weights[i]
    all_spectra.append(data)

# 5. Merge, Sort by Wavelength, and Save
final_table = np.vstack(all_spectra)
final_table = final_table[final_table[:, 0].argsort()]

output_spectrum = "cdspectrum"
np.savetxt(output_spectrum, final_table, fmt=['%.4f', '%.8e'], 
           header="Wavelength(nm) Weighted_Intensity")

print(f"Success: '{output_spectrum}' and '{energy_summary_file}' generated.")
