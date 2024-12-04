# examen2IS
Examen 2 de ingenería de software

python3 -m coverage run      
Output:      
![Pytest1](images/pts.png)
python3 -m coverage report      
Output:      
![Pytest2](images/pytest2.png)


3. Cambios sugeridos :
    Agergar los métodos eliminar contacto y usuario
    tener una variable que sea el limite de contactos que pueda tener una persona.

Métodos nuevos : 

Eliminar_usuario()
Eliminar_contacto()

Casos de prueba adicionales :

Intentar agregar más contactos de los permitidos (por ejemplo, 11 contactos cuando si la cantidad de contactos máxima es 10).
Eliminar un contacto de la lista de contactos de un usuario
Asegurarse de que los mensajes ya enviados a un contacto eliminado sean preservados.

Cuánto riesgo hay de “romper” lo que ya funciona?

. Si se elimina un usuario, se debe asegurar que la eliminación no afecte los mensajes que se haya enviado a otros de sus contactos
. Riesgo bajo: Si la validación de contactos se implementa correctamente, no debería afectar la funcionalidad actual.
. Riesgo moderado: La eliminación de usuarios podría afectar el acceso a mensajes si no se maneja correctamente.
