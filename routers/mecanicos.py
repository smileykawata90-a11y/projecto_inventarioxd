from fastapi import APIRouter, Depends, HTTPException
from schemas import MecanicoCreate
from deoendencias.dependencias import verificar_gerente, verificar_auditor, parametros_paginacion
from database import leer_mecanicos, guardar_mecanicos

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])

@router.get("/")
async def obtener_mecanicos(
    paginacion: dict = Depends(parametros_paginacion),
    rol: str = Depends(verificar_auditor)
):
    datos = await leer_mecanicos()
    skip = paginacion["skip"]
    limit = paginacion["limit"]
    datos_paginados = datos[skip : skip + limit]
    return {"total_mecanicos": len(datos), "mecanicos": datos_paginados}

@router.post("/", status_code=201)
async def crear_mecanico(
    mecanico: MecanicoCreate,
    rol: str = Depends(verificar_gerente)
):
    datos = await leer_mecanicos()
    nuevo_id = max([m["id"] for m in datos], default=0) + 1
    nuevo = {"id": nuevo_id, **mecanico.model_dump()}
    datos.append(nuevo)
    await guardar_mecanicos(datos)
    return {"mensaje": "Mecánico creado exitosamente", "mecanico": nuevo}

@router.delete("/{id}")
async def eliminar_mecanico(
    id: int,
    rol: str = Depends(verificar_gerente)
):
    datos = await leer_mecanicos()
    datos_filtrados = [m for m in datos if m["id"] != id]
    if len(datos) == len(datos_filtrados):
        raise HTTPException(status_code=404, detail="Mecánico no encontrado")
    await guardar_mecanicos(datos_filtrados)
    return {"mensaje": f"Mecánico {id} eliminado"}