from pydantic import BaseModel


class NewMessage(BaseModel):
    order_id: str
    text: str
    user_id: int

class NewPayment(BaseModel):
    order_id: str
    user_id: int
    need_account: bool
