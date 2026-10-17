import asyncio
import json
import aiofiles
from database import crear_producto, vender_producto

async def ejecutar_venta_segura(codigo, cantidad):
    try:
        resultado = await vender_producto(codigo, cantidad)
        print(f"Venta OK: {resultado}")
    except KeyError as e:
        print(f"Error KeyError: {e}")
    except ValueError as e:
        print(f"Error ValueError: {e}")

async def prueba_de_estres():
    async with aiofiles.open("inventario.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps([], indent=4))
    
    await asyncio.gather(
        crear_producto("M001", "Llanta trasera", 10),
        crear_producto("M002", "Filtro de aire", 25)
    )
    print("Productos creados")

    await asyncio.gather(
        ejecutar_venta_segura("M001", 2),
        ejecutar_venta_segura("M001", 6),
        ejecutar_venta_segura("M001", 20),
        ejecutar_venta_segura("M999", 1)
    )

    await asyncio.sleep(3)

asyncio.run(prueba_de_estres())