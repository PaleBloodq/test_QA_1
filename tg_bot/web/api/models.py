from pydantic import BaseModel


class NewMessage(BaseModel):
    order_number: str
    text: str
    user_id: int

class NewPayment(BaseModel):
    order_number: str
    user_id: int
    need_account: bool