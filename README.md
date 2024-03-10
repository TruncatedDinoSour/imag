# imag

> simple and hackable suckless image board

the imag image board is made to be simple, though separated, so you
could easily add or remove features, update them, etc

this is not sole software, it is suckless ( ? ) software, which you are meant
to hack yourself,, you can, of course, use the default settings and whatnot,
but it is highly encouraged to make forks and hack it yourself :)

# licensing

you can distribute, modify, share, redistribute, etc etc etc with no credit or anything,
this project is released under unlicense and i give away all my rights to this project :)

license : unlicense

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
