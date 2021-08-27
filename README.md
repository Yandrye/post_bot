# post_bot

Bot de Telegram

-Crea publicaciones ayudado por las APIS de [Anilist](https://anilist.gitbook.io/anilist-apiv2-docs/), [Visual Novel Data Base](https://vndb.org) y [IGDB](https://api-docs.igdb.com/) y las envía a un canal de Telegram.

## Información sobre copyright

### Para incluir el bot en su canal de telegram relacionado con toDus s3 se seguirá lo siguiente

- el @username del bot estará en la info de su canal
- en la info del bot habrá un link a este repo [Armando-J/post_bot](https://github.com/Armando-J/post_bot) y opcionalmente a [RathHunt/post-bot](https://github.com/RathHunt/post_bot)

## Para correrlo

    Configurar las variables de entorno:

    ID_CANAL = -100xxx (el canal donde poner los posts)

    TOKEN = el token del bot de telegram que te da [BotFather](https://t.me/BotFather)

    SUPPORT = id del grupo/canal donde se registra la interacion con el bot (para moderación)

    DATABASE_URL = dirección de la base de datos, si no te importa que se reinicie solo pon sqlite:///meh.db , si quieres persistencia busca una como elephant sql o el addon de heroku postgre

## API de Juegos

si no se colocan adecuadamente el bot inicia con la API deshabilitada

referencias en los docs

    TWITCH_CLIENT_ID
    TWITCH_CLIENT_SECRET
