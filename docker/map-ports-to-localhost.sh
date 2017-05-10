#!/bin/sh

vboxmanage controlvm default natpf1 "mysql,tcp,,3306,,3306"
vboxmanage controlvm default natpf1 "pdfreactor,tcp,,9423,,9423"
vboxmanage controlvm default natpf1 "es1,tcp,,9200,,9200"
vboxmanage controlvm default natpf1 "es2,tcp,,9300,,9300"
