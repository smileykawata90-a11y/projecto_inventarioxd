from fastapi import Header, Query, HTTPException

async def verficar_api_key(
    x_api_key: str = Header(..., description="API Key secreta para el taller")
):
    if x_api_key != "sena2026":
        raise HTTPException(status_code=401, detail="API Key inválida")
    return x_api_key


verificar_api_key = verficar_api_key

def parametros_paginacion(
    skip: int = Query(0, description="Cuantos registros saltar"),
    limit: int = Query(10, description="Límite de registros a devolver")
):
    return {"skip": skip, "limit": limit}

async def simular_base_datos():
    print("Simulando acceso a la base de datos...")
    yield "(conexión lista)"
    print("Cerrando la conexión simulada a la base de datos...")



async def verificar_gerente(x_role: str = Header(..., description="Rol del usuario")):
    if x_role != "Gerente":
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol Gerente")
    return x_role

async def verificar_auditor(x_role: str = Header(..., description="Rol del usuario")):
    if x_role not in ["Gerente", "Auditor"]:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol Gerente o Auditor")
    return x_role