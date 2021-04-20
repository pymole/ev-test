from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBasic

import settings


api_key_header = APIKeyHeader(name='API-Key')


def check_admin_authentication_header(api_key: str = Depends(api_key_header)):

    if api_key == settings.global_settings.admin_api_key:
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


http_basic = HTTPBasic()
