import os
from keycloak import KeycloakOpenID
from typing import Tuple


def get_keycloak_data() -> Tuple[KeycloakOpenID, str]:
    keycloak_url: str = os.getenv("KEYCLOAK_URL")
    client_id: str = "application"
    client_secret: str = "pOCVJN96A6JadyLHH2xK15O264ee2K61"

    if keycloak_url is None:
        raise ValueError("The keyclock URL isn't defined!")

    if (client_id is None) or (client_secret is None):
        raise ValueError("The client's credentials aren't defined!")

    openid = KeycloakOpenID(
        server_url=keycloak_url,
        client_id=client_id,
        realm_name="inference",
        client_secret_key=client_secret,
        verify=False
    )
    config_well_known = openid.well_known()
    endpoint = config_well_known["token_endpoint"]
    return openid, endpoint
    
    
def get_Actual_keycloak_data(arg1,arg2) -> Tuple[KeycloakOpenID, str]:
    keycloak_url: str = os.getenv("KEYCLOAK_URL")
    client_id: str = arg1
    client_secret: str = arg2

    if keycloak_url is None:
        raise ValueError("The keyclock URL isn't defined!")

    if (client_id is None) or (client_secret is None):
        raise ValueError("The client's credentials aren't defined!")

    openid = KeycloakOpenID(
        server_url=keycloak_url,
        client_id=client_id,
        realm_name="inference",
        client_secret_key=client_secret,
        verify=False
    )
    config_well_known = openid.well_known()
    endpoint = config_well_known["token_endpoint"]
    return openid, endpoint
