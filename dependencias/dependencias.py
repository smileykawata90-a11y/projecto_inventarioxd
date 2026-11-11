from fastapi import Header, Query, HTTPException, Depends
from core.database import SessionLocal

# 1. BASE DE DATOS REAL - Esta es la que va a usar tu main.py
async def obtener_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

# 2. SEGURIDAD - API Key del taller
async def verificar_api_key(
    x_api_key: str = Header(..., description="API Key secreta para el taller")
):
    if x_api_key != "sena2026":
        raise HTTPException(status_code=401, detail="API Key inválida")
    return x_api_key

# 3. PAGINACIÓN - Para no traer 1000 órdenes de un solo golpe
def parametros_paginacion(
    skip: int = Query(0, description="Cuantos registros saltar"),
    limit: int = Query(10, description="Límite de registros a devolver")
):
    return {"skip": skip, "limit": limit}

# 4. SIMULADA - Esta ya no la necesitas, la puedes borrar, pero te la dejo por si tu profe la pide
async def simular_base_datos():
    print("Simulando acceso a la base de datos...")
    yield "(conexión lista)"
    print("Cerrando la conexión simulada a la base de datos...")

# 5. ROLES - Solo Gerente
async def verificar_gerente(x_role: str = Header(..., description="Rol del usuario")):
    if x_role != "Gerente":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol Gerente")
    return x_role

# 6. ROLES - Gerente o Auditor
async def verificar_auditor(x_role: str = Header(..., description="Rol del usuario")):
    if x_role not in ["Gerente", "Auditor"]:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol Gerente o Auditor")
    return x_role