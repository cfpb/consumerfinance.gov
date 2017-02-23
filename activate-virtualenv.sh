# ==========================================================================
# Script for activating the virtualenv (creating it first, if necessary).
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Confirm that variable VENV_NAME is already set to the name of the virtualenv
if [ -z $VENV_NAME ]; then
  echo "Error: Environment variable VENV_NAME must be set before continuing."
  return
fi

echo 'Activating virtualenv, if not already activated...'

if ! type "workon" &>/dev/null; then
  virtualenvwrapper_path=`which virtualenvwrapper.sh || echo 'not found'`

  if [ "$virtualenvwrapper_path" == 'not found' ]; then
    echo 'Error: virtualenvwrapper.sh is not on your path.' \
         'Please ensure virtualenv & virtualenvwrapper are installed correctly.'
    return
  fi

  echo "virtualenvwrapper found at $virtualenvwrapper_path"
  source $virtualenvwrapper_path
fi

if ! which python2.7 &>/dev/null; then
  echo 'Error: python2.7 is not in your path.' \
       'Please ensure python2.7 is installed and available'
  return
fi

if workon $VENV_NAME; then
  echo "Virtualenv $VENV_NAME activated."
else
  echo "Attempting to create new virtualenv $VENV_NAME..."
  if mkvirtualenv -p `which python2.7` $VENV_NAME; then
    echo "Virtualenv $VENV_NAME created and activated."
  else
    echo 'Error: virtualenv not activated.' \
         'Something went wrong.'
  fi
fi
