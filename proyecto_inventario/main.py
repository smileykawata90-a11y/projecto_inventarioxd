from fastapi import FastAPI, HTTPException
from database import leer_base_datos, obtener_producto

app = FastAPI(
    title="API SENAS SENITAS",
    description="Mi primera API asincrona",
    version="1.0.0"
)

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
    return resultado

@app.get("/productos")
async def listar_productos():
    datos = await leer_base_datos()
    return {"cantidad": len(datos), "productos": datos}

@app.get("/productos/{codigo_producto}")
async def buscar_un_producto(codigo_producto: str):
    try:
        producto = await obtener_producto(codigo_producto)
        return producto
    except KeyError:
        raise HTTPException(status_code=404, detail="El producto solicitado no existe en la BD")



@app.get("/categorias")
async def obtener_categorias():
    datos = await leer_base_datos()
    categorias = set()
    for producto in datos:
      
        cat = producto.get("categoria")
        if cat:
            categorias.add(cat)
    return {"categorias": list(categorias)}

@app.get("/alertas/stock")
async def alerta_stock():
    datos = await leer_base_datos()
    productos_criticos = []
    for producto in datos:
        if producto.get("stock", 999) <= 3:
            productos_criticos.append(producto)
    return {"cantidad": len(productos_criticos), "productos": productos_criticos}

@app.get("/productos/buscar/{palabra_clave}")
async def buscar_productos(palabra_clave: str):
    datos = await leer_base_datos()
    resultados = []
    for producto in datos:
        if palabra_clave.lower() in producto.get("nombre","").lower():
            resultados.append(producto)
    return {"cantidad": len(resultados), "productos": resultados}