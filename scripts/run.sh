#!/usr/bin/env sh

set -eu

main() {
    cd src
    python3 -m gunicorn -b 127.0.0.1:19721 -w "$(nproc --all)" main:app &
}

main "$@"
