#!/usr/bin/env bash
echo "reduciendo... por favor espere mientras se reducen las instacias SAT a IP"

python reductor/core.py > log.log

echo ""
echo "la reduccion de SAT a IP ya termino, por favor revisa la carpeta instanciasMiniZinc y revisa el archivo log para ver el tiempo"