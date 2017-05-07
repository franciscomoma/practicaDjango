# Plataforma de blogging Fblog

## Reescalado de imágenes
Se ha implementado una cola de tareas para reescalar imágenes. La funcionalidad está toda en la aplicación `museum` (es completamente indpendiente de la plataforma), pero para aprovecharla se ha creado la aplicación `gallery`, la cual implementa las tareas en segundo plano y los endpoints para crear imágenes.

Para reescalar imágenes, es necesario crear tamaños a través del admin de Django (no se implementan endpoints porque es una tarea administrativa la cual tampoco va a ser usada en demasiadas ocasiones). 

Una vez haya creados tamaños, bastará con arrancar Celery con los settings `-A gallery.tasks worker --loglevel=info` y cualquier imágen que subamos haciendo `POST` a `/api/1.0/images` creará una nueva imagen y tantos tamaños de imagen como tamaños haya definidos salvo que la imagen sea menor a alguno de estos.

Aunque en las especificaciones se dice que la imagen original será descartada, he decidido no hacerlo porque puede ser que, en un momento dado, necesitemos cambiar los tamaños de imagen en nuestra plataforma debido a un cambio en el diseño gráfico, de modo que hay un comando de Django que regenera todas los tamaños de imagen. Se lanza con `python manage.py resize_all_images`.

PD.: La aplicación `museum` es susceptible de ir en un repositorio aparte debido a su autonomía del resto del sistema, por lo tanto, sus dependencias están definidas en su propio `requirements.txt`. No olvides instalarlas también antes de usar esta funcionalidad.
