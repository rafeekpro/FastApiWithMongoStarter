from .rwmodel import RWModel

class Classification(RWModel):
    country: str = ""
    value: str = ""

class ClassificationInResponse(RWModel):
    classification: Classification
