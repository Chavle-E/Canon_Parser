from pydantic import BaseModel
from typing import List


class CanonPreview(BaseModel):
    model: str
    price: str
    category: str
    detailed_link: str


class ImageURLS(BaseModel):
    images: List[str]
