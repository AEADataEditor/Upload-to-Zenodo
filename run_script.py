# Import Packages
import glob, os
import requests
from dotenv import load_dotenv  
import argparse
import hashlib

# Get home directory 
home_dir = os.path.expanduser("~") 


def upload_file(file, bucket_url, params,headers):
    """Uploads a file to Zenodo.
    Args:
        filename (str): The name of the file to upload.
        bucket_url (str): The URL of the bucket to upload to.
        params (dict): The parameters to use for the upload.
        headers (dict): The headers to use for the upload.
    Returns:
        str: The URL of the uploaded file.
    """
    filename = os.path.basename(file)
    
    with open(file, "rb") as fp:
            url = bucket_url + "/" + filename + "?access_token=" + params['access_token']
            rput = requests.put(url,data = fp)
            
            # Checking if upload was successful
            if (rput.status_code!=201):
                print("Error Uploading File: {0}, Error Code: {1}".format(filename,rput.status_code))
                
            else:
                print("Uploading Successful For: "+filename)


def create_filelist(directory, extension, subdir):
    """Creates a list of files to upload.
    Args:
        directory (str): The directory to search for files.
        extension (str): The file extension to search for.
        subdir (bool): Whether or not to search subdirectories.
    Returns:
        list: A list of files to upload.
    """
    search_path = os.path.join(directory, extension)
    if subdir:
        return glob.glob(search_path, recursive=True)
    else:
        return glob.glob(search_path)

    
def main():
    parser = argparse.ArgumentParser(description='Upload to Zenodo. Please create a deposit manually.')
    parser.add_argument('-d','--directory', required=True, help='Directory to use for upload')
    parser.add_argument('-f','--files', required=True,  help='File extension to upload')
    parser.add_argument('-i','--id', required=True,  help='Zenodo Deposition ID')
    parser.add_argument('-e','--envvars', required=False,  help='Environment file containing Zenodo credentials')
    parser.add_argument('-p','--pat', required=False,  help='Zenodo Personal Access Token')
    parser.add_argument('--production', required=False, action='store_true', help='Do NOT use Zenodo sandbox')
    parser.add_argument('--subdir', required=False, action='store_true', help='Search subdirectories')
    args = parser.parse_args()
    
    # Load environment variables  

    # Construct full .env file path
    if args.envvars:
        env_file = args.envvars
    else:
        # if the envvars file exists, read it
        if os.path.isfile(os.path.join(home_dir, ".envvars")):
            env_file = os.path.join(home_dir, ".envvars")
        else:
            if os.path.isfile(os.path.join(home_dir, ".env")):
                env_file = os.path.join(home_dir, ".env")
    
    # if the envvars file exists, read it
    if env_file:
        print("Reading environment variables from " + env_file)
        load_dotenv(env_file)

    if args.pat:
        ACCESS_TOKEN = args.pat
    else:
        ACCESS_TOKEN= os.getenv('ZENODO_PAT')
    # if pat still empty, exit with error message
    if ACCESS_TOKEN == "":
        print("Error: Could not find ZENODO_PAT in files or command line")
        exit(1)
    
    extension = args.files
    directory = args.directory
    DEPOSITION_ID = args.id
    if args.production:
        BASE_URL = "https://zenodo.org/api/deposit/depositions"
    else:
        BASE_URL = "https://sandbox.zenodo.org/api/deposit/depositions"
    subdir = args.subdir

    # setting search_pattern to be full path
    # construct the full search path

    search_pattern = os.path.join(directory, extension)

    print("Search pattern:" + search_pattern)

    params = {'access_token': ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}

    r = requests.get(BASE_URL + '/' + DEPOSITION_ID,
                     params = params, 
                     headers = headers, 
                     json = {})
    if r.status_code != 200:
        print("Error getting deposition: {0}, Error Code: {1}".format(DEPOSITION_ID,r.status_code))
    else:
        print("Deposit found: " + DEPOSITION_ID)

    bucket_url = r.json()["links"]["bucket"]

    #bucket_url = BASE_URL + '/' + DEPOSITION_ID + '/files'
    print("Uploading to start: ")
    print(" Deposit          : " + DEPOSITION_ID)
    print(" (check at " + BASE_URL + '/' + DEPOSITION_ID + ")")
    print(" Bucket           : " + bucket_url )
    input("Press Enter to continue...")

    # Parsing through each file and uploading it
    for file in create_filelist(directory, extension, subdir):
        filename = os.path.basename(file)
        needupload = 1
        for item in r.json()['files']:
            if filename == item['filename']:
                needupload = 0
                original_md5 = item['checksum']
                print("Filename " + filename + " present")

                # Compute checksum for each file
                with open(file, "rb") as fp:
                    # read contents of the file
                    data = fp.read()
                    # pipe contents of the file through
                    # hashlib to get a hash value
                    md5_returned = hashlib.md5(data).hexdigest()

                # Compare checksums
                if md5_returned == original_md5:
                    print("Checksums match for " + filename)
                else:
                    print("Checksums do not match for " + filename)
                    print("Original checksum: " + original_md5)
                    print("Returned checksum: " + md5_returned)
                    print("Uploading file again")
                    needupload = 1

        if needupload == 0:
            print("Filename " + filename + " present")
            continue

        print("Starting upload for file: "+filename)
        # Uploading each file
        upload_file(file, bucket_url, params,headers)


if __name__ == "__main__":
    main()
