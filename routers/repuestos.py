from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.schemas import RepuestoCreate, RepuestoResponse
from models.repuesto import Repuesto
from dependencias.dependencias import obtener_bd, verificar_gerente, verificar_auditor, parametros_paginacion

router = APIRouter(prefix="/repuestos", tags=["Repuestos"])

@router.get("/", response_model=list[RepuestoResponse])
async def obtener_repuestos(
    db: AsyncSession = Depends(obtener_bd),
    paginacion: dict = Depends(parametros_paginacion),
    rol: str = Depends(verificar_auditor)
):
    query = select(Repuesto).offset(paginacion["skip"]).limit(paginacion["limit"])
    resultado = await db.execute(query)
    return resultado.scalars().all()

@router.post("/", status_code=201)
async def crear_repuesto(
    repuesto: RepuestoCreate,
    db: AsyncSession = Depends(obtener_bd),
    rol: str = Depends(verificar_gerente)
):
    existe = await db.execute(select(Repuesto).where(Repuesto.codigo == repuesto.codigo))
    if existe.scalars().first():
        raise HTTPException(status_code=400, detail="Código ya registrado")
    nuevo = Repuesto(**repuesto.model_dump())
    db.add(nuevo)
    await db.commit()
    await db.refresh(nuevo)
    return {"mensaje": "Repuesto creado exitosamente", "repuesto": nuevo}

@router.delete("/{id}")
async def eliminar_repuesto(
    id: int,
    db: AsyncSession = Depends(obtener_bd),
    rol: str = Depends(verificar_gerente)
):
    resultado = await db.execute(select(Repuesto).where(Repuesto.id == id))
    repuesto_db = resultado.scalars().first()
    if not repuesto_db:
        raise HTTPException(status_code=404, detail="Repuesto no encontrado")
    await db.delete(repuesto_db)
    await db.commit()
    return {"mensaje": f"Repuesto {id} eliminado"}