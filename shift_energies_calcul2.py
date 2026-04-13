"""
CD SPECTRUM ALIGNMENT TO EXPERIMENTAL SECOND BAND
-------------------------------------------------
DESCRIPTION:
  Calculates an energy shift (eV) based on the difference between 
  the third data point (second band) in the theoretical file and 
  a user-specified experimental wavelength.

INPUTS:
  1. 'cdspectrum' : Text file with wavelength (nm) and intensity.
  2. CLI Argument  : Wavelength of the experimental second band (nm).

OUTPUT:
  1. 'cdspectrum_shifted_calcul2' : Shifted spectrum file.
-------------------------------------------------
"""

import numpy as np
import sys

# Physical constant for h*c in eV·nm
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
                # Split whitespace and convert to floats
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

def calculate_shift_from_second_band(file_name, exp_peak_nm):
    """
    Calculates the energy shift needed to align the second band 
    (index 2) of the file with the experimental reference.
    """
    data = read_data_file(file_name)
    if len(data) < 3:
        print("Error: The file does not contain at least 3 data points.")
        sys.exit(1)

    # Convert the 2nd row wavelength to energy (eV)
    theoretical_ev = nm_to_eV(data[1][0])
    # Convert experimental wavelength to energy (eV)
    experimental_ev = nm_to_eV(exp_peak_nm)
    
    # Calculate the shift required
    return experimental_ev - theoretical_ev

def apply_shift(file_name, shift_val):
    """Applies a global energy shift to all data points in the file."""
    data = read_data_file(file_name)
    
    for row in data:
        # Convert nm to eV, add shift, convert back to nm
        current_ev = nm_to_eV(row[0])
        shifted_ev = current_ev + shift_val
        row[0] = eV_to_nm(shifted_ev)
        
    return data

# --- Main Execution ---

# Check for the experimental wavelength argument from command line
try:
    exp_second_peak = float(sys.argv[1])
    print(f"Target experimental second peak: {exp_second_peak} nm")
except (IndexError, ValueError):
    print("Error: Please provide the experimental wavelength as an argument.")
    print("Example: python script.py 250.0")
    sys.exit(1)

# 1. Determine the energy shift
computed_shift = calculate_shift_from_second_band("cdspectrum", exp_second_peak)
print(f"Calculated Shift: {computed_shift:.6f} eV")

# 2. Process the spectrum shift
final_data = apply_shift("cdspectrum", computed_shift)

# 3. Save the results
output_name = "cdspectrum_shifted_calcul2"
if final_data:
    np.savetxt(output_name, final_data, delimiter="  ",
               header=f"Wavelength(nm)_Shifted_to_{exp_second_peak}nm Intensity")
    print(f"Success: '{output_name}' generated.")
