from pydantic import BaseModel
from typing import List


class CanonPreview(BaseModel):
    model: str
    price: str
    detailed_link: str
    category: str


class ImageURLS(BaseModel):
    images: List[str]
