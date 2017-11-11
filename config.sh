# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]
if [ "$MB_PYTHON_VERSION" == '2.6' ]; then
    DEPENDS="ipaddress unittest2 argparse mock==1.0.1"
elif [ $(lex_ver $MB_PYTHON_VERSION) -le $(lex_ver 3.2) ]; then
    DEPENDS="ipaddress mock"
elif [ "$MB_PYTHON_VERSION" == '3.3' ]; then
    DEPENDS=ipaddress
fi

function pre_build {
    # Any stuff that you need to do before you start building the wheels
    # Runs in the root directory of this repository.
    :
}

function run_tests {
    # Runs tests on installed distribution from an empty directory
    if [ -n "$DEPENDS" ]; then
        pip install $DEPENDS
    fi
    python --version
    pwd
    cd ..
    ls -la
    ls -la ..
    PSUTIL_TESTING=1 python -Wa ../psutil/psutil/tests/__main__.py
    # PSUTIL_TESTING=1 python -Wa ../psutil/psutil/tests/test_memory_leaks.py
}
