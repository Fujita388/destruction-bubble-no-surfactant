###########################################################
# Add gas phase
# Gravity on a time-developed system in "make_bubble.input"
###########################################################

class Atoms:
    def __init__(self, atom_id, mol_id, atom_type, x, y, z, vx, vy, vz):
       self.atom_id = atom_id
       self.mol_id = mol_id
       self.atom_type = atom_type
       self.x = x
       self.y = y
       self.z = z
       self.vx = vx
       self.vy = vy
       self.vz = vz


#class Bonds:
#    def __init__(self, bond_id, bond_type, atom_id1, atom_id2):
#        self.bond_id = bond_id
#        self.bond_type = bond_type
#        self.atom_id1 = atom_id1
#        self.atom_id2 = atom_id2


# Read ".atoms" and ".lammpstrj"
def read_files(atoms, bonds, atoms_file, dump_file):
    with open(atoms_file, "r") as f:  # Read ".atoms"
        atoms_data = f.readlines()
    with open(dump_file, "r") as f:  # Read ".lammpstrj"
        dump_data = f.readlines()
    step = []  # Array of the first index of each step in ".lammpstrj"
    for i, line in enumerate(dump_data):
        if "ITEM: TIMESTEP" in line:
            step.append(i)
    num_atoms = int(atoms_data[2].split()[0])  # Number of atoms
    num_bonds = int(atoms_data[3].split()[0])  # Number of bonds
    mol_list = [0 for i in range(num_atoms+num_bonds)]  # List of mol_id
    for i, line in enumerate(atoms_data):
        if "Atoms" in line:
            while i+2 < num_atoms+14:
                atom_id = int(atoms_data[i+2].split()[0])
                mol_id = int(atoms_data[i+2].split()[1])
                mol_list[atom_id-1] = mol_id
                i += 1
        if "Bonds" in line:
            while len(atoms_data) > i+2:
                db = atoms_data[i+2].split()  # Data in Bonds section
                bonds.append(Bonds(db[0], db[1], db[2], db[3]))
                i += 1
    for i in range(num_atoms):
        position = dump_data[step[-1]+9+i]  # Beginning of atomic data of the last step 
        atom_id = int(position.split()[0])
        atom_type = int(position.split()[1])
        x = float(position.split()[2])
        y = float(position.split()[3])
        z = float(position.split()[4])
        vx = float(position.split()[5])
        vy = float(position.split()[6])
        vz = float(position.split()[7])
        atoms.append(Atoms(atom_id, mol_list[atom_id-1], atom_type, x, y, z, vx, vy, vz))


def save_file(atoms, bonds, l):
    print("Position Data\n")
    print("{} atoms".format(len(atoms)))
    print("{} bonds\n".format(len(bonds)))
    print("2 atom types")
    print("1 bond types\n")
    print("0.00 {} xlo xhi".format(l))
    print("0.00 {} ylo yhi".format(l))
    print("0.00 {} zlo zhi\n".format(2*l))
    print("Atoms\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {} {} {}".format(a.atom_id, a.mol_id, a.atom_type, a.x, a.y, a.z))
    print("\n")
    print("Velocities\n")
    for i, a in enumerate(atoms):
        print("{} {} {} {}".format(a.atom_id, a.vx, a.vy, a.vz))
    print("\n")
    print("Bonds\n")
    for i, a in enumerate(bonds):
        print("{} {} {} {}".format(a.bond_id, a.bond_type, a.atom_id1, a.atom_id2))


atoms = []
bonds = []
read_files(atoms, bonds, "make_bubble.atoms", "make_bubble.lammpstrj")
save_file(atoms, bonds, 51.0)
