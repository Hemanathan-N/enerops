from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=True)

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    # Mock JWT Decoder for Phase 4 MVP Setup
    # A Bearer token equals "MOCK_TOKEN_{ROLE}"
    
    token = credentials.credentials
    if token == "MOCK_TOKEN_ADMIN":
        return {"username": "admin_user", "role": "admin"}
    elif token == "MOCK_TOKEN_MANAGER":
        return {"username": "plant_manager", "role": "manager"}
    elif token == "MOCK_TOKEN_OPERATOR":
        return {"username": "line_operator", "role": "operator"}
    
    raise HTTPException(status_code=401, detail="Invalid Mock Bearer Token")
