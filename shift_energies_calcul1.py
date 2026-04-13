"""
CD SPECTRUM ALIGNMENT TO EXPERIMENTAL FIRST BAND
------------------------------------------------
DESCRIPTION:
  Calculates an energy shift (eV) based on the difference between 
  the first wavelength in the theoretical file and a user-specified 
  experimental peak wavelength.

INPUTS:
  1. 'cdspectrum' : Text file with wavelength (nm) and intensity.
  2. CLI Argument  : Wavelength of the experimental first band (nm).

OUTPUT:
  1. 'cdspectrum_shifted_calcul1' : Shifted spectrum file.
------------------------------------------------
"""

import numpy as np
import sys

# Constant for h*c in eV·nm for direct conversion
HC_EV_NM = 1239.84193  

def read_data_file(file_name):
    """Parses the input file, ignoring comments and empty lines."""
    cleaned_data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Split and convert to float
                values = [float(i) for i in line.split()]
                cleaned_data.append(values)
        return cleaned_data
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []

def nm_to_eV(wavelength_nm):
    """Converts wavelength (nm) to energy (eV)."""
    return HC_EV_NM / wavelength_nm

def eV_to_nm(energy_eV):
    """Converts energy (eV) to wavelength (nm)."""
    return HC_EV_NM / energy_eV

def calculate_shift(file_name, exp_peak_nm):
    """
    Calculates the energy shift required to align the first band 
    of the file with the experimental peak.
    """
    data = read_data_file(file_name)
    if not data:
        sys.exit(1)

    # Convert the first wavelength in the file to energy (eV)
    theoretical_ev = nm_to_eV(data[0][0])
    # Convert experimental wavelength to energy (eV)
    experimental_ev = nm_to_eV(exp_peak_nm)
    
    # Calculate the difference (Shift)
    return experimental_ev - theoretical_ev

def apply_shift(file_name, shift_val):
    """Applies the calculated energy shift to all data points."""
    data = read_data_file(file_name)
    
    for row in data:
        # Energy domain conversion and shift
        current_ev = nm_to_eV(row[0])
        shifted_ev = current_ev + shift_val
        # Return to wavelength domain
        row[0] = eV_to_nm(shifted_ev)
        
    return data

# --- Main Execution ---

# Check for experimental wavelength argument
try:
    exp_first_peak = float(sys.argv[1])
    print(f"Target experimental first peak: {exp_first_peak} nm")
except (IndexError, ValueError):
    print("Error: Please provide the experimental wavelength as an argument.")
    print("Example: python script.py 215.5")
    sys.exit(1)

# 1. Determine shift
computed_shift = calculate_shift("cdspectrum", exp_first_peak)
print(f"Calculated Shift: {computed_shift:.6f} eV")

# 2. Apply shift to data
final_data = apply_shift("cdspectrum", computed_shift)

# 3. Save output
if final_data:
    np.savetxt("cdspectrum_shifted_calcul1", final_data, delimiter="  ",
               header=f"Wavelength(nm)_Shifted_to_{exp_first_peak}nm Intensity")
    print("Success: 'cdspectrum_shifted_calcul1' generated.")

