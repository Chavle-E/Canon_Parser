from pydantic import BaseModel


class CanonPreview(BaseModel):
    model: str
    price: str
    category: str
    detailed_link: str
