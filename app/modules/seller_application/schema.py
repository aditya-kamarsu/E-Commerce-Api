from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modules.seller_application.utils import SellerApplicationStatus


class CreateSellerApplication(BaseModel):
    business_name: str
    reason: str | None = None


class SellerApplicationResponse(BaseModel):
    id: int
    user_id: int
    business_name: str
    reason: str | None
    status: SellerApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)