---
name: Configuration OPENAI/LLM, Invitations Utilisateurs, Docker, et Endpoints Manquants
overview: Ce plan couvre la configuration des API keys LLM pour les tests, l'implémentation complète du système d'invitation (avec endpoint d'acceptation), la création directe d'utilisateurs par les owners, la correction des Dockerfiles et docker-compose, et la création des endpoints de campagne selon REALISATION_TECHNIQUE.md.
todos:
  - id: llm-config-tests
    content: Configurer OLLAMA/CLAUDE pour les tests - mettre à jour conftest.py, retirer skip des tests E2E campaign, créer .env.test
    status: pending
  - id: docker-compose-fix
    content: Corriger docker-compose.yml - ajouter 'build:' ligne 61, ajouter toutes les variables d'environnement LLM/Email/External APIs, créer .env.example
    status: pending
  - id: invitation-migration-otp
    content: Migrer système invitation vers OTP - créer table invitations, migration DB, mettre à jour InvitationService pour utiliser OTP au lieu de tokens
    status: pending
  - id: invite-accept-endpoint
    content: Créer POST /api/v1/user/invite/accept - endpoint pour accepter invitation avec OTP, schema AcceptInvitationRequest, logique complète dans user.py
    status: pending
    dependencies:
      - invitation-migration-otp
  - id: create-user-direct-endpoint
    content: Créer POST /api/v1/user/organizations/me/users/create - endpoint pour créer utilisateur directement (Owner/Admin), schema CreateUserRequest, service create_user_directly
    status: pending
  - id: campaign-endpoints
    content: Créer endpoints campagne selon REALISATION_TECHNIQUE.md - campaigns.py avec CRUD + launch/pause sous /api/v1/user/campaigns/*, schemas campaign.py, service campaign.py
    status: pending
  - id: campaign-tests
    content: Tests pour endpoints campagne - tests unitaires service, tests intégration API, tests E2E flow complet
    status: pending
    dependencies:
      - campaign-endpoints
  - id: invitation-tests
    content: Tests pour invitation - test_invite_user_generates_otp, test_accept_invitation (avec OTP), test_create_user_directly, cas d'erreur (OTP expiré, OTP invalide, email existant)
    status: pending
    dependencies:
      - invitation-migration-otp
      - invite-accept-endpoint
      - create-user-direct-endpoint
  - id: api-documentation
    content: Mettre à jour DOC-TECH-002_API_CONTRACTS.md - ajouter tous les nouveaux endpoints avec exemples complets
    status: pending
    dependencies:
      - invite-accept-endpoint
      - create-user-direct-endpoint
      - campaign-endpoints
  - id: workflow-logs
    content: Créer logs selon WORKFLOW_ORCHESTRATION.md - logs pour chaque feature/endpoint/fix créé
    status: pending
  - id: docker-test
    content: Tester docker-compose - vérifier que tous les services démarrent, que les variables d'environnement sont injectées, que les healthchecks fonctionnent
    status: pending
    dependencies:
      - docker-compose-fix
---

