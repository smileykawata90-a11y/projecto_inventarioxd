from pydantic import BaseModel, Field
from typing import Optional


class MecanicoCreate(BaseModel):
    documento: str = Field(..., max_length=15)
    nombre_completo: str = Field(..., max_length=100)
    especialidad: Optional[str] = Field(None, max_length=50)

class MecanicoResponse(MecanicoCreate):
    id: int
    activo: bool
    class Config:
        from_attributes = True


class RepuestoCreate(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    precio: float = Field(..., ge=0)
    stock: int = Field(0, ge=0)

class RepuestoResponse(RepuestoCreate):
    id: int
    activo: bool
    class Config:
        from_attributes = True


class OrdenCreate(BaseModel):
    placa: str = Field(..., max_length=6)
    modelo: str
    falla_reportada: str

class OrdenUpdate(BaseModel):
    nuevo_estado: str
    costo_reparacion: float

class OrdenPatch(BaseModel):
    nuevo_estado: Optional[str] = None
    costo_reparacion: Optional[float] = None
    falla_reportada: Optional[str] = None

class OrdenResponse(BaseModel):
    id: int
    placa: str
    modelo: str
    falla_reportada: Optional[str]
    estado: str
    costo_reparacion: float
    class Config:
        from_attributes = True