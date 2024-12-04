from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

class Usuario:
    def __init__(self, alias, nombre, contactos=None):
        self.alias = alias
        self.nombre = nombre
        self.contactos = contactos if contactos else []
        self.mensajes_recibidos = []

    def agregar_contacto(self, contacto, nombre_contacto=None):
        if contacto not in self.contactos:
            self.contactos.append(contacto)
            return True
        return False

    def recibir_mensaje(self, mensaje):
        self.mensajes_recibidos.append(mensaje)

BD = [
    Usuario("cpaz", "Christian", ["lmunoz", "mgrau"]),
    Usuario("lmunoz", "Luisa", ["mgrau"]),
    Usuario("mgrau", "Miguel", ["cpaz"]),
]

def obtener_usuario(alias):
    for usuario in BD:
        if usuario.alias.strip() == alias.strip():
            return usuario
    return None

@app.route('/mensajeria/contactos', methods=['GET'])
def obtener_contactos():
    alias = request.args.get('mialias')
    usuario = obtener_usuario(alias)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    contactos = {contacto: obtener_usuario(contacto).nombre for contacto in usuario.contactos}
    return jsonify(contactos)

@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    data = request.json
    contacto = data.get('contacto')
    nombre = data.get('nombre')
    
    usuario = obtener_usuario(alias)
    if not usuario:
        usuario = Usuario(alias, alias)  
        BD.append(usuario)
    if usuario.agregar_contacto(contacto, nombre):
        if nombre:  
            print(usuario.contactos)
            return jsonify({"mensaje": f"Contacto {contacto} agregado con éxito"}), 201
        return jsonify({"mensaje": f"Contacto {contacto} ya estaba en la lista"}), 200
    return jsonify({"error": "El contacto ya existe en la lista"}), 400

@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.json
    usuario_alias = data.get('usuario')
    contacto_alias = data.get('contacto')
    mensaje_texto = data.get('mensaje')
    
    usuario = obtener_usuario(usuario_alias)
    if not usuario:
        return jsonify({"error": "El usuario que envía no existe"}), 404
    
    if contacto_alias not in usuario.contactos:
        return jsonify({"error": "El contacto no está en la lista de contactos"}), 400
    
    contacto = obtener_usuario(contacto_alias)
    if not contacto:
        return jsonify({"error": "El contacto no existe en la base de datos"}), 404
    
    mensaje = {
        "remitente": usuario_alias,
        "mensaje": mensaje_texto,
        "fecha": datetime.now().strftime('%d/%m/%y %H:%M')
    }
    contacto.recibir_mensaje(mensaje)
    
    return jsonify({"mensaje": f"Mensaje enviado a {contacto_alias}"}), 200

@app.route('/mensajeria/recibidos', methods=['GET'])
def obtener_mensajes_recibidos():
    alias = request.args.get('mialias')
    usuario = obtener_usuario(alias)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    mensajes = []
    for mensaje in usuario.mensajes_recibidos:
        mensajes.append(f"{mensaje['remitente']} te escribió: \"{mensaje['mensaje']}\" el {mensaje['fecha']}.")
    
    return jsonify(mensajes)

if __name__ == '__main__':
    app.run(debug=True)
