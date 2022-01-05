# Zenodo Uploading Code

Python Directory Parsing and Uploading Code 

- File `run_script.py` does the following:
    1. Finds all files with a certain extension in a directory.
    2. Uploads them to `Zenodo` using their API.
    3. Generates a log file `error_log.txt` in the root directory to note any errors encountered from the Zenodo server.

- The code is platform agnostic, tested on Windows, and used in production on Linux. 

## Prepare

Review `run_script.py` to verify that it does what you think it does. In particular, verify the hard-coded parameters in lines 24 and 29 (see NOTES).

The code can be downloaded to anywhere on your system. The first argument is the path to where the data files are.

You obviously need Python. The script uses imports which you may need to install.

```python
import glob, os
import sys
import requests
import json
import ntpath
```
We suggest to create a Python environment:
```
python3 -m venv .env
source .env/bin/activate
pip install --upgrade pip
pip install requests
```

## Run the code

```python
python run_script.py (DIRECTORY) "(GLOBPAT)" APIKEY [DEPOSITID]
```
where parameters are as follows:

- `(DIRECTORY)`: directory containing the files to upload
- `(GLOBPAT)`: glob pattern for files to upload (e.g., `"*.7z"`). Should include the quotes.
- `APIKEY`: API key generated as per https://developers.zenodo.org/#authentication
- (optional) `DEPOSITID`: If a deposit has already been initiated manually on Zenodo, then specify it on the command line. Otherwise, a new deposit will be generated.

## Finalizing

The script only uploads the files. All metadata will need to be entered through the Zenodo web interface. The URL is printed to the console. Publishing the deposit is intentionally manual.

## NOTES

- Relative paths have <strike>not</strike> been tested. They <strike>may</strike> work.
- If testing, use the Zenodo Sandbox
    - Uncomment line 23, and comment out line 24
- If you would like to search and upload the files from sub-directories in the directory as well, then change the value in Line 29 to "TRUE". 
    - Otherwise, it is "FALSE" by default and the program uploads all files with a certain extension in the directory, but none of its sub-directories.
- Specifying a `DEPOSITID` when the deposit doesn't actually exist will probably lead the code to fail; not tested.


## License

Licensed under [BSD 3-Clause](LICENSE) license.

