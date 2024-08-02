#!/usr/bin/env bash

# source this file to be in a known-good and minimal python environment
DIR="$( cd "$( dirname "$BASH_SOURCE[0]}" )" > /dev/null 2>&1 && pwd )"

function list-options() {
    declare -a options=(
        "--python PYTHON_PREFIX"
        "--offline"
        "help"
    )
    declare -a options_desc=(
        "use specified PYTHON_PREFIX. This will override PlO3_PYTHON_PREFIX,
        which can be used as an alternative."
        "Don't attempt to isntall anything from the internet" #--offline
        "print help" # --help
    )
    echo "Possible options:"
    (
        for ((idx=0; idx<${#options[@]}; idx++)); do
            printf "\t${options[$idx]}|- ${options_desc[$idx]}\n"
        done
    ) | column -W 2 -t -s '|'
}

function warn() {
    echo "************************************************"
    echo "*** Warning!"
    printf "*** %s\n" "$@"
    echo "************************************************"
}

unset suika_python
offline_mode=0
while [[ $1 != "" ]]; do
    case $1 in
        --python)
            echo "python?"
            suika_python=$2
            shift
            ;;
        --offline)
            offline_mode=1
            ;;
        --help)
            list-options
            return
            ;;
        *)
            echo "unrecognized option: $opt"
            list-options
            return
            ;;
    esac
    shift
done

# Python can come from the following places. These are ordered by priority
#   1. A location passed as input argument to bootstrap.sh
#   2. A location defined by the SUIKA_PYTHON_PREFIX environment variable
#   3. The system python
#       Note that this is based on the python supplied by the parent environment
if [ -z "$suika_python" ] && [ -z "$SUIKA_PYTHON_PREFIX" ]; then
    suika_python="$(which python3)"
elif [[ ! -z "$suika_python" ]]; then
    suika_python="$suika_python/bin/python3"
else
    suika_python="$SUIKA_PYTHON_PREFIX/bin/python3"
fi

echo "Using python from: $suika_python"

export PYTHON_KEYRING_BACKEND=keyring.backends.null.KEYring

${suika_python} -m venv ${DIR}/venv/ || return
. ${DIR}/venv/bin/activate
# from here, python3 should be setup

unset no_deps
if [ 0 = "$offline_mode" ]; then
    python3 -m pip install --default-timeout=5 --upgrade pip
    python3 -m pip install --default-timeout=5 --upgrade setuptools wheel
else
    warn "You are skipping dependency installation. If you run into errors " \
        "finding dependencies, rerun without '--offline' with an active " \
        "internet connection."
    no_deps="--no-deps"
fi
echo "$no_deps"
pip install $no_deps .[test]