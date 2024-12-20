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

    def enviar_mensaje(self, contacto, mensaje):
        if contacto not in self.contactos:
            raise ValueError("Contacto no está en la lista de contactos")
        self.mensajes.append({"contacto": contacto, "mensaje": mensaje})
        print(f"Mensaje enviado a {contacto}: {mensaje}")

    def recibir_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

    def ver_mensajes_enviados(self):
        return [{"contacto": m["contacto"], "mensaje": m["mensaje"]} for m in self.mensajes]

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
        usuario.enviar_mensaje(contacto_alias, mensaje)
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


@app.route('/mensajeria/enviados', methods=['GET'])
def ver_mensajes_enviados():
    mialias = request.args.get('mialias')
    usuario = next((u for u in BD if u.alias == mialias), None)
    
    if usuario:
        mensajes_enviados = usuario.ver_mensajes_enviados()
        return jsonify(mensajes_enviados)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
