"""
CD SPECTRUM AUTO-ALIGNMENT (TARGET: 240nm)
------------------------------------------
DESCRIPTION:
  Calculates a specific energy shift (eV) based on the midpoint 
  between the 4th and 5th data points (bands) to align that 
  midpoint exactly to 240 nm.

INPUTS:
  1. 'cdspectrum' : Text file with wavelength (nm) and intensity.

OUTPUT:
  1. 'cdspectrum_shifted_calcul240' : Shifted spectrum file.
------------------------------------------
"""

import numpy as np
import sys

# Constant for direct conversion: Energy(eV) = 1239.84 / Lambda(nm)
# Derived from (h * c) / e_charge
HC_EV_NM = 1239.84193  

def read_data_file(file_name):
    """Parses the input file, filtering out comments and empty lines."""
    cleaned_data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Map strings to floats for calculation
                values = [float(i) for i in line.split()]
                cleaned_data.append(values)
        return cleaned_data
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []

def nm_to_eV(wavelength_nm):
    """Converts wavelength in nm to energy in eV."""
    return HC_EV_NM / wavelength_nm

def eV_to_nm(energy_eV):
    """Converts energy in eV to wavelength in nm."""
    return HC_EV_NM / energy_eV

def calculate_required_shift(file_name):
    """
    Determines the energy shift needed to move the midpoint 
    of the 4th and 5th bands to 240 nm.
    """
    data = read_data_file(file_name)
    if len(data) < 5:
        print("Error: Not enough data points to find the 4th and 5th bands.")
        sys.exit(1)

    # Calculate the wavelength midpoint between row index 3 and 4
    # (Note: index 3 is the 4th band, index 4 is the 5th band)
    midpoint_nm = (data[4][0] - data[3][0]) / 2 + data[3][0]
    
    # Convert midpoint and target (240nm) to energy
    current_energy_ev = nm_to_eV(midpoint_nm)
    target_energy_ev = nm_to_eV(240)
    
    # The shift is the difference needed to reach the target
    shift = target_energy_ev - current_energy_ev
    
    print(f"Midpoint found at: {midpoint_nm:.4f} nm")
    print(f"Calculated shift: {shift:.6f} eV")
    return shift

def apply_energy_shift(file_name, shift_val):
    """Applies a global energy shift to all wavelengths in the file."""
    data = read_data_file(file_name)
    
    for row in data:
        # 1. NM -> eV
        current_ev = nm_to_eV(row[0])
        # 2. Apply Shift
        new_ev = current_ev + shift_val
        # 3. eV -> NM
        row[0] = eV_to_nm(new_ev)
        
    return data

# --- Main Execution ---

target_file = "cdspectrum"
output_file = "cdspectrum_shifted_calcul240"

# Step 1: Calculate the automated shift
calculated_shift = calculate_required_shift(target_file)

# Step 2: Apply the shift to the whole dataset
final_data = apply_energy_shift(target_file, calculated_shift)

# Step 3: Save results
if final_data:
    np.savetxt(output_file, final_data, delimiter="  ", 
               header="Wavelength(nm)_Shifted_to_240 Intensity")
    print(f"Success: Shifted spectrum saved as '{output_file}'")
