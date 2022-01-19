# Import Packages
import glob, os
import sys
import requests
import json
import ntpath
import hashlib

# Change Directory To The Root Directory, please ensure that there is no slash symbol in the end
#root_dir = "C:/Users/vg224_RS/sample_folder"
root_dir = sys.argv[1]

# Extension To Be Searched
#ext = "*.py"
ext = sys.argv[2]

# Change Access Token
#ACCESS_TOKEN = "CHANGE_ME"
ACCESS_TOKEN = sys.argv[3]
DEPOSITION_ID = sys.argv[4]

#====================== hard-coded parameters - CHANGE IF NECESSARY ======================================
# Base URL: could be the sandbox!
# BASE_URL = "https://sandbox.zenodo.org/api/deposit/depositions"
BASE_URL = "https://zenodo.org/api/deposit/depositions"

# Would you like to search the subdirectories in the directory as well? 
# "True" for Yes, "False" for No. 
# "True" by default.
subdir = False

#============================= NO FURTHER CHANGES NEEDED BEYOND HERE =======================================

# setting search_pattern to be full path
os.chdir(root_dir)
search_path = root_dir + "/"
search_pattern = search_path + ext

print("Search pattern:" + search_pattern)

# Configuring Script For Zenodo Upload
params = {'access_token': ACCESS_TOKEN}
headers = {"Content-Type": "application/json"}
# If creating a new deposit, then the post will create that new deposit
#r = requests.post(BASE_URL,params = params, headers = headers, json = {})
# However, if we already have a deposit, we want to get the information
r = requests.get(BASE_URL + '/' + DEPOSITION_ID,params = params, headers = headers, json = {})
bucket_url = r.json()['links']['bucket']
print("Uploading to start: ")
print(" Deposit          : " + DEPOSITION_ID)
print(" (check at " + BASE_URL + '/' + DEPOSITION_ID + ")")
print(" Bucket           : " + bucket_url )
input("Press Enter to continue...")
# Parsing through each file and verifying it
for file in glob.glob(search_pattern, recursive = subdir):
    filename = ntpath.basename(file)
    path = os.path.abspath(file)
    needupload = 1
    for item in r.json()['files']:
        if filename == item['filename']:
            needupload = 0
            original_md5 = item['checksum']
            print("Filename " + filename + " present")

            # Compute checksum for each file
            with open(path, "rb") as fp:
            # read contents of the file
                data = fp.read()    
            # pipe contents of the file through
                md5_returned = hashlib.md5(data).hexdigest()
            # Finally compare original MD5 with freshly calculated
                if original_md5 == md5_returned:
                    print("Filename " + filename + ": MD5 verified.")
                else:
                    print("Filename " + filename + ": MD5 verification failed!.")
                    print(" Server MD5: " + original_md5)
                    print(" Local  MD5: " + md5_returned)
    if needupload == 1:
        print("Filename  "+filename + " missing on server")
        continue


        
    
    
