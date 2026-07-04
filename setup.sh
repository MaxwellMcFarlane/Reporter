#!/usr/bin/sh
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done

export XUTILSPATH="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
export LIBSPATH="${XUTILSPATH}/libs/py-modules"
export PATH="$XUTILSPATH/bin:$PATH"
export PYTHONPATH="$LIBSPATH:$PYTHONPATH"