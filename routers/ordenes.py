from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from schemas.schemas import OrdenCreate, OrdenPatch, OrdenUpdate, OrdenResponse
from models.orden import Orden
from dependencias.dependencias import obtener_bd, verificar_api_key, parametros_paginacion

router = APIRouter(prefix="/ordenes", tags=["Gestionar ordenes"])

@router.get("/", response_model=list[OrdenResponse])
async def obtener_ordenes(
    db: AsyncSession = Depends(obtener_bd),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    modelo: Optional[str] = Query(None, description="Filtrar por modelo ej: Bajaj"),
    costo_minimo: Optional[float] = Query(None, ge=0, description="Costo minimo")
):
    query = select(Orden)

    if estado:
        query = query.where(Orden.estado.ilike(f"%{estado}%"))
    if modelo:
        query = query.where(Orden.modelo.ilike(f"%{modelo}%"))
    if costo_minimo is not None:
        query = query.where(Orden.costo_reparacion >= costo_minimo)

    resultado = await db.execute(query)
    ordenes = resultado.scalars().all()
    return ordenes

@router.post("/", status_code=201)
async def crear_orden(
    orden: OrdenCreate,
    db: AsyncSession = Depends(obtener_bd),
    api_key: str = Depends(verificar_api_key)
):
    # Verificar si la moto ya está en el taller y no entregada
    query = select(Orden).where(Orden.placa == orden.placa, Orden.estado != "Entregada")
    resultado = await db.execute(query)
    existente = resultado.scalars().first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail=f"La moto con placa {orden.placa} ya se encuentra en el taller ({existente.estado})."
        )

    nueva_orden = Orden(
        placa=orden.placa,
        modelo=orden.modelo,
        falla_reportada=orden.falla_reportada,
        estado="En diagnóstico",
        costo_reparacion=0.0
    )
    db.add(nueva_orden)
    await db.commit()
    await db.refresh(nueva_orden)

    return {"mensaje": "Orden creada exitosamente", "orden": nueva_orden, "llave usada": api_key}

@router.get("/paginadas")
async def obtener_ordenes_paginadas(
    db: AsyncSession = Depends(obtener_bd),
    paginacion: dict = Depends(parametros_paginacion)
):
    skip = paginacion["skip"]
    limit = paginacion["limit"]

    query = select(Orden).offset(skip).limit(limit)
    resultado = await db.execute(query)
    ordenes = resultado.scalars().all()

    total = await db.execute(select(Orden))
    total_bd = len(total.scalars().all())

    return {
        "mostrando": len(ordenes),
        "total_bd": total_bd,
        "skip": skip,
        "limit": limit,
        "ordenes": ordenes
    }

@router.put("/{placa}")
async def actualizar_orden(placa: str, orden_update: OrdenUpdate, db: AsyncSession = Depends(obtener_bd)):
    query = select(Orden).where(Orden.placa == placa)
    resultado = await db.execute(query)
    orden_db = resultado.scalars().first()

    if not orden_db:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    orden_db.estado = orden_update.nuevo_estado
    orden_db.costo_reparacion = orden_update.costo_reparacion
    await db.commit()
    await db.refresh(orden_db)
    return {"mensaje": "Orden actualizada correctamente", "orden": orden_db}

@router.delete("/{placa}", status_code=204)
async def eliminar_orden(placa: str, db: AsyncSession = Depends(obtener_bd)):
    query = select(Orden).where(Orden.placa == placa)
    resultado = await db.execute(query)
    orden_db = resultado.scalars().first()

    if not orden_db:
        raise HTTPException(status_code=404, detail="La orden no existe.")

    await db.delete(orden_db)
    await db.commit()
    return None

@router.patch("/{placa}")
async def actualizacion_parcial(placa: str, orden_patch: OrdenPatch, db: AsyncSession = Depends(obtener_bd)):
    query = select(Orden).where(Orden.placa == placa)
    resultado = await db.execute(query)
    orden_db = resultado.scalars().first()

    if not orden_db:
        raise HTTPException(status_code=404, detail="La orden no existe.")

    datos_a_actualizar = orden_patch.model_dump(exclude_unset=True)
    # Mapeamos nuevo_estado -> estado porque en la BD se llama estado
    if "nuevo_estado" in datos_a_actualizar:
        orden_db.estado = datos_a_actualizar.pop("nuevo_estado")
    for campo, valor in datos_a_actualizar.items():
        setattr(orden_db, campo, valor)

    await db.commit()
    await db.refresh(orden_db)
    return {"mensaje": "La orden ha sido actualizada", "orden": orden_db}