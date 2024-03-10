# developer API

the API is meant for developers to access and use, it doesn't return human
readable data unlike the human interface

the POST APIs are based on form data requests and JSON responses

-   `GET /api/image/<id>` - get image information
-   `GET /api/search/<id>?q=...` - search in image descriptions, creation dates, and editing dates
-   `POST /api/key` - check if you can access the key api ( admin access only )
    -   `POST /api/key/new` - generate a new access key, following form arguments are required :
        -   `perm` - the permission level, usually either `write` or `admin`
    -   `POST /api/key/revoke` - revoke a key
        -   `rev` form argument is required with the value of the key being revoked
    -   `GET /api/key/keys` - list all keys and their permission levels
    -   `GET /api/key/info` - shows information about a specific key
        -   `target` - the target key

keep in mind, this is **form data**, so in for example JavaScript you'd use `FormData`, or `-F'field=value'` in curl
and whatnot
