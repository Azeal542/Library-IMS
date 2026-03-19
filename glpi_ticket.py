import requests
import json
import sys
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout, ConnectionError

GLPI_URL = "http://10.70.50.11/apirest.php/"

try:
    with open(r"C:\Users\CalebPierce\OneDrive - Klamath Family Head Start\Documents\glpi.txt", 'r') as file:
    #with open(r"/home/kfheadstart/Documents/api.txt", 'r') as file:
        glpi = file.read().strip()  # .strip() removes any leading/trailing whitespace
    print(f"Token loaded successfully: {glpi[:5]}...")  # Show only first 5 characters for security
except FileNotFoundError:
    print("Error: The file C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\glpi.txt was not found.")
    glpi = None
except PermissionError:
    print("Error: Permission denied when reading C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\glpi.txt")
    glpi = None
except Exception as e:
    print(f"An error occurred: {e}")
    glpi = None   

try:
    with open(r"C:\Users\CalebPierce\OneDrive - Klamath Family Head Start\Documents\user.txt", 'r') as file:
    #with open(r"/home/kfheadstart/Documents/api.txt", 'r') as file:
        user = file.read().strip()  # .strip() removes any leading/trailing whitespace
    print(f"Token loaded successfully: {user[:5]}...")  # Show only first 5 characters for security
except FileNotFoundError:
    print("Error: The file C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\user.txt was not found.")
    user = None
except PermissionError:
    print("Error: Permission denied when reading C:\\Users\\CalebPierce\\OneDrive - Klamath Family Head Start\\Documents\\user.txt")
    user = None
except Exception as e:
    print(f"An error occurred: {e}")
    user = None   

USE_TOKEN_AUTH = True
USER_TOKEN = user

APP_TOKEN = glpi

REQUEST_TIMEOUT = 10

# ============================================================================
# GLPI API CLIENT CLASS
# ============================================================================

class GLPIClient:
    """
    Client for interacting with GLPI REST API v1.
    
    Supports two authentication methods:
    1. User Token: Personal token from user profile (use_token=True)
    2. Username/Password: Direct login with credentials (use_token=False)
    """

    def __init__(self, base_url: str, app_token: Optional[str] = None, 
                 user_token: Optional[str] = None, username: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        Initialize GLPI API client.

        Args:
            base_url: Base URL of GLPI API (e.g., http://glpi.local/apirest.php)
            app_token: Application token (optional)
            user_token: User token for token-based authentication
            username: Username for login-based authentication
            password: Password for login-based authentication
        """
        self.base_url = base_url
        self.app_token = app_token
        self.user_token = user_token
        self.username = username
        self.password = password
        self.session_token = None

    def _get_headers(self, include_session: bool = False) -> Dict[str, str]:
        """
        Build request headers.

        Args:
            include_session: Whether to include session token in headers

        Returns:
            Dictionary of HTTP headers
        """
        headers = {'Content-Type': 'application/json'}

        if self.app_token:
            headers['App-Token'] = self.app_token

        if include_session and self.session_token:
            headers['Session-Token'] = self.session_token

        return headers

    def init_session(self) -> bool:
        """
        Initialize a session with GLPI API.
        Tries user_token first, then falls back to username/password.

        Returns:
            True if session initialized successfully, False otherwise
        """
        try:
            headers = self._get_headers()
            
            # Try user_token first if available
            if self.user_token:
                request_data = {'user_token': self.user_token}
                print("Attempting authentication with user token...")
            # Then try username/password
            elif self.username and self.password:
                request_data = {'login': self.username, 'password': self.password}
                print("Attempting authentication with username/password...")
            else:
                print("No authentication credentials provided.")
                print("  Please set either USER_TOKEN or (GLPI_LOGIN + GLPI_PASSWORD)")
                return False
            
            response = requests.post(
                f"{self.base_url}initSession",
                headers=headers,
                json=request_data,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                session_data = response.json()
                self.session_token = session_data.get('session_token')
                print("Session initialized successfully.")
                return True
            else:
                print(f"Failed to initialize session: {response.status_code}")
                print(f"  Response: {response.text}")
                return False

        except (ConnectionError, Timeout) as e:
            print(f"Connection error: {e}")
            return False
        except RequestException as e:
            print(f"Request error: {e}")
            return False

    def kill_session(self) -> bool:
        """
        Terminate the current GLPI session.

        Returns:
            True if session terminated successfully, False otherwise
        """
        if not self.session_token:
            return True

        try:
            headers = self._get_headers(include_session=True)
            response = requests.post(
                f"{self.base_url}killSession",
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code == 200:
                print("Session terminated successfully.")
                self.session_token = None
                return True
            else:
                print(f"Failed to terminate session: {response.status_code}")
                return False

        except RequestException as e:
            print(f"Error terminating session: {e}")
            return False

    def create_ticket(
        self,
        title: str,
        description: str,
        category_id: Optional[int] = None,
        urgency: int = 3,
        impact: int = 3,
        priority: int = 3,
        type_id: int = 1,
        status: int = 1,
        assigned_to: Optional[int] = None,
        requesters: Optional[list] = None,
        use_session: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new ticket in GLPI.

        Args:
            title: Ticket title/name
            description: Ticket description/content
            category_id: ITIL category ID (optional)
            urgency: Urgency level (1-5, default: 3)
            impact: Impact level (1-5, default: 3)
            priority: Priority level (1-5, default: 3)
            type_id: Ticket type ID (1=Incident, 2=Request, default: 1)
            status: Ticket status (1=New, 2=Processing, etc., default: 1)
            assigned_to: User ID to assign ticket to (optional)
            requesters: List of requester user IDs (optional)
            use_session: Whether to use session token (True) or direct auth (False)

        Returns:
            Response dictionary with ticket info if successful, None otherwise
        """
        try:
            # Initialize session if needed and not already done
            if use_session and not self.session_token:
                if not self.init_session():
                    return None

            headers = self._get_headers(include_session=use_session)

            # Build ticket data
            ticket_data = {
                'name': title,
                'content': description,
                'urgency': urgency,
                'impact': impact,
                'priority': priority,
                'type': type_id,
                'status': status
            }

            # Add optional fields
            if category_id is not None:
                ticket_data['itilcategories_id'] = category_id

            if assigned_to is not None:
                ticket_data['_users_id_assign'] = assigned_to

            if requesters:
                ticket_data['_users_id_requester'] = requesters

            # GLPI API v1 expects data wrapped in 'input' array
            request_payload = {'input': [ticket_data]}
            
            response = requests.post(
                f"{self.base_url}Ticket",
                headers=headers,
                json=request_payload,
                timeout=REQUEST_TIMEOUT
            )

            if response.status_code in (200, 201):
                result = response.json()
                # Handle wrapped response format from GLPI
                if isinstance(result, dict) and 'id' in result:
                    ticket_id = result['id']
                    print(f"Ticket created successfully! Ticket ID: {ticket_id}")
                    return result
                else:
                    print(f"Ticket creation request accepted.")
                    print(f"  Response: {json.dumps(result, indent=2)}")
                    return result
            else:
                print(f"Failed to create ticket: {response.status_code}")
                print(f"  Response: {response.text}")
                return None

        except RequestException as e:
            print(f"Request error creating ticket: {e}")
            return None
        
def reportDamagedAsset(assets, location: str, user: str):
    """
    Create a ticket in GLPI for damaged assets.

    Args:
        assets: List of assets
        location: Location where damage occurred
        user: Username reporting the damage
    """
    client = GLPIClient(base_url=GLPI_URL, app_token=APP_TOKEN, user_token=USER_TOKEN)
    ticket_title = f"Damaged Asset Report - {user}"
    
    # Build description with a line for each asset
    description_lines = [f"Location: {location}", ""]
    description_lines.append("Affected Assets:")
    
    if isinstance(assets, list):
        for i, asset in enumerate(assets, 1):
            if isinstance(asset, dict):
                asset_id = asset.get('id', asset.get('asset_id', 'Unknown'))
                asset_name = asset.get('name', asset.get('asset_name', ''))
                if asset_name:
                    description_lines.append(f"  {i}. Asset ID: {asset_id} - {asset_name}")
                else:
                    description_lines.append(f"  {i}. Asset ID: {asset_id}")
            else:
                # Assume it's just an asset ID
                description_lines.append(f"  {i}. Asset ID: {asset}")
    else:
        # Single asset
        description_lines.append(f"  1. Asset ID: {assets}")
    
    ticket_description = "\n".join(description_lines)

    ticket = client.create_ticket(
        title=ticket_title,
        description=ticket_description,
        urgency=4,
        impact=3,
        priority=4,
        type_id=1,
        status=1,
        category_id=1,
        use_session=True
    )

    if ticket:
        asset_count = len(assets) if isinstance(assets, list) else 1
        print(f"Damage report ticket created for {asset_count} asset(s) reported by {user}.")
        client.kill_session()
        return ticket
    else:
        print(f"Failed to create damage report ticket.")
        client.kill_session()

def main():
    reportDamagedAsset(
        assets=[{'id': 123, 'name': 'Laptop A'}, {'id': 456, 'name': 'Projector B'}],
        location="Main Office",
        user="John Doe"
    )

if __name__ == "__main__":
    main()