import json
import aiofiles
import asyncio

ARCHIVO_BD = "inventario.json"
db_lock = asyncio.Lock()

async def leer_base_datos():
    try:
        async with aiofiles.open(ARCHIVO_BD, mode="r", encoding="utf-8") as f:
            contenido = await f.read()
            return json.loads(contenido) if contenido else []
    except FileNotFoundError:
        return []

async def guardar_base_datos(datos):
    async with aiofiles.open(ARCHIVO_BD, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(datos, indent=4))

async def crear_producto(codigo, nombre, stock):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        for dato in datos:
            if dato["codigo"] == codigo:
                raise ValueError(f"El producto con el código {codigo} ya existe.")
        nuevo_producto = {"codigo": codigo, "nombre": nombre, "stock": stock}
        datos.append(nuevo_producto)
        await guardar_base_datos(datos)
        return nuevo_producto

async def obtener_producto(codigo):
    async with db_lock:
        await asyncio.sleep(0.2)
        datos = await leer_base_datos()
        for dato in datos:
            if dato["codigo"] == codigo:
                return dato
        raise KeyError(f"Producto {codigo} no ha sido encontrado.")

async def actualizar_stock(nuevo_stock, codigo):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        for dato in datos:
            if dato["codigo"] == codigo:
                dato["stock"] = nuevo_stock
                await guardar_base_datos(datos)
                return dato
        raise KeyError(f"Producto {codigo} no ha sido encontrado perdiste pupu xdddd como yo la perdi a ella.... .")

async def eliminar_producto(codigo):
    async with db_lock:
        await asyncio.sleep(0.5)
        datos = await leer_base_datos()
        nuevos_datos = [dato for dato in datos if dato["codigo"] != codigo]
        if len(datos) == len(nuevos_datos):
            raise KeyError(f"Producto {codigo} no ha sido encontrado.")
        await guardar_base_datos(nuevos_datos)
        return True

async def alerta_stock_bajo(codigo, nombre, stock_actual):
    await asyncio.sleep(2)
    print(f"ALERTA CRITICA: El producto {nombre} ({codigo}) ha bajado a {stock_actual} unidades. Solicitar restock inmediato.")

async def vender_producto(codigo, cantidad_vendida):
    async with db_lock:
        datos = await leer_base_datos()
        producto = None
        for d in datos:
            if d["codigo"] == codigo:
                producto = d
                break
        if not producto:
            raise KeyError("Producto no encontrado")
        if cantidad_vendida > producto["stock"]:
            raise ValueError("Stock insuficiente")
        producto["stock"] -= cantidad_vendida
        await guardar_base_datos(datos)
        if producto["stock"] < 3:
            asyncio.create_task(alerta_stock_bajo(codigo, producto["nombre"], producto["stock"]))
        return {"mensaje": "Venta exitosa", "producto": producto["nombre"], "stock_restante": producto["stock"]}