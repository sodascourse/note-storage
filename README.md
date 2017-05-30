# Note Storage API

API Endpoint (Choose one, they are the same. `sodas.tw` comes with CloudFlare,
so it would be faster):

- https://notes.sodas.tw
- https://sodas-note-storage.herokuapp.com

This is a JSON REST API, so data would be transferred in `application/json` content type.


## Paths

- `/signup`
  - method: `POST`
  - required fields:
    - `POST` - `username`, `password`, and `email`
  - resonse:
    - `POST` - A dictionary with `username` and `email` of registered user.

- `/notes`
  - method: `GET` (list notes) and `POST` (create notes)
  - Use `HTTP Basic Authentication` with username and password.
  - required fields:
    - `GET` - N/A
    - `POST` - N/A, but usually have `title` and `content`.
  - response:
    - `GET` - A list of dictionaries, which has `modified_time`, `title`, and `uuid` of a note.
    - `POST` - A dictionary which has `modified_time`, `title`, `content`, and `uuid` of the created note.

- `/notes/<UUID of notes>`
  - method: `GET` (retrieve a note), `PUT` (update/replace a note),
    `PATCH` (partial-update a note), and `DELETE` (destroy a note)
  - Use `HTTP Basic Authentication` with username and password.
  - required fields:
    - `PUT` - N/A, but usually have `title` and `content`.
    - Others - N/A
  - response:
    - `GET`, `PUT`, and `PATCH` - A dictionary which has `modified_time`, `title`, `content`,
                                  and `uuid` of the created note.
    - `DELETE` - N/A
