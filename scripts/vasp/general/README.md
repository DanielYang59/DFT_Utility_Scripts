# VASP Cleanup Script

## Overview

The `vasp_cleanup.py` script is a Python utility designed to clean up unnecessary VASP (Vienna Ab initio Simulation Package) output files in a given directory. The script retains essential input files like `INCAR`, `POSCAR`, `POTCAR`, and `KPOINTS`, along with the job submission script (default is `script.sh`). All other standard VASP output files are moved to a backup directory for safekeeping.

## Requirements

- Python 3.x
- No external Python packages are required.

## Features

- Moves standard VASP output files to a backup directory.
- Creates a new backup directory if previous ones exist.
- Provides an optional verbosity setting for console output.

## Usage

1. Navigate to the directory containing your VASP files in a terminal.
2. Run the script by specifying its full path:

   ```
   python3 /path/to/vasp_cleanup.py
   ```

### Optional Parameters

- `--job_script`: The name of the job submission script you'd like to keep. Default is `script.sh`.
- `--verbose`: Sets the verbosity level. Can be either "silent" or "verbose". Default is "silent".

### Example Usage from Python

If you prefer to call the script's function from within another Python script, you can do so like this:

```python
from pathlib import Path
from vasp_cleanup import clean_vasp_files

directory = Path(os.getcwd())
clean_vasp_files(directory, job_script="my_script.sh", verbose="verbose")
```
