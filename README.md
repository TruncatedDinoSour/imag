# imag

> simple and hackable suckless image board

the imag image board is made to be simple, though separated, so you
could easily add or remove features, update them, etc

this is not sole software, it is suckless ( ? ) software, which you are meant
to hack yourself,, you can, of course, use the default settings and whatnot,
but it is highly encouraged to make forks and hack it yourself :)

example instance : https://quotes.ari.lt/

~~i hate github versioning so much~~

# licensing

you can distribute, modify, share, redistribute, etc etc etc with no credit or anything,
this project is released under unlicense and i give away all my rights to this project :)

license : unlicense

# bot

i made a matrix bot to integrate well with this, it is open source : <https://ari.lt/gh/quotes-bot>, mainly for purpose of posting quotes

# docs & running

see the [doc directory](/dov) for documentation, it also has an example nginx config,
and you can also run the app using [./scripts/run.sh](./scripts/run.sh) to match that config :) - but don't run it using
the run.sh as the first run if you ever want to post on it lol

running with gunicorn ( run.sh ) is for production use, for master key generation ( first run ), please
run it in dev mode :

```sh
python3 src/main.py
```

and only then with gunicorn :)

if you already ran it in production and don't know where the key is, run the following command :

```sh
rm -rf src/images src/instance
```

and then run it in debug

### step-by-step

this comes from an email i got from a user :

1. clone the repository : `git clone https://ari.lt/gh/imag && cd imag`
2. make sure you have virtualenv installed ( either through python-virtualenv / python3-virtualenv / py3-virtualenv packages, or by pip - `python3 -m pip install --user --break-system-packages --upgrade virtualenv`
3. ensure you have sqlite3 and memcached installed : `apt install sqlite3 memcached`
3. create a new virtual environment : `python3 -m virtualenv venv && source venv/bin/activate`
4. install the dependencies in the environment : `pip install -r requirements.txt`
5. run the app by either running `scripts/run.sh` or by manually starting memcached and running `src/main.py` with gunicorn ( i assume you're reverse proxying it anyway )
