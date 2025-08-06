#!/usr/bin/env python3
############################################################################################################################ 
#
# The Cambridge Crystallographic Data Centre (CCDC) provides various scripts to many users for use with CCDC applications.
# Some scripts may be library scripts, written at some earlier stage in time and distributed to other users. Other scripts
# may be written de novo or modified library scripts for distribution to a specific client for a specific purpose.
#
# Unless otherwise agreed, CCDC reserves the right to store a modified or de novo script and use that script as part of a
# library available to other users.
#
# No warranty: regardless of the intent of the parties, CCDC makes no warranty that any script is fit for any particular
# purpose.
#
# License grant: By accepting any CSD-MD script from CCDC, each user accedes to the following terms:
#
# - CSD-MD scripts and models remain the property of CCDC and the Richard Bryce Group at the University of Manchester (RBG).
#   Regardless of any changes made by a user, the original source code, models and script remain the property of CCDC and
#   the RBG, and users agree to make no claim of ownership thereof.
# - Users are granted a license to use the CSD-MD software for any purpose, and to change or modify (edit) the script to
#   suit specific needs.
# - Users may not share the CSD-MD script (unmodified or modified by the user) with any third party without permission from
#   CCDC or RBG.
# - Users will acknowledge the original authors when using CSD-MD and derived scripts in their research.
#
# Please note, this CSD-MD script is provided as-is, but is not formally supported by CCDC at this time.
#
############################################################################################################################
__author__ = ['Christopher D Williams']
__credits__ = ['Kepa Burusco-Goni, Simon Cottrell, Austin Lloyd, '
               'Bojana Popovic, Richard Bryce ']
__license__ = '...'
__developer__ = 'Christopher D Williams'
__email__ = 'christopher.williams-2@manchester.ac.uk'
__status__ = 'Development'
__funding__ = "Funded by UKRI IAA"


def main():
    """

    :return:
    """
    from molecular_dynamics import MolecularDynamics
    import os, shutil
    import warnings, get_structure
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    print("Reading input parameters...")
    simulation = MolecularDynamics()
    simulation.read_inputs()

    if simulation.CSD != "from_gro":
        simulation.input_dir = "md_input/"
        isExist = os.path.exists(simulation.input_dir)
        if isExist:
            shutil.rmtree(simulation.input_dir)
        os.makedirs(simulation.input_dir)

        if simulation.protein:
            print("Retrieving PDB...")
            get_structure.protein(simulation)
            print("Fixing PDB...")
            get_structure.fix_protein_pdbfixer(simulation)

        if simulation.ligand:
            print(f"Retrieving CSD entry for {simulation.CSD}...")
            get_structure.ligand(simulation.CSD, simulation)
            print(f"SMILES notation: {simulation.smiles} ")

            if simulation.protein:
                print(f"Docking ligand...")
                get_structure.docking(simulation)

    print("Setting up MD simulation...")
    simulation.setup()

    simulation.simulate()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

