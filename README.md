# NewMoney - API de Microfinance

## Installation rapide

1. Exécutez le script d'installation :
```bash
chmod +x install.sh
./install.sh
```

2. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

3. Lancez le serveur :
```bash
python manage.py runserver
```

4. Accédez à la documentation : http://127.0.0.1:8000/swagger/

## Structure du projet

- `users/` - Authentification et gestion des utilisateurs
- `clients/` - Gestion des clients
- `agents/` - Gestion des agents
- `products/` - Gestion des produits et conditions
- `accounts/` - Comptes, transactions et épargnes
- `loans/` - Prêts et remboursements
- `notifications/` - Système de notifications

## API Endpoints

- Authentication: `/api/v1/auth/`
- Clients: `/api/v1/clients/`
- Agents: `/api/v1/agents/`
- Products: `/api/v1/products/`
- Accounts: `/api/v1/accounts/`
- Loans: `/api/v1/loans/`
- Notifications: `/api/v1/notifications/`

## Documentation

- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/
- Admin: http://127.0.0.1:8000/admin/
