
# Diagrama de classes - Projecte Flaskr

## Objectiu

Aquest document representa el diagrama de classes
del projecte Flaskr. Mostra les classes User i Post,
els seus atributs, mètodes i les seves relacions.

## Diagrama UML

```mermaid
classDiagram
    class User {
        +INTEGER id
        +TEXT username
        -TEXT password
        +register()
        +login()
        +logout()
    }

    class Post {
        +INTEGER id
        +INTEGER author_id
        +TIMESTAMP created
        +TEXT title
        +TEXT body
        +create()
        +update()
        +delete()
    }

    User "1" --> "0..*" Post : crea
```
