# Import Packages
import glob, os
import sys
import requests
import json
import ntpath

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
print("Getting information on deposit...")
r = requests.get(BASE_URL + '/' + DEPOSITION_ID,params = params, headers = headers, json = {})
bucket_url = r.json()['links']['bucket']
print("Uploading to start: ")
print(" Deposit          : " + DEPOSITION_ID)
print(" (check at " + BASE_URL + '/' + DEPOSITION_ID + ")")
print(" Bucket           : " + bucket_url )
input("Press Enter to continue...")
# Parsing through each file and uploading it
for file in glob.glob(search_pattern, recursive = subdir):
    filename = ntpath.basename(file)
    needupload = 1
    for item in r.json()['files']:
        if filename == item['filename']:
           needupload = 0
    if needupload == 0:
           print("Filename " + filename + " present")
           continue

    print("Starting upload for file: "+filename)
    path = os.path.abspath(file)

    # Uploading each file
    with open(path, "rb") as fp:
        rput = requests.put("%s/%s" % (bucket_url, filename),data = fp,params = params)

        # Checking if upload was successful
        if (rput.status_code!=200):
            print("Error Uploading File: {0}, Error Code: {1}".format(filename,rput.status_code))
             
            # Logging an unsuccessful attempt in root directory
            with open((root_dir+"/error_log.log"),"a+") as logger_file:
                logger_file.write(("Error Uploading File: {0}, Error Code: {1}".format(file,rput.status_code))+"\n")
                logger_file.write(rput.json()['message']+"\n")
        else:
            print("Uploading Successful For: "+filename)

# Adding documentation for debugging errors
with open((root_dir+"/error_log.log"),"a+") as logger_file:
    logger_file.write("Please check the descriptions of the error codes at: https://developers.zenodo.org/#http-status-codes"+"\n")

        
    
    
