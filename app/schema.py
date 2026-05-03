from pydantic import BaseModel

class InputData(BaseModel):
    age: int
    sex: str
    profession: str
    province: str


# ⭐ เพิ่มอันนี้
class FeedbackData(BaseModel):
    age: int
    sex: str
    profession: str
    province: str
    customer_segment: str
    platform: str
    ad_time: str
    feedback: str   # yes / no