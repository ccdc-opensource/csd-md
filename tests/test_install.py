#!/usr/bin/env python
############################################################################################################################ 
#
# NOTICE WITH SOFTWARE                                                                                                  
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
import unittest
import sys
import importlib
import os
import time
import subprocess
from pathlib import Path


#########################################################################
#                              README
#########################################################################
# Run this script after creating the conda environment and downloading
# the CSD-MD package from GitHub.
#
# In order to run it use this command:
#
# pytest test_install.py &> test_install.log 
#
# The script will check that:
# 1) the python version installed is the right one (test 1)
# 2) all the packages and dependencies required are installed (test 2)
# 3) a few different types of calculations in different scenarios
#    can be done with this workflows (test 3)
#
# The total running time of the tests is about 40 min.
#########################################################################


PACKAGES = {
        'openmm':            'openmm',
        'openmmplumed':      'openmmplumed',
        'ambertools':        'pytraj',
        'openmmforcefields': 'openmmforcefields',
        'pyyaml':            'yaml',
        'tensorflow':        'tensorflow',
        'pdbfixer':          'pdbfixer',
        'openbabel':         'openbabel'
        'pytest':            'pytest'}


EXAMPLES = [
        'asp-gas-MM', 'asp-solution-MM', 'asp-gas-MM-enhanced',
        'asp-gas-ML', 'asp-solution-ML', 'ibu-gas-ML',
        'ibu-solution-MM-enhanced', '4ph9-protein-MM',
        'asp-4ph9-MM', 'asp-4ph9-ML', 'ibu-4ph9-MM']


class TestInstallation(unittest.TestCase):

    # test 1
    def test_python_version(self):
        self.assertGreaterEqual(sys.version_info.major, 3)
        self.assertGreaterEqual(sys.version_info.minor, 9)

    # test 2
    def test_required_packages(self):
        missing = [] 
        for package, module in PACKAGES.items():
            print(f" => Test package {package}",flush=True)
            try:
                importlib.import_module(module)
            except ImportError:
                missing.append(package)
        assert not missing, f"Missing packages: {', '.join(missing)}"

    # test 3
    def test_functionalities(self):
        
        def contains_matching_text(file_path, search_text):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if search_text.lower() in line.lower():
                        return True
            return False

        missing2 = []
        for example in EXAMPLES:
            print(f" => Test example {example} {'':.<{30 -len(example) - 1}}",end='',flush=True)
            cwd = Path.cwd()
            parent = cwd.parent
            yaml_file = parent / "examples" / f"{example}.yaml"
            log_file = cwd / f"{example}.log"
            script = parent / "CSD-MD.py"
            with open(log_file, 'w') as log:
                subprocess.run(['python', script, '--md_params', yaml_file],
                               stdout=log, stderr=subprocess.STDOUT)
            # Wait until the log file exists
            while not os.path.exists(log_file):
                time.sleep(0.1)  # Check every 100ms
            normal_termination = contains_matching_text(log_file, "MD simulation has completed")
            if normal_termination:
                print(f" PASS",flush=True)
            else:
                missing2.append(example)
                print(f".. FAIL <=",flush=True)
        assert not missing2, f"Failed tests: {', '.join(missing2)}"


if __name__ == '__main__':
    unittest.main()


