#!/bin/sh

vboxmanage controlvm default natpf1 "gulpwatch,tcp,,3000,,3000"
vboxmanage controlvm default natpf1 "django,tcp,,8000,,8000"
vboxmanage controlvm default natpf1 "mysql,tcp,,3306,,3306"
vboxmanage controlvm default natpf1 "pdfreactor,tcp,,9423,,9423"
vboxmanage controlvm default natpf1 "phpmyadmin,tcp,,8080,,8080"
vboxmanage controlvm default natpf1 "fakes3,tcp,,4569,,4569"
vboxmanage controlvm default natpf1 "es1,tcp,,9200,,9200"
vboxmanage controlvm default natpf1 "es2,tcp,,9300,,9300"
