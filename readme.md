# Plataforma de blogging Fblog

## Notificaciones por email
La plataforma está preparada para lanzar notificaciones por email pero no está implementado ningún backend de envío de emails.

Solamente se enviarán notificaciones al crear un post nuevo (nunca al editar) y siempre y cuando el post sea una contestación a otro post (se crean contestaciones creando un nuevo post en la url `/api/1.0/<blog_id>/posts/<post_id>/reply/`) o mencionando un usuario con `@username` en el cuerpo del post, siempre y cuando ni el post relacionado ni el usuario mencionado sea el propio usuario dueño del post.

Para comprobar esta funcionalidad, lanzar el script `email_sender.js` (después de haber instalado sus dependencias con `npm install`) el cual está suscrito a las publicaciones de emails lanzadas desde la plataforma.

Además, para probarlo rápido, símplemente ejecuta los tests y verás los emails que estos envían.
