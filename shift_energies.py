"""
CD SPECTRUM WAVELENGTH SHIFTER
------------------------------
DESCRIPTION:
  Shifts a CD spectrum by a specific energy value (in eV). 
  Since the shift is applied in the energy domain, wavelengths (nm) 
  are converted to eV, shifted, and then converted back to nm.

INPUTS:
  1. 'cdspectrum' : Text file with wavelength (col 1) and intensity (col 2).
  2. Command Line Argument  : Float value representing the shift in eV.

OUTPUT:
  1. 'cdspectrum_shifted' : Text file with shifted wavelengths.
------------------------------
"""

import numpy as np
import sys

def read_data_file(file_name):
    """Parses the input file, ignoring comments and empty lines."""
    cleaned_data = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Ignore empty lines or comments
                if not line or line.startswith('#'):
                    continue
                
                # Convert strings to floats and append to list
                values = [float(i) for i in line.split()]
                cleaned_data.append(values)

        return cleaned_data

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []

def apply_shift(file_name, shift_ev):
    """Converts nm to eV, applies the shift, and converts back to nm."""
    data = read_data_file(file_name)
    
    # Physics Constants
    h = 6.626e-34      # Planck's constant (J·s)
    c = 3.0e8          # Speed of light (m/s)
    e_charge = 1.6e-19 # Elementary charge (C) to convert J to eV
    
    # Conversion factor for convenience: E(eV) = HC_FACTOR / lambda(nm)
    # hc / e_charge * 1e9 (to account for nanometers)
    HC_FACTOR = (h * c * 1e9) / e_charge

    for row in data:
        # Original wavelength in nm
        wavelength_nm = row[0]
        
        # 1. Convert wavelength (nm) to energy (eV)
        energy_ev = HC_FACTOR / wavelength_nm
        
        # 2. Apply the shift
        shifted_energy_ev = energy_ev + shift_ev
        
        # 3. Convert shifted energy back to wavelength (nm)
        # Handle potential division by zero if energy becomes 0
        if shifted_energy_ev != 0:
            row[0] = HC_FACTOR / shifted_energy_ev
        else:
            row[0] = 0.0

    return data

# --- Main Execution ---

# Get the shift value from the command line arguments
try:
    shift = float(sys.argv[1])
    print(f"Shift applied: {shift} eV")
except (IndexError, ValueError):
    # Default value if no argument is provided or if input is invalid
    shift = -0.5
    print(f"No valid input provided. Using default shift: {shift} eV")
    
# Process the data
shifted_data = apply_shift("cdspectrum", shift)

# Save the result to a text file
if shifted_data:
    np.savetxt("cdspectrum_shifted", shifted_data, delimiter=" ", 
               header="Wavelength(nm)_Shifted Intensity")
    print("Success: 'cdspectrum_shifted' has been generated.")
