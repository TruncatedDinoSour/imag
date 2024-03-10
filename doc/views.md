# views ( user access endpoints )

most of the following routes are meant mainly for user access, so they are restricted by CORS and return human readable
data, for developer access see the developer api docs

-   `GET /` - the index page, lazy-loads all images, renders `src/imag/templates/index.j2` - original origin only
-   `POST /` - posts an image to the instance, redirects to the image once uploaded, POST the following form arguments
    -   `key` - an access key with at least `write` permissions
        -   by default a master admin key is generated, see the developer api docs for more info
        -   the key length is usually going to be 128 bytes
    -   `desc` ( optional ) - description of the image
        -   the description length is usually limited to 1024 bytes
    -   `image` - the image file, only images allowed ( `image/*` mimetypes )
-   `GET /search?q=...` - search the description, edit, and creation dates of images, argument `q` required, else redirects back to `/` - original origin only
-   `GET /image/<id>` or `/image/<id>.png` or `/image/<id>.jpg` ( like `/image/69` or `/image/69.png` ) - returns the image file of the associated ID - all origins
-   `POST /edit/<image id>` - edit the image data, supports all the same arguments as `POST /`, but updates the `edited` date
