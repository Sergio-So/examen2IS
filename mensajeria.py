from flask import Flask, request, jsonify
app = Flask(__name__)

class Usuario:
    def __init__(self, alias, nombre, contactos=None):
        self.alias = alias
        self.nombre = nombre
        self.contactos = contactos if contactos else []
        self.mensajes = []
    
    def agregar_contacto(self, contacto):
        if contacto not in self.contactos:
            self.contactos.append(contacto)
    
    def recibir_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

BD = [
    Usuario("cpaz", "Christian", ["lmunoz", "mgrau"]),
    Usuario("lmunoz", "Luisa", ["mgrau"]),
    Usuario("mgrau", "Miguel", ["cpaz"])
]

@app.route('/mensajeria/contactos', methods=['GET'])
def obtener_contactos():
    mialias = request.args.get('mialias')
    usuario = next((u for u in BD if u.alias == mialias), None)
    
    if usuario:
        return jsonify({contacto: next((u.nombre for u in BD if u.alias == contacto), None) for contacto in usuario.contactos})
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    data = request.get_json()
    contacto = data['contacto']
    nombre = data['nombre']
    
    # Buscar si el alias existe
    usuario = next((u for u in BD if u.alias == alias), None)
    
    if usuario:
        usuario.agregar_contacto(contacto)
    else:
        nuevo_usuario = Usuario(alias, nombre, [contacto])
        BD.append(nuevo_usuario)
    
    return jsonify({"message": "Contacto añadido exitosamente"})

@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    usuario_alias = data['usuario']
    contacto_alias = data['contacto']
    mensaje = data['mensaje']
    
    usuario = next((u for u in BD if u.alias == usuario_alias), None)
    contacto = next((u for u in BD if u.alias == contacto_alias), None)
    
    if usuario and contacto and contacto_alias in usuario.contactos:
        mensaje_info = {"usuario": usuario.nombre, "mensaje": mensaje}
        contacto.recibir_mensaje(mensaje_info)
        return jsonify({"message": "Mensaje enviado exitosamente"})
    else:
        return jsonify({"error": "Usuario o contacto no encontrado o no está en los contactos"}), 400

@app.route('/mensajeria/recibidos', methods=['GET'])
def recibir_mensajes():
    mialias = request.args.get('mialias')
    usuario = next((u for u in BD if u.alias == mialias), None)
    
    if usuario:
        mensajes = [{"usuario": m["usuario"], "mensaje": m["mensaje"]} for m in usuario.mensajes]
        return jsonify(mensajes)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
