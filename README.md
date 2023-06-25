# Enigma

[![pipeline status](https://mygit.th-deg.de/jd17123/enigma/badges/develop/pipeline.svg)](https://mygit.th-deg.de/jd17123/enigma/-/commits/develop)
[![coverage report](https://mygit.th-deg.de/jd17123/enigma/badges/develop/coverage.svg)](https://mygit.th-deg.de/jd17123/enigma/-/commits/develop)
[![Latest Release](https://mygit.th-deg.de/jd17123/enigma/-/badges/release.svg)](https://mygit.th-deg.de/jd17123/enigma/-/releases)

`docker` can be replaced with `podman`.

## Dev

```console
docker-compose -f compose.yml -f compose.dev.yml build
docker-compose -f compose.yml -f compose.dev.yml up
docker-compose -f compose.yml -f compose.dev.yml down
```

Check source:

```console
docker build --progress=plain --build-arg context=local-check -t backend:local-check -f backend/Containerfile backend # or
podman build --build-arg context=local-check -t backend:local-check backend
```

Run end-to-end tests:

```console
docker-compose -f compose.yml -f compose.e2e.yml build
docker-compose -f compose.yml -f compose.e2e.yml up
docker-compose -f compose.yml -f compose.e2e.yml down
```

## Prod

```console
docker-compose -f compose.yml up
docker-compose -f compose.yml down
```
