import pytest
from mensajeria import Usuario  # Asegúrate de importar las clases correctas

# Caso de prueba 1: Prueba de éxito al obtener contactos
def test_obtener_contactos_exito():
    usuario = Usuario("cpaz", "Christian", ["lmunoz", "mgrau"])
    assert usuario.contactos == ["lmunoz", "mgrau"]

# Caso de prueba 2: Prueba de éxito al enviar un mensaje
def test_enviar_mensaje_exito():
    usuario = Usuario("cpaz", "Christian", ["lmunoz"])
    usuario.enviar_mensaje("lmunoz", "¡Hola, Luisa!")
    assert len(usuario.mensajes) == 1
    assert usuario.mensajes[0]['mensaje'] == "¡Hola, Luisa!"

# Caso de prueba 3: Prueba de éxito al agregar un contacto
def test_agregar_contacto_exito():
    usuario = Usuario("cpaz", "Christian", ["lmunoz"])
    usuario.agregar_contacto("mgrau")
    assert "mgrau" in usuario.contactos

# Caso de prueba 4: Prueba de éxito al recibir un mensaje
def test_recibir_mensaje_exito():
    usuario = Usuario("cpaz", "Christian", ["lmunoz"])
    usuario.recibir_mensaje({"usuario": "lmunoz", "mensaje": "Hola, Christian!"})
    assert len(usuario.mensajes) == 1
    assert usuario.mensajes[0]['mensaje'] == "Hola, Christian!"

# Caso de prueba 1 de error: Usuario no encontrado al intentar enviar mensaje
def test_enviar_mensaje_error_usuario_no_existe():
    usuario = Usuario("cpaz", "Christian", [])  # Usuario "cpaz" no tiene contactos
    try:
        usuario.enviar_mensaje("lmunoz", "Mensaje")
    except ValueError as e:
        assert str(e) == "Contacto no está en la lista de contactos"  # Este es el error correcto

# Caso de prueba 2 de error: Contacto no está en la lista de contactos
def test_enviar_mensaje_error_contacto_no_existe():
    usuario = Usuario("cpaz", "Christian", [])
    try:
        usuario.enviar_mensaje("mgrau", "Mensaje")
    except ValueError as e:
        assert str(e) == "Contacto no está en la lista de contactos"

# Caso de prueba 3 de error: Intentar agregar un contacto a sí mismo
def test_agregar_contacto_error_igual():
    usuario = Usuario("cpaz", "Christian", [])
    try:
        usuario.agregar_contacto("cpaz")
    except ValueError as e:
        assert str(e) == "No puedes agregar a ti mismo como contacto"
