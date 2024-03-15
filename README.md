WARNING: This probably no longer works, since it was using the pre-2024 Zenodo API!!

# Zenodo Uploading Code

Python Directory Parsing and Uploading Code 

- File `run_script.py` does the following:
    1. Finds all files with a certain extension in a directory.
    2. Uploads them to `Zenodo` using their API.

- The code is platform agnostic, used in production on Linux. Previous versions worked on Windows, but this version has not been tested.

> This version is compatible with the Zenodo API released in October 2023.

## Prepare

Review `run_script.py` to verify that it does what you think it does. 

The code can be downloaded to anywhere on your system. The first argument is the path to where the data files are.

You obviously need Python. The script uses imports which you may need to install. See [requirements.txt](requirements.txt).

```python
import glob, os
import requests
from dotenv import load_dotenv  
import argparse
import hashlib
```

You need a Zenodo API key. See https://developers.zenodo.org/#authentication. You can either export it as an environment variable, or put it in a file called `.env` in the home directory (you can also specify a different file on the command line).

You need to create an empty Zenodo deposit. This will give you (in the URL) the Deposit ID, e.g. `https://zenodo.org/uploads/11303` has Deposit ID `11303`.


## Setting up Python

We suggest to create a [virtual environment](https://docs.python.org/3/library/venv.html)

```{bash}
python3 -m venv .env
source .env/bin/activate
python3 -m pip install -r requirements.txt
export ZENODO_PAT=your-zenodo-key-here-xxxx
```

When you are done with the code, exit the environment:

```{bash}
deactivate
```

## Run the code

```{bash}
python run_script.py (DIRECTORY) "(GLOBPAT)" APIKEY [DEPOSITID]
```
where parameters are as follows:

- `(DIRECTORY)`: directory containing the files to upload
- `(GLOBPAT)`: glob pattern for files to upload (e.g., `"*.7z"`). Should include the quotes.
- `APIKEY`: API key generated as per https://developers.zenodo.org/#authentication
- (optional) `DEPOSITID`: If a deposit has already been initiated manually on Zenodo, then specify it on the command line. Otherwise, a new deposit will be generated.

## Verifying files

Once uploaded, you will want to verify the integrity of the uploaded files. Using the same environment as before,


```{bash}
python run_script.py [-h] -d DIRECTORY -f FILES [-e ENVVARS] [-p PAT] -i ID
                     [--production] [--subdir]
```

(or `python3` depending on your system)

where arguments are as follows:

- (required) `(DIRECTORY)`: directory containing the files to upload
- (required) `(FILES)`: glob pattern for files to upload (e.g., `"*.7z"`). Should include the quotes.
- (required) `ID`: Deposit from upload request.
- `PAT`: API key generated as per https://developers.zenodo.org/#authentication. Required if not provided via the environment variables, or the `.env` file.
- `ENVVARS`: Path to environment variables file. Default is `~/.env`.
- `--production`: Use the production Zenodo server. Default is to use the sandbox.
- `--subdir`: Search subdirectories for files to upload. Default is to only search the specified directory.

This will compute the MD5 sum locally, and compare to files on the server. Output is to standard out. Files already uploaded and with the same MD5 sum are skipped.

You may want to run this with `tee` and then search the output file for failed uploads:


## Finalizing

The script only uploads the files. All metadata will need to be entered through the Zenodo web interface. The URL is printed to the console. Publishing the deposit is intentionally manual.


## License

Licensed under [BSD 3-Clause](LICENSE) license.

