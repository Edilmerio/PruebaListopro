PruebaListopro es una plaaforma para lee un fichero json (events.json) con eventos
resultado de la api de Google Calendar.Este fichero debe estar ubicado en el directorio
PruebaListopro.

Pagina principal event/show_events

En la pagina principal se muestra:
1-Un calendario que recibe solo recibe los eventos desde el servidor que esten dentro de la
fecha de inicio y fin del calendario, tanto cuando se carga inicialmente como cuando se mueve adelante
o atras con los botones, inicialmente el calendario es congigurado con la fecha actual.
2-La zona horaria inicial, con a que se muestran los eventos, la coincide inicialmete con la configurada en el equipo local, ademas
da la posibilidad de cambiar la zona horaria a la deseada mediante el select TimeZone
3-Cuando se da click sobre un evento dentro del caledario se muestra un popover con la informacion
detallada del evento
4-Boton Load Events from File que permite de forma asincrona leer el fichero events.json, insertar
los nuevos eventos, actualizar los existentes utilizando como identificador el id del evento
enviado por la api Google Calendar y recargar el calendario con los cambios.

En el fichero PruebaListopro/log se escriben los log del sistema

1- Instalar python version 3.6 o superior
2-Instalar yarn
3- Clonar el proyecto (git clone https://github.com/Edilmerio/PruebaListopro.git)
4- Crear entorno virtul (python -m venv venv)
5- Activar venv
6- Ubicarse en el directorio PruebaListopro/
7- Run pip install -r requirements.txt
8- Run yarn install --flat
9- Run python manage.py makemigrations
10- Run python manage.py migrate
11-Run python manage.py collectstatic for production environment
12-Crear y cargar en el fichero PruebaListopro/events.json el JSON de los eventos de google calendar