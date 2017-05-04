#!/usr/bin/env bash

set -e

start() {
	python manage.py migrate
	python manage.py runscript initial_data
	python manage.py runscript test_data
	end
	python manage.py runserver 9500 < /dev/null &
}

end() {
	lsof -i tcp:9500| awk 'NR!=1 {print $2}' | xargs kill
}

if [ "$1" == "end" ]; then
	end
else
	start
fi
