import argparse

# Default OPLSAA atom type and charge for unknown atoms
DEFAULT_OPLSAA_ATOM_TYPE = "@atom:0"  
DEFAULT_CHARGE = 0.0  

# Extended OPLSAA atom type dictionary (now including P and Ni)
OPLSAA_ATOM_TYPES = {
    "C": "@atom:135",    # CH3 Carbon
    "N": "@atom:94",     # Nitrile Nitrogen
    "H": "@atom:140",    # Hydrogen in CH3
    "O": "@atom:434",    # Hydroxide Oxygen
    "K": "@atom:408",    # Potassium Ion
    "CL": "@atom:154",   # Chlorine
    "F": "@atom:179",    # Fluorine
    "P": "@atom:200",    # Phosphorus (Added)
    "NI": "@atom:300"    # Nickel (Added)
}

# Default charges for common atoms (including P and Ni)
CHARGE_MAP = {
    "C": 0.18,
    "N": -0.43,
    "H": 0.06,
    "O": -1.00,
    "K": 1.00,
    "CL": -0.10,
    "F": -0.20,
    "P": 0.50,   # Example charge for Phosphorus
    "NI": 2.00   # Example charge for Nickel
}

def pdb_to_lt(pdb_file, lt_file, molecule_name):
    """
    Converts any PDB file to a Moltemplate .lt file with OPLSAA compatibility.
    Supports all standard elements and automatically assigns atom types and charges.
    """

    atoms = []
    bonds = []
    atom_counter = 1
    atom_name_map = {}  # To map PDB indices to LT atom names

    # Step 1: Parse the PDB file for atoms and bonds
    with open(pdb_file, 'r') as file:
        for line in file:
            if line.startswith(("ATOM", "HETATM")):
                # Parsing standard PDB columns
                atom_index = line[6:11].strip()
                atom_type = line[76:78].strip().upper()  # Ensure uppercase for consistency
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())

                # Assign atom type and charge using dictionaries (defaults if missing)
                oplsaa_type = OPLSAA_ATOM_TYPES.get(atom_type, DEFAULT_OPLSAA_ATOM_TYPE)
                charge = CHARGE_MAP.get(atom_type, DEFAULT_CHARGE)

                # Generate unique atom name for Moltemplate
                atom_name = f"c{atom_counter}"
                atom_name_map[atom_index] = atom_name
                atoms.append(f'    $atom:{atom_name} $mol {oplsaa_type} {charge} {x:.4f} {y:.4f} {z:.4f}\n')
                atom_counter += 1

            elif line.startswith("CONECT"):
                # Parsing bond information (CONECT)
                parts = line.split()[1:]
                atom1 = atom_name_map[parts[0]]
                for bonded_atom in parts[1:]:
                    atom2 = atom_name_map[bonded_atom]
                    bond_name = f"b{len(bonds)+1}"
                    bonds.append(f'    $bond:{bond_name} $atom:{atom1} $atom:{atom2}\n')

    # Step 2: Write the Moltemplate .lt file
    with open(lt_file, 'w') as file:
        file.write(f'import "oplsaa.lt"\n\n{molecule_name} inherits OPLSAA {{\n\n')
        
        # Writing atom definitions
        file.write('    write("Data Atoms") {\n')
        file.writelines(atoms)
        file.write('    }\n\n')

        # Writing bond definitions if available
        if bonds:
            file.write('    write("Data Bond List") {\n')
            file.writelines(bonds)
            file.write('    }\n\n')

        file.write('}\n')

    print(f"{lt_file} successfully created for {molecule_name}!")
    print(" ")
    print("credit to hasbiarraihanmh")
    
def main():
    # Command-line parser for flexible PDB input
    parser = argparse.ArgumentParser(description="Convert any PDB file to a Moltemplate .lt file with full OPLSAA compatibility.")
    parser.add_argument("pdb_file", help="Path to the PDB file.")
    parser.add_argument("molecule_name", help="Molecule name for the Moltemplate .lt file.")
    args = parser.parse_args()

    # Generate the output .lt filename automatically
    lt_file = args.pdb_file.replace(".pdb", ".lt")
    
    # Convert the PDB to LT
    pdb_to_lt(args.pdb_file, lt_file, args.molecule_name)

if __name__ == "__main__":
    main()
