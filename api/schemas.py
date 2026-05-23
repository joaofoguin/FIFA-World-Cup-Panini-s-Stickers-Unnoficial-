from pydantic import BaseModel


class FigurinhaBase(BaseModel):
    numero_album: str
    nome: str
    pais: str


class FigurinhaCreate(FigurinhaBase):
    pass


class FigurinhaUpdate(FigurinhaBase):
    pass


class FigurinhaResponse(FigurinhaBase):
    id: int

    class Config:
        from_attributes = True