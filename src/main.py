# -*- coding: utf-8 -*-
import os
from model_utils import load_model, make_inference
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_utils import Oauth2ClientCredentials
from pydantic import BaseModel
from keycloak.uma_permissions import AuthStatus
from keycloak_utils import get_keycloak_data,get_Actual_keycloak_data


class Instance(BaseModel):
    Age: int
    Gender: str
    Sleep_duration: float
    Deep_sleep_percentage: int
    Light_sleep_percentage: int
    Awakenings: float
    Caffeine_consumption: float
    Alcohol_consumption: float
    Smoking_status: str
    Exercise_frequency: float

class ClientData(BaseModel):
    client_id: str
    client_secret_key: str


app = FastAPI()
keycloak_openid, token_endpoint = get_keycloak_data()
CLIENT_ID, CLIENT_KEY = "",""

oauth2_scheme = Oauth2ClientCredentials(tokenUrl=token_endpoint)

model_path: str = os.getenv("MODEL_PATH")
if model_path is None:
    raise ValueError("The environment variable $MODEL_PATH is empty!")


async def get_token_status(token: str,real_keycloak_openid) -> AuthStatus:
    return real_keycloak_openid.has_uma_access(
        token, "Default_Resource#infer")


async def check_token(client_data: ClientData, token: str = Depends(oauth2_scheme)) -> None:
    dictt = client_data.dict()
    CLIENT_ID = dictt["client_id"]
    CLIENT_KEY = dictt["client_secret_key"]
    print(CLIENT_ID, CLIENT_KEY)
    real_keycloak_openid, pseudo_token_endpoint = get_Actual_keycloak_data(CLIENT_ID, CLIENT_KEY)
    token = real_keycloak_openid.token(grant_type="client_credentials")
    print("---")
    #print(token)
    print("---")
    auth_status = await get_token_status(token["access_token"],real_keycloak_openid)
    is_logged = auth_status.is_logged_in
    is_authorized = auth_status.is_authorized

# Получаем значение токена доступа из ответа
    access_token = token["access_token"]
    print(access_token)
    print("\n")
    user_info = real_keycloak_openid.introspect(access_token)
    print(user_info)
    print("---")
    print(auth_status)
    #print(token_endpoint)
    print("---")

    if not is_logged:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not is_authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    print(token_endpoint)
    return {"status": "ok"}


@app.post("/predictions")
async def predictions(instance: Instance, client_data: ClientData, token: str = Depends(check_token)) -> dict[str, float]:
    
    return make_inference(load_model(model_path), instance.dict())
