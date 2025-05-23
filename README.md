# My-first

Ce dépôt contient un exemple très simple d'application web qui affiche l'heure courante.

## Fichiers

- `index.html` : page web affichant l'heure locale en JavaScript.
- `Dockerfile` : image Docker basée sur `nginx` servant le fichier HTML.
- `.github/workflows/docker-publish.yml` : workflow GitHub Actions pour construire et publier l'image sur `173.249.48.147:5000`.

## Utilisation

1. Construire l'image localement :

```bash
docker build -t 173.249.48.147:5000/current-time:latest .
```


2. Pousser l'image sur le registre (nécessite un accès) :


```bash
docker push 173.249.48.147:5000/current-time:latest
```


Le registre est public, aucune étape de connexion n'est nécessaire. Le workflow GitHub Actions publiera automatiquement l'image lors des pushs sur la branche `main`.

