from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
app = FastAPI()

class Nombre(BaseModel):
    nombre: str


import contextlib

@contextlib.contextmanager
def conectarse_db():
    conn = sqlite3.connect('identifier.sqlite')
    try:
        yield conn  # aquí entregas la conexión para usarla
    finally:
        conn.close()  # se cierra automáticamente al terminar el bloque 'with'



conn = sqlite3.connect('identifier.sqlite')
@app.post("/name")
async def solicitar_guardarnombre(data: Nombre):

    with conectarse_db() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                         INSERT INTO nombre (nombre)
                         VALUES (?)
                     ''', (data.nombre,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return {f'No se pudo insertar a la base de datos ,error: {e}'}
        return {"nombre": data.nombre}




@app.get('/')
async def obtener_nombres():
    with conectarse_db() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM nombre
            ''')
            var = cursor.fetchall()
            var.sort()
            nombres = []
            for i in var:
                nombres.append(i[0])
            conn.close()
            return {"nombres": nombres}
        except sqlite3.Error as e:
            return {f'No se puedieron obtener los datos de la base de datos: error {e}'}
@app.get('/name/{nombre}')
async def buscar_nombre(nombre:str):
    with conectarse_db() as conn:
        try:
            var = nombre
            cursor = conn.cursor()
            cursor.execute('''SELECT * from nombre where nombre=?
               ''', (var,))
            resultado = cursor.fetchone()
            conn.commit()
            conn.close()
            if resultado:
                return {"Encontrado": nombre}
            else:
                return {"No encontrado": nombre}
        except sqlite3.Error as e:
            return {f'No se puedieron obtener los datos de la base de datos: error {e}'}


@app.delete('/eliminar/{nombre}')
async def eliminar_nombre(nombre:str):
    with conectarse_db() as conn:
        try:
            var = nombre
            cursor = conn.cursor()
            cursor.execute('''DELETE from nombre where nombre = ?
            ''', (var,))
            conn.commit()
            if cursor.rowcount > 0:
                return {"Usuario Eliminado": nombre}
            else:
                return {"Usuario no encontrado o ya eliminado": nombre}
        except sqlite3.Error as e:
            return {f'No se puedieron obtener los datos de la base de datos: error {e}'}