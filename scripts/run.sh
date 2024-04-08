#!/usr/bin/env sh

set -eu

main() {
    cd src
    memcached --port=18391 --daemon --memory-limit=1024 --enable-largepages
    python3 -m gunicorn -b 127.0.0.1:19721 -w "$(nproc --all)" main:app &
}

main "$@"
