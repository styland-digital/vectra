# Vectra API - Collection Postman

Collection Postman complète pour tester les APIs Vectra.

## 📋 Fichiers

- **`Vectra_API_Collection.json`** - Collection principale avec tous les endpoints
- **`Vectra_Local_Environment.json`** - Variables d'environnement pour développement local

## 🚀 Installation Rapide

### 1. Importer la Collection

1. Ouvrir Postman
2. Cliquer sur **Import** (en haut à gauche)
3. Sélectionner `Vectra_API_Collection.json`
4. Cliquer sur **Import**

### 2. Importer l'Environnement

1. Cliquer sur **Environments** (icône œil en haut à droite)
2. Cliquer sur **Import**
3. Sélectionner `Vectra_Local_Environment.json`
4. Cliquer sur **Import**
5. Sélectionner **"Vectra Local"** dans le menu déroulant d'environnement

### 3. Configurer les Variables (si nécessaire)

Si votre backend tourne sur un autre port ou host, modifier les variables dans l'environnement :

- `base_url`: URL de base de l'API (par défaut: `http://localhost:8000`)
- `test_email`: Email de test à utiliser (par défaut: `test@example.com`)

## 📖 Utilisation

### Workflow de Base

1. **Register** (ou **Login** si utilisateur existant)
   - Les tokens sont automatiquement sauvegardés dans les variables d'environnement
   - `access_token` et `refresh_token` sont disponibles pour les autres requêtes

2. **Get Current User (Me)**
   - Utilise automatiquement le `access_token` sauvegardé
   - Affiche les informations de l'utilisateur connecté

3. **Refresh Token**
   - Remplacer le `access_token` expiré par un nouveau
   - Le nouveau token est automatiquement sauvegardé

4. **Change Password** / **Logout**
   - Requièrent l'authentification (Bearer token)

### Variables Automatiques

Les scripts de test sauvegardent automatiquement :

- `access_token` - Token d'accès JWT
- `refresh_token` - Token de rafraîchissement JWT
- `user_id` - ID de l'utilisateur connecté
- `organization_id` - ID de l'organisation

Ces variables sont utilisées automatiquement dans les requêtes suivantes.

## 🔄 Workflow de Mise à Jour

### Quand ajouter/modifier un endpoint ?

Chaque fois qu'une nouvelle route API est créée ou modifiée :

1. **Créer/Modifier la requête dans Postman**
2. **Ajouter des tests automatisés** (vérification du statut, structure de réponse)
3. **Mettre à jour ce README** si nécessaire
4. **Exporter la collection** (Menu → Export)
5. **Commit les changements** dans Git

### Structure Recommandée

Organiser les requêtes par modules dans des dossiers :

```
Vectra API Collection
├── Auth
│   ├── Register
│   ├── Login
│   ├── Refresh Token
│   ├── Get Current User (Me)
│   ├── Change Password
│   └── Logout
├── Campaigns (à venir)
├── Leads (à venir)
├── Emails (à venir)
└── Meetings (à venir)
```

### Template pour Nouveau Endpoint

```json
{
    "name": "Endpoint Name",
    "event": [
        {
            "listen": "test",
            "script": {
                "exec": [
                    "pm.test(\"Status code is 200\", function () {",
                    "    pm.response.to.have.status(200);",
                    "});",
                    "",
                    "if (pm.response.code === 200) {",
                    "    const response = pm.response.json();",
                    "    // Tests spécifiques",
                    "}"
                ],
                "type": "text/javascript"
            }
        }
    ],
    "request": {
        "method": "GET|POST|PUT|DELETE|PATCH",
        "header": [
            {
                "key": "Authorization",
                "value": "Bearer {{access_token}}"
            },
            {
                "key": "Content-Type",
                "value": "application/json"
            }
        ],
        "body": {
            "mode": "raw",
            "raw": "{\n    \"key\": \"value\"\n}"
        },
        "url": {
            "raw": "{{base_url}}/api/v1/module/endpoint",
            "host": ["{{base_url}}"],
            "path": ["api", "v1", "module", "endpoint"]
        },
        "description": "Description de l'endpoint"
    }
}
```

## 🧪 Tests Automatisés

Chaque requête inclut des tests automatisés qui vérifient :

- **Code de statut HTTP** correct
- **Structure de la réponse** (présence de champs attendus)
- **Sauvegarde automatique** des tokens/IDs dans les variables

Les résultats des tests apparaissent dans l'onglet **Test Results** après l'exécution d'une requête.

## 🔐 Authentification

La collection utilise l'authentification JWT :

1. **Login/Register** retournent `access_token` et `refresh_token`
2. Les tokens sont **automatiquement sauvegardés** dans les variables d'environnement
3. Les requêtes suivantes utilisent **automatiquement** `Bearer {{access_token}}`

Si le token expire :
1. Utiliser **Refresh Token** pour obtenir un nouveau `access_token`
2. Le nouveau token sera automatiquement sauvegardé

## 🛠️ Dépannage

### Erreur : "Connection refused"

**Problème :** Le backend n'est pas lancé.

**Solution :**
```bash
# Vérifier que le backend tourne
docker compose ps backend

# Lancer le backend si nécessaire
docker compose up -d backend
```

### Erreur : "Unauthorized" ou "Could not validate credentials"

**Problème :** Le token est expiré ou invalide.

**Solution :**
1. Relancer **Login** ou **Register**
2. Le nouveau token sera automatiquement sauvegardé

### Variables d'environnement non disponibles

**Problème :** L'environnement "Vectra Local" n'est pas sélectionné.

**Solution :**
1. Cliquer sur le menu déroulant d'environnement (en haut à droite)
2. Sélectionner **"Vectra Local"**

## 📝 Notes

- **Stateless Auth** : Les tokens JWT restent valides même après logout (côté client)
- **OAuth2 Compatible** : L'endpoint `/login` utilise `form-data` avec le champ `username` pour l'email
- **Tests** : Tous les tests sont dans l'onglet "Tests" de chaque requête

## 🔗 Liens Utiles

- **Documentation API** : `docs/tech/DOC-TECH-002_API_CONTRACTS.md`
- **Workflow** : `docs/workflow/WORKFLOW_ORCHESTRATION.md`
- **Backend** : `backend/app/api/v1/`

---

*Dernière mise à jour : 15 Janvier 2026*
