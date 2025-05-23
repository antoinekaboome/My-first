# My-first

Ce dépôt contient un exemple très simple d'application web qui affiche l'heure courante.
Cette nouvelle version propose une interface plus attrayante avec un fond dégradé et une police de style digital. Elle affiche également une horloge analogique.

## Fichiers

- `index.html` : page web affichant l'heure locale en JavaScript avec une horloge numérique et une version analogique.
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


## Déploiement automatique

Lorsque le workflow pousse l'image sur le registre, il se connecte ensuite au serveur pour mettre à jour le conteneur en cours d'exécution. Pour cela, deux secrets doivent être ajoutés dans les paramètres du dépôt :

- `SERVER_USER` : nom d'utilisateur SSH.
- `SERVER_SSH_KEY` : clé privée permettant la connexion.

Une fois ces secrets renseignés, le workflow exécutera `docker pull`, arrêtera l'ancien conteneur s'il existe puis lancera la nouvelle image.
