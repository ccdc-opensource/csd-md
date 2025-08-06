# CSD-MD
CSD-MD is a Python package that enables the user to setup and run a molecular dynamics simulation using CSD entries and CCDC tools.

## Funding, Authorship, and Acknowledgments
This workflow has been developed thanks to the seed funding from the Grant "UKRI Impact Acceleration Account (IAA) Proof of Concept Scheme" and the collaboration between:
- The Richard Bryce Group at the University of Manchester (UoM): https://research.manchester.ac.uk/en/persons/richard.bryce and,
- The Discovery Science Team at the Cambridge Cristallographic Data Centre (CCDC).

#### Main author and developer
- Christopher D. Williams (UoM) -> CSD-MD code, workflows and ML models
#### Developers
- Simon Cottrell (CCDC) -> ccdc_convertor & convertor tests
- Kepa Burusco-Goni (CCDC) -> install tests
#### Credits
- Christopher D. Williams (UoM), Simon Cottrell (CCDC), Kepa Burusco-Goni (CCDC), Austin Lloyd (CCDC), Bojana Popovic (CCDC), & Richard Bryce (UoM)

## Installation (Ubuntu Linux machine or Linux Virtual Machine)
This workflow is primarily designed for Linux-based systems. While it can be installed and run on macOS, compatibility may vary and additional configuration might be required. Running the workflow on Windows is not straightforward and typically requires the use of the Windows Subsystem for Linux (WSL), along with manual adjustments to system settings and dependencies.

### 1. Install a local miniconda3 in your home directory to avoid interfering with the CCDC one
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### 2. Activate the new local miniconda3
```
conda activate /home/username/miniconda3/
source /home/username/miniconda3/bin/activate
```

### 3. Create the csd-md conda environment in your local directory 
```
conda create --prefix ~/csd-md -c conda-forge --override-channels conda python=3.9
conda activate /home/username/csd-md/
source /home/username/csd-md/bin/activate
conda install -c conda-forge openmm openmm-plumed ambertools openmmforcefields pyyaml tensorflow=2.12 pdbfixer openbabel pytest
conda install -c https://conda.ccdc.cam.ac.uk csd-python-api
```

### 4. Add the PATHS to CSD databases and the license to your .bashrc file in your home directory
ATTENTION: We are assuming here that there is already an existing system install containing the CSD-Portfolio on your VM or machine.
If there is not, you will need to first install the CSD portfolio, and then identify the paths mentioned below in your VM or computer:
```
# License activation 
export CCDC_LICENSING_CONFIGURATION="YOUR-LICENSE-LOCATION"
# PATHS to databases (they may differ in your machine)
export CSD_DATA_DIRECTORY="/opt/CCDC/ccdc-data/csd"
export CCDC_MOGUL_DATA="/opt/CCDC/ccdc-data/mogul"
export CSDHOME="/opt/CCDC/ccdc-software"
# PATHS to CCDC software.
# You may or may not require access to this depending on your needs.
# You may need to add or delete some lines. 
export CCDC_ISOSTAR_DATA_DIRECTORY="/opt/CCDC/ccdc-data/isostar/"
export GOLD_DIR="/opt/CCDC/ccdc-software/gold/GOLD/"
```

### 5. Clone the CSD-MD repository
- From CCDC open-source GitHub repository: `git clone https://github.com/ccdc-opensource/csd-md.git`
- From Chris Williams original GitHub repository: `git clone https://github.com/mbdx6cw3/CSD-MD.git`

### 6. Test install
To verify that the installation has been completed successfully, navigate to the tests directory and execute the following command:

`pytest test_install.py &> test_install.log &`

The test suite is organized into three groups:
1. Python Environment Check - Verifies the installed Python version.
2. Dependencies Validation - Ensures all required packages and dependencies are present.
3. Workflow Capabilities - Confirms the availability of supported calculation types.
Currently, there are 11 calculation types being tested. Please note that one of them (asp-4ph9-ML.yaml) is still under development and is expected to fail.
This is normal and does not indicate a problem with the installation.

The test suite takes approximately 40 minutes to complete so, if it appears to be taking a while, there's no need for concern.
Once the tests have finished, you can clean up the test directory by running the following command:

`python clean_tests.py`

## Running MD simulations
A single .yaml input file is required. This contains all information required to retrieve structures, construct topologies and run MD simulations.

#### Example usage:
`python CSD-MD.py --md_params input.yaml > md.log`

#### Input options (input.yaml):
```
name:                   name of the simulation
system type:            "ligand", "protein" or "protein-ligand"
CSD identifier:         identifier associated with the ligand
PDB identifier:         four letter identifier associated with protein,
pair-net model path:    path to trained PairNet model or "none"
solvate system:         "yes" or "no"
simulation type:        "standard" or "enhanced"
simulation time (ns):   total simulation time in nanoseconds
timestep (fs):          integration timestep in femtoseconds
temperature (K):        temperature in Kelvin
ensemble:               "NVT"
```

##### System types:
- *ligand* will retrieve a ligand from a CSD entry and generate the initial structure using CCDC conformer generator.
- *protein* will retrieve a protein from RCSB Protein Data Bank and generate the initial (sanitised) structure using PDBFixer.
- *ligand-protein* will retrieve a ligand from a CSD entry and a protein from RCSB Protein Data Bank, and then generate the initial structure by docking the ligand to the protein, defining the binding site using a native ligand in the unsanitised protein structure.

##### Solvate system:
- *yes* (ligand only) adds water to the system and ionises functional groups appropriate for pH 7.4.
- *no* will perform a gas phase simulation
Note that since PairNet has a fixed number of input descriptors, the number of atoms in the ligand must match the number of atoms in the PairNet model.

##### Simulation types:
- *standard* will perform an MD simulation
- *enhanced* will perform a metadynamics simulation with sampling enhanced with respect to the rotatable bonds identified using the CCDC conformer generator

##### PairNet Model Library (in "models" directory):
- *models/aspirin/neutral/MD-300K/*
- *models/aspirin/neutral/Meta-300K/*
- *models/aspirin/ionised/MD-300K/*
- *models/aspirin/ionised/Meta-300K/*
- *models/ibuprofen/neutral/MD-300K/*
- *models/ibuprofen/neutral/Meta-300K/*
- *models/ibuprofen/ionised/MD-300K/*
- *models/ibuprofen/ionised/Meta-300K/*

Note that "none" will use an MM potential (GAFF2) instead of PairNet. Water will be modelled using TIP3P.

## Example Library (in "examples" directory):
- *asp-gas-MM.yaml*:                MD simulation of aspirin using an MM potential
- *asp-solution-MM.yaml*:           MD simulation of aspirin in water using an MM potential
- *asp-gas-MM-enhanced.yaml*:       Metaydnamics simulation of aspirin using an MM potential
- *asp-gas-ML.yaml*:                MD simulation of aspirin using a PairNet potential
- *asp-solution-ML.yaml*:           MD simulation of aspirin in water using a PairNet potential
- *ibu-gas-ML.yaml*:                MD simulation of ibuprofen using a PairNet potential
- *ibu-solution-MM-enhanced.yaml*:  Metadynamics simulation of ibuprofen in water using an MM potential
- *4ph9-protein-MM.yaml*:           MD simulation of cyclooxygenase-2 using an MM potential
- *asp-4ph9-MM.yaml*:               MD simulation of cyclooxygenase-2 bound aspirin using an MM potential
- *asp-4ph9-ML.yaml*:               MD simulation of cyclooxygenase-2 bound aspirin using a PairNet potential
- *ibu-4ph9-MM.yaml*:               MD simulation of cyclooxygenase-2 bound ibuprofen using a PairNet potential

## References:

- CR Groom, IJ Bruno, MP Lightfoot and SC Ward, The Cambridge Structural Database, **2016**, *Acta Cryst.*, B72: 171-179.
- JC Cole, O Korb, P McCabe, MG Read, R Taylor, Knowledge-Based Conformer Generation Using the Cambridge Structural Database, **2018**, *J. Chem. Inf. Model.*, 58: 615-629.
- G Jones, P Willett, RC Glen, AR Leach, R Taylor, Development and Validation of a Genetic Algorithm for Flexible Docking, **1997**, *J. Mol. Bio.*, 267: 727-748.
- P Eastman, J Swails, JD Chodera, RT McGibbon, Y Zhao, KA Beauchamp, LP Wang, AC Simmonett, MP Harrigan, CD Stern, RP Wiewiora, BR Brooks, VS Pande, OpenMM 7: Rapid Development of High Performance Algorithms for Molecular Dynamics, **2017**, *PLOS Comp. Biol.*, 13(7): e1005659.
- CD Williams, J Kalayan, NA Burton, RA Bryce, Stable and Accurate Atomistic Simulations of Flexible Molecules using Conformationally Generalisable Machine Learned Potentials, **2024**, *Chem. Sci.*, 15: 12780-12795.
- RA Sykes, NT Johnson, CJ Kingsbury et al, What Has Scripting Ever Done For Us? The CSD Python Application Programming Interface (API), **2024**, *J. Appl. Cryst.*, 57, 1235-1250.
