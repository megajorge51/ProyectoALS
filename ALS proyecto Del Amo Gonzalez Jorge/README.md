# Links management web

## Intro

Una web de demostración sobre el manejo de enlaces url creada con Flask.

<i>A demo web for managing url links, created with Flask.</i>

## Build

Solo tienes que instalar **Flask** y algunas dependencias y ejecutar `app.py`.

<i>Just install **Flask** and some dependencies and execute `app.py`.</i>

```bash
$ pip install -U -r requirements.txt
$ python app.py
```

El proyecto fue creado con **PyCharm**, pero puede utilizarse cualquier otro IDE.

<i>The project was created with **PyCharm**, but you can use any IDE you need.</i>

## Deploy

Al ejecutarse, el programa generará una excepción debido a que no será capaz de enontrar el archivo de configuración `instance/config.json`. Esto es debido a que en este archivo se guarda la clave secreta de la app, y por ello no tiene sentido distribuirla.

*On first execution, the programm will complain about a missing `instance/config.json` file with an exception. This is due to this file containing the secret key of the app, and therefore it does not make any sense to distribute it.*

Será necesario proporcionar un archivo `instance/config.json` con el contenido de la `SECRET_KEY', por ejemplo:

*You will have to create your own `instance/config.json`file, with the contents of the `SECRET_KEY`, for instance:*

```json
{
  "SECRET_KEY"="Lalala"
}
```

Por supuesto, en una aplicación real, sería conveniente aportar una clave también real, más compleja.

*Of couse, in a real application you should consider to include a proper, more complex key.*
