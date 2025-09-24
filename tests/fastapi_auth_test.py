from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

bearer = HTTPBearer(auto_error=False)


class Auth:

    @staticmethod
    def verify_token(creds: HTTPAuthorizationCredentials | None = Security(bearer)):
        if creds is None or not creds.credentials or creds.scheme.lower() != "bearer":
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Missing or invalid auth")
        token = creds.credentials
        # 在这里校验 token（示例中直接通过）
        if token != "secret-token":
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return token
