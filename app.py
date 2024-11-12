from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import pymongo

app = Flask(__name__)
client = MongoClient("mongodb+srv://sebastian_admin:admin..@cluster0.qyojj.mongodb.net/")
db = client["Easyshop"]

productos = db["productos"]
trabajador = db["trabajador"]
cliente = db["cliente"]
boleta = db["boleta"]

@app.route('/')         #Pagina Principal
def index():
    return render_template('index.html')

@app.route('/productos')        #Pagina Productos
def pagina_productos():
    lista_productos = list(productos.find())
    for producto in lista_productos:
        producto["_id"] = str(producto["_id"])
    return render_template('productos.html', productos=lista_productos)

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    nuevo_producto = {
        "_id": request.form.get("id", ObjectId()),
        "nombre": request.form["nombre"],
        "precio": int(request.form["precio"]),
        "stock": int(request.form["stock"]),
        "categoria": request.form["categoria"],
        "descripcion": request.form.get("descripcion", "")
    }
    productos.insert_one(nuevo_producto)
    return redirect(url_for('pagina_productos'))

@app.route('/eliminar_producto/<id>', methods=['POST'])
def eliminar_producto(id):
    productos.delete_one({"_id": id})
    return redirect(url_for('pagina_productos'))

@app.route('/editar_producto/<id>', methods=['GET'])
def editar_producto(id):
    producto = productos.find_one({"_id": id})
    producto["_id"] = str(producto["_id"])
    return render_template('editar_producto.html', producto=producto)

@app.route('/actualizar_producto/<id>', methods=['POST'])
def actualizar_producto(id):
    productos.update_one(
        {"_id": id},
        {"$set": {
            "nombre": request.form["nombre"],
            "precio": int(request.form["precio"]),
            "stock": int(request.form["stock"]),
            "categoria": request.form["categoria"],
            "descripcion": request.form.get("descripcion", "")
        }}
    )
    return redirect(url_for('pagina_productos'))

@app.route('/buscar_producto', methods=['GET'])
def buscar_producto():
    criterio = request.args.get("criterio")
    valor = request.args.get("valor")

    if not valor:       # Si no hay un valor de búsqueda, redirige a la página principal de productos
        return redirect(url_for('pagina_productos'))

    if criterio == "id":
        resultados = list(productos.find({"_id": valor}))
    elif criterio == "nombre":
        resultados = list(productos.find({"nombre": {"$regex": valor, "$options": "i"}}))
    elif criterio == "categoria":
        resultados = list(productos.find({"categoria": {"$regex": valor, "$options": "i"}}))
    else:
        resultados = []

    for producto in resultados:
        producto["_id"] = str(producto["_id"])

    return render_template('productos.html', productos=resultados)

@app.route('/trabajadores')         #Pagina Trabajadores
def pagina_trabajadores():
    lista_trabajadores = list(trabajador.find())
    for t in lista_trabajadores:
        t["_id"] = str(t["_id"])
    return render_template('trabajadores.html', trabajadores=lista_trabajadores)

@app.route('/crear_trabajador', methods=['POST'])
def crear_trabajador():
    nuevo_trabajador = {
        "_id": request.form.get("id", ObjectId()),
        "nombre": request.form["nombre"],
        "tipo": request.form["tipo"],
        "contacto": {
            "telefono": request.form["telefono"],
            "email": request.form["email"]
        }
    }
    trabajador.insert_one(nuevo_trabajador)
    return redirect(url_for('pagina_trabajadores'))

@app.route('/editar_trabajador/<id>', methods=['GET'])
def editar_trabajador(id):
    t = trabajador.find_one({"_id": id})
    t["_id"] = str(t["_id"])
    return render_template('editar_trabajador.html', trabajador=t)

@app.route('/actualizar_trabajador/<id>', methods=['POST'])
def actualizar_trabajador(id):
    trabajador.update_one(
        {"_id": id},
        {"$set": {
            "nombre": request.form["nombre"],
            "tipo": request.form["tipo"],
            "contacto": {
                "telefono": request.form["telefono"],
                "email": request.form["email"]
            }
        }}
    )
    return redirect(url_for('pagina_trabajadores'))

@app.route('/eliminar_trabajador/<id>', methods=['POST'])
def eliminar_trabajador(id):
    trabajador.delete_one({"_id": id})
    return redirect(url_for('pagina_trabajadores'))

@app.route('/buscar_trabajador', methods=['GET'])
def buscar_trabajador():
    criterio = request.args.get("criterio")
    valor = request.args.get("valor")
    
    if criterio == "id":
        resultados = list(trabajador.find({"_id": valor}))
    elif criterio == "nombre":
        resultados = list(trabajador.find({"nombre": {"$regex": valor, "$options": "i"}}))
    else:
        resultados = []

    for t in resultados:
        t["_id"] = str(t["_id"])
    
    return render_template('trabajadores.html', trabajadores=resultados)

@app.route('/clientes')         #Pagina Clientes
def pagina_clientes():
    lista_clientes = list(cliente.find())
    for c in lista_clientes:
        c["_id"] = str(c["_id"])
    return render_template('clientes.html', clientes=lista_clientes)


@app.route('/crear_cliente', methods=['POST'])
def crear_cliente():
    nuevo_cliente = {
        "_id": request.form.get("id", ObjectId()),
        "nombre": request.form["nombre"]
    }
    cliente.insert_one(nuevo_cliente)
    return redirect(url_for('pagina_clientes'))

@app.route('/editar_cliente/<id>', methods=['GET'])
def editar_cliente(id):
    c = cliente.find_one({"_id": id})
    c["_id"] = str(c["_id"])
    return render_template('editar_cliente.html', cliente=c)

@app.route('/actualizar_cliente/<id>', methods=['POST'])
def actualizar_cliente(id):
    cliente.update_one(
        {"_id": id},
        {"$set": {"nombre": request.form["nombre"]}}
    )
    return redirect(url_for('pagina_clientes'))

@app.route('/eliminar_cliente/<id>', methods=['POST'])
def eliminar_cliente(id):
    cliente.delete_one({"_id": id})
    return redirect(url_for('pagina_clientes'))

@app.route('/buscar_cliente', methods=['GET'])
def buscar_cliente():
    criterio = request.args.get("criterio")
    valor = request.args.get("valor")
    
    if criterio == "id":
        resultados = list(cliente.find({"_id": valor}))
    elif criterio == "nombre":
        resultados = list(cliente.find({"nombre": {"$regex": valor, "$options": "i"}}))
    else:
        resultados = []

    for c in resultados:
        c["_id"] = str(c["_id"])
    
    return render_template('clientes.html', clientes=resultados)

@app.route('/boletas')          #Pagina Boletas
def pagina_boletas():
    lista_boletas = list(boleta.find())
    for b in lista_boletas:
        b["_id"] = str(b["_id"])

    clientes = list(cliente.find())
    trabajadores = list(trabajador.find())
    lista_productos = list(productos.find())

    return render_template('boletas.html', boletas=lista_boletas, clientes=clientes, trabajadores=trabajadores, productos=lista_productos)

@app.route('/crear_boleta', methods=['GET'])
def crear_boleta():
    clientes = list(cliente.find())
    trabajadores = list(trabajador.find())
    productos = list(productos.find())
    return render_template('crear_boleta.html', clientes=clientes, trabajadores=trabajadores, productos=productos)

@app.route('/guardar_boleta', methods=['POST'])
def guardar_boleta():
    boleta_id = request.form.get("boleta_id")
    if boleta_id:
        boleta_id = str(boleta_id)
    
    cliente_id = request.form["cliente_id"]
    trabajador_id = request.form["trabajador_id"]
    productos_comprados = []
    total = 0

    for p in productos.find():
        cantidad = request.form.get(f"cantidad_{p['_id']}")
        if cantidad and int(cantidad) > 0:
            subtotal = int(cantidad) * p["precio"]
            productos_comprados.append({
                "producto_id": str(p["_id"]),
                "nombre": p["nombre"],
                "cantidad": int(cantidad),
                "subtotal": subtotal
            })
            total += subtotal

    nueva_boleta = {
        "_id": boleta_id if boleta_id else ObjectId(),
        "cliente_id": cliente_id,
        "trabajador_id": trabajador_id,
        "productos": productos_comprados,
        "total": total,
        "fecha": datetime.datetime.now()
    }

    try:
        boleta.insert_one(nueva_boleta)
    except pymongo.errors.DuplicateKeyError:
        return "Error: El ID de la boleta ya existe. Por favor, usa otro ID.", 400

    return redirect(url_for('pagina_boletas'))

@app.route('/eliminar_boleta/<id>', methods=['POST'])
def eliminar_boleta(id):
    boleta.delete_one({"_id": id})
    return redirect(url_for('pagina_boletas'))

@app.route('/buscar_boleta', methods=['GET'])
def buscar_boleta():
    criterio = request.args.get("criterio")
    valor = request.args.get("valor")
    
    if criterio == "cliente_id":
        resultados = list(boleta.find({"cliente_id": valor}))
    elif criterio == "trabajador_id":
        resultados = list(boleta.find({"trabajador_id": valor}))
    elif criterio == "fecha":
        resultados = list(boleta.find({"fecha": {"$regex": valor}}))
    else:
        resultados = []

    for b in resultados:
        b["_id"] = str(b["_id"])

    return render_template('boletas.html', boletas=resultados)



if __name__ == '__main__':
    app.run(debug=True)