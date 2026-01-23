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

def get_assets():
    A = Assets()
    r = A.get(server, token, limit=None, order='asc', offset=None)
    print(r)

def check_in_asset(assetID):
    A = Assets()
    r = A.checkInAsset(server, token, assetID, note=None, locationID=None)
    print(r)

def get_asset(AssetTAG):
    A = Assets()
    r = A.getDetailsByTag(server, token, AssetTAG)
    print(r)

def check_out_asset(assetID, userID):
    A = Assets()
    r = A.checkOutAsset(server, token, assetID, userID, note=None, locationID=None)
    #Add try catch for assets that were already checked out
    print(r)

def search_assets(keyword):
    A = Assets()
    r = A.search(server, token, limit=None, order='asc', keyword=keyword, offset=None)
    print(r)

def get_asset_by_model(modelID):
    A = Assets()
    r = A.getAssetsByModel(server, token, modelID, limit=None, order='asc', offset=None)
    print(r)

def get_asset_by_category(categoryID):
    A = Assets()
    r = A.getAssetsByCategory(server, token, categoryID, limit=None, order='asc', offset=None)
    print(r)

def get_asset_by_manufacturer(manufacturerID):
    A = Assets()
    r = A.getAssetsByManufacturer(server, token, manufacturerID, limit=None, order='asc', offset=None)
    print(r)

def get_assets_by_company(companyID):
    A = Assets()
    r = A.getAssetsByCompany(server, token, companyID, limit=None, order='asc', offset=None)
    print(r)

def get_asset_by_location(locationID):
    A = Assets()
    r = A.getAssetsByLocation(server, token, locationID, limit=None, order='asc', offset=None)
    print(r)

def get_asset_by_status(statusID):
    A = Assets()
    r = A.getAssetsByStatus(server, token, statusID, limit=None, order='asc', offset=None)
    print(r)

def get_asset_by_status_label(statusLabel):
    A = Assets()
    r = A.getAssetsByStatusLabel(server, token, statusLabel, limit=None, order='asc', offset=None)
    print(r)

def get_details_by_id(assetID):
    A = Assets()
    r = A.getDetailsByID(server, token, assetID)
    print(r)

def get_details_by_tag(tag):
    A = Assets()
    r = A.getDetailsByTag(server, token, tag)
    print(r)

def get_details_by_serial(serial):
    A = Assets()
    r = A.getDetailsBySerial(server, token, serial)
    print(r)

def create_asset(asset_tag, status_id, model_id, name):
    A = Assets()
    r = A.create(server, token, asset_tag, status_id, model_id, name)
    print(r)

def get_id(asset_tag):
    A = Assets()
    r = A.getID(server, token, asset_tag)
    print(r)

def delete_asset(assetID):
    A = Assets()
    r = A.delete(server, token, assetID)
    print(r)

#check_out_asset(1, 1)
#get_asset("asdf1234")
#check_in_asset(1)
#get_assets()
#search_assets("1234")
#get_asset_by_model("book")
#get_asset_by_category("2")
#get_asset_by_manufacturer("")
#get_assets_by_company("")
#get_asset_by_location("")
#get_asset_by_status("1")
#get_asset_by_status_label("")
#get_details_by_id("1")
#get_details_by_tag("asdf1234")
#get_details_by_serial("1234")
create_asset("testtag1234", 2, 1, "Test Asset")
#get_id("testtag1234")
#delete_asset("2")