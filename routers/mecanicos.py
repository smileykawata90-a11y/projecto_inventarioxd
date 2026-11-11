from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.schemas import MecanicoCreate, MecanicoResponse
from models.mecanico import Mecanico
from dependencias.dependencias import obtener_bd, verificar_gerente, verificar_auditor, parametros_paginacion

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])

@router.get("/", response_model=list[MecanicoResponse])
async def obtener_mecanicos(
    db: AsyncSession = Depends(obtener_bd),
    paginacion: dict = Depends(parametros_paginacion),
    rol: str = Depends(verificar_auditor)
):
    query = select(Mecanico).offset(paginacion["skip"]).limit(paginacion["limit"])
    resultado = await db.execute(query)
    return resultado.scalars().all()

@router.post("/", status_code=201)
async def crear_mecanico(
    mecanico: MecanicoCreate,
    db: AsyncSession = Depends(obtener_bd),
    rol: str = Depends(verificar_gerente)
):
    # Verificar documento duplicado
    existe = await db.execute(select(Mecanico).where(Mecanico.documento == mecanico.documento))
    if existe.scalars().first():
        raise HTTPException(status_code=400, detail="Documento ya registrado")

    nuevo = Mecanico(**mecanico.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return {"mensaje": "Mecánico creado exitosamente", "mecanico": nuevo}

@router.delete("/{id}")
async def eliminar_mecanico(
    id: int,
    db: AsyncSession = Depends(obtener_bd),
    rol: str = Depends(verificar_gerente)
):
    resultado = await db.execute(select(Mecanico).where(Mecanico.id == id))
    mecanico_db = resultado.scalars().first()
    if not mecanico_db:
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")
    await db.delete(mecanico_db)
    await db.commit()
    return {"mensaje": f"Mecánico {id} eliminado"}