# Note Storage API

API Endpoint (Choose one, they are the same. `sodas.tw` comes with CloudFlare, 
so it would be faster):
- https://notes.sodas.tw
- https://sodas-note-storage.herokuapp.com

This is a JSON REST API, so data would be transferred in `application/json` content type.


## Paths

+ `/signup`
  - method: `POST`
  - required fields: `username`, `password`, and `email`
  - resonse: A dictionary with `username` and `email` of registered user.

+ `/notes`
  - method: `GET` (list notes) and `POST` (create notes)
  - Use `HTTP Basic Authentication` with username and password.
  - required fields:
    * `POST` - `title` and `content`.
  
+ `/notes/<UUID of notes>`
  - method: `GET` (retrieve a note), `PUT` (update/replace a note), 
    `PATCH` (partial-update a note), and `DELETE` (destroy a note)
  - Use `HTTP Basic Authentication` with username and password.
