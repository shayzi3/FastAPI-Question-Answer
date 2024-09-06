
from fastapi.security import OAuth2PasswordBearer


oauth2 = OAuth2PasswordBearer(tokenUrl='api/v1/token/')