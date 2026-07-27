


from datetime import UTC, datetime, timedelta

import jwt


SECRET_KEY = "fc00ec899c2aea9909a2cb05a6db940dfe768c0787245e4368339b39a76b9871"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict)->str:
    to_encode = data.copy()
    expire = datetime.now(UTC)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
