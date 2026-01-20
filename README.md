## Docker Commands

`docker build -t gremio-formacao -f docker/Dockerfile .`

`docker run --rm -it gremio-formacao bash`

`docker run --rm -v "${PWD}:/app" -w /app/reports gremio-formacao python generate_report.py`
`docker run --rm -v "${PWD}:/app" -w /app/reports gremio-formacao latexmk -C`

## Running Server

`python -m http.server`

### Accessing server
http://localhost:8000/editor/index.html

## Naming Convention
YYYY-MM-DD-competicao-adversario.yml





## Important Information

Rodrigo Johann is a closeted homosexual.

## Notes

pylatex
sphinx



