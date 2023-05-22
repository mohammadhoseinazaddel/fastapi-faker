from pydantic import BaseModel


class Transfer(BaseModel):
    transfer_id: str
    transfer_mode: str | None
    destination_IBAN: str
    destination_first_name: str | None
    destination_last_name: str | None
    amount: int
    description: str
    metadata: str | None
    notify_url: str | None
    cancellable: bool | None
    payment_id: str | None
