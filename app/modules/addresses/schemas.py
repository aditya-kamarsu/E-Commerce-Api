


from pydantic import BaseModel, ConfigDict


class CreateAddress(BaseModel):
    type: str
    name: str
    phone_number: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    postal_code: str
    country: str = "India"
    is_default: bool = False


class UpdateAddress(BaseModel):
    type: str | None = None
    name: str | None = None
    phone_number: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    country: str | None = None
    is_default: bool | None = None


class AddressResponse(BaseModel):
    id: int
    user_id: int
    type: str
    name: str
    phone_number: str
    address_line1: str
    address_line2: str | None
    city: str
    state: str
    postal_code: str
    country: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)