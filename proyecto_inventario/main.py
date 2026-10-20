from fastapi import FastAPI, HTTPException
from database import leer_base_datos, obtener_producto



# inicializar la app
app = FastAPI(
    title="API SENAS SENITAS",
    description="Mi primera API asíncrona",
    version="1.0.0"
)

# nuestra primer endpoint
@app.get("/")
async def ruta_principal():
    return {"mensaje": "¡Bienvenido a mi API rest!"}

@app.get("/estado")
async def estado_servidor():
    return {"status": "linea", "servicios": "operativos"}

@app.get("/suma")
async def sumar():
    numero1 = 5
    numero2 = 4
    resultado = numero1 + numero2
    return  resultado
@app.get("/productos")
async def listar_productos():
    datos = await leer_base_datos()
    return{"cantidad": len(datos), "productos": datos}
@app.get("/productos/{codigo_producto}")
async def buscar_un_producto(codigo_producto: str):
    try:
        # Para llamar a la función de obtener producto
        producto = await obtener_producto(codigo_producto)
        return producto
    except KeyError:
        raise HTTPException(status_code=404, detail="El producto solicitado no existe en la BD")