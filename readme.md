# Sistema de Informacion para documentos de proyectos

## Descripcion

Este proyecto tiene como objetivo almacenar de manera segura y ordenada los documentos de distintos proyectos, implementando un control de versiones para cada uno de ellos.


## Uso
Si deseas utilizar esta aplicación, puedes abrir el archivo ejecutable o ejecutar el archivo main.py en la terminal de comandos con el siguiente comando:

```bash
SDI-DocumentosLisduer/Scripts/activate.bat
python src/main.py
```

## Mecanismo de Encriptación
El mecanismo de encriptación está diseñado para garantizar que la información sensible, como claves y contraseñas, no se almacene en texto plano. A continuación se detalla su funcionamiento:

1. **Generación y Almacenamiento de Claves**:
   - Al inicializar la base de datos, el sistema registra un usuario administrador y genera una clave aleatoria. Esta clave se hashea y se almacena en la tabla "Llaves" de la base de datos.
   - La contraseña se utiliza como clave de desencriptación, asegurando que la clave real no pueda ser extraída fácilmente.

2. **Gestión de Sesiones**:
   - La contraseña desencriptada puede almacenarse como una variable de sesión, permitiendo un acceso seguro durante las operaciones sin exponerla.

3. **Encriptación/Desencriptación de Documentos**:
   - Al encriptar o desencriptar un documento, el sistema verifica las variables de sesión para recuperar la clave aleatoria. Esta clave se utiliza como clave de encriptación para los documentos.
   - Si se crea una nueva cuenta de usuario, el sistema desencripta la clave maestra y la vuelve a encriptar con la clave del nuevo usuario, asegurando que no se almacene información desencriptada en la base de datos.




