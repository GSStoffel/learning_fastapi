from datetime import timedelta, datetime

from jose import jwt

SECRET_KEY = "a3fcb2e93a5e49059c12f0d9d3c4f69e2f7a905bd735e77efcc491829cccfb80"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    jwt_encode = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_encode
