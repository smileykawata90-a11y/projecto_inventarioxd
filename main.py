from fastapi import FastAPI, Depends
from routers.ordenes import router as router_ordenes
from routers.mecanicos import router as router_mecanicos
from deoendencias.dependencias import simular_base_datos

app = FastAPI(
    title="API DE REPARACION DE MOTOS ASI BIEN EPICA XD",
    description="Sistema de triaje y facturación asi bien epica xd ",
    version="1.0"
)

app.include_router(router_ordenes)
app.include_router(router_mecanicos)

@app.get("/prueba-yield")
async def probar_yield(conexion=Depends(simular_base_datos)):
    print("2. [RUTA] Ejecutando la ruta. Estado: Conexión simulada")
    return {"mensaje": "Conexión simulada", "conexion": conexion}