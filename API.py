from snipeit import Assets
# Read the token from the file
try:
    with open(r"C:\Users\CalebPierce\OneDrive - Klamath Family Head Start\Documents\api.txt", 'r') as file:
        token = file.read().strip()  # .strip() removes any leading/trailing whitespace
    print(f"Token loaded successfully: {token[:5]}...")  # Show only first 5 characters for security
except FileNotFoundError:
    print("Error: The file C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\api.txt was not found.")
    token = None
except PermissionError:
    print("Error: Permission denied when reading C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\api.txt")
    token = None
except Exception as e:
    print(f"An error occurred: {e}")
    token = None   

server='http://10.70.50.215'


def get_asset(AssetTAG):
    A = Assets()
    r = A.getDetailsByTag(server, token, AssetTAG)
    print(r)

def check_out_asset(assetID, userID):
    A = Assets()
    r = A.checkOutAsset(server, token, assetID, userID, note=None, locationID=None)
    #Add try catch for assets that were already checked out
    print(r)


check_out_asset(1, 1)
#get_asset("asdf1234")