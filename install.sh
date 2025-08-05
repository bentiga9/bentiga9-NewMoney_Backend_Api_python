#!/bin/bash
echo "🚀 Installation de NewMoney..."

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
if [[ "$OS" == "Windows_NT" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Installer les dépendances
pip install -r requirements.txt

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

echo "✅ Installation terminée !"
echo "Créez un superutilisateur : python manage.py createsuperuser"
echo "Lancez le serveur : python manage.py runserver"
echo "Documentation : http://127.0.0.1:8000/swagger/"
