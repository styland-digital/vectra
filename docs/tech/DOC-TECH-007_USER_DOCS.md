# VECTRA - DOCUMENTATION UTILISATEUR
## Guide de Démarrage et Manuel d'Utilisation
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-008  
**Statut:** APPROUVÉ  
**Audience:** Utilisateurs finaux de la plateforme Vectra  

---

## TABLE DES MATIERES

1. Bienvenue sur Vectra
2. Premiers Pas
3. Créer une Campagne
4. Gérer les Leads
5. Approuver les Emails
6. Suivre les Performances
7. Paramètres
8. FAQ
9. Support

---

## 1. BIENVENUE SUR VECTRA

### 1.1 Qu'est-ce que Vectra ?

Vectra est une plateforme d'agents IA qui automatise votre prospection commerciale B2B. Nos agents intelligents :

- **Trouvent** des prospects qualifiés correspondant à vos critères
- **Qualifient** chaque prospect selon le framework BANT
- **Rédigent** des emails personnalisés
- **Planifient** des rendez-vous automatiquement

**Résultat :** Plus de rendez-vous qualifiés, moins de temps perdu.

### 1.2 Comment ça fonctionne ?

```
1. Vous définissez votre cible (postes, secteurs, taille)
        ↓
2. L'agent Prospector trouve des prospects correspondants
        ↓
3. L'agent BANT qualifie chaque prospect (score 0-100)
        ↓
4. L'agent Scheduler génère un email personnalisé
        ↓
5. Vous approuvez l'email
        ↓
6. L'email est envoyé avec un lien Calendly
        ↓
7. Le prospect prend rendez-vous → Vous closez !
```

### 1.3 Temps d'utilisation quotidien

- **Jour 1 :** 10-15 min (création de campagne)
- **Jours suivants :** 2-5 min (approbation des emails + suivi)

---

## 2. PREMIERS PAS

### 2.1 Connexion

1. Allez sur **app.vectra.io**
2. Entrez votre email et mot de passe
3. Cliquez sur **Se connecter**

**Mot de passe oublié ?**
Cliquez sur "Mot de passe oublié" et suivez les instructions envoyées par email.

### 2.2 Découverte du Dashboard

Le dashboard est votre page d'accueil. Voici ce que vous y voyez :

| Section | Description |
|---------|-------------|
| **Métriques** | Vos chiffres clés : prospects trouvés, qualifiés, emails envoyés, RDV |
| **Actions rapides** | Boutons pour les actions fréquentes |
| **Activité récente** | Dernières actions de vos agents |
| **Alertes** | Éléments nécessitant votre attention |

### 2.3 Navigation

- **Dashboard** - Vue d'ensemble
- **Campagnes** - Gérer vos campagnes de prospection
- **Leads** - Voir tous vos prospects
- **Emails** - Approuver les emails en attente
- **Meetings** - Vos rendez-vous planifiés
- **Analytics** - Rapports détaillés
- **Paramètres** - Configuration du compte

---

## 3. CRÉER UNE CAMPAGNE

### 3.1 Étape 1 : Nom et Secteur

1. Cliquez sur **Nouvelle Campagne**
2. Donnez un nom explicite (ex: "VP Sales France Q1 2026")
3. Sélectionnez le secteur cible
4. Cliquez sur **Suivant**

**💡 Conseil :** Utilisez un nom qui vous permet d'identifier facilement la campagne plus tard.

### 3.2 Étape 2 : Profil Cible

Définissez qui vous voulez contacter :

| Champ | Description | Exemple |
|-------|-------------|---------|
| **Postes** | Titres des personnes à contacter | VP Sales, Directeur Commercial |
| **Taille entreprise** | Nombre d'employés | 50-200 |
| **Géographie** | Pays ou régions | France, Belgique |
| **Secteurs** | Industries ciblées | SaaS, Tech, Consulting |

**💡 Conseil :** Soyez précis. Une cible trop large = prospects moins qualifiés.

### 3.3 Étape 3 : Template d'Email

Un email a été pré-généré pour vous. Vous pouvez :

- **Utiliser tel quel** (recommandé pour commencer)
- **Modifier** le sujet ou le contenu
- **Tester** avec l'aperçu

**Structure recommandée :**
1. Accroche personnalisée
2. Problème que vous résolvez
3. Proposition de valeur (1-2 phrases)
4. Call-to-action clair

### 3.4 Étape 4 : Disponibilités

Configurez quand vous êtes disponible pour des rendez-vous :

1. Sélectionnez les jours de la semaine
2. Définissez les créneaux horaires
3. Ajoutez votre lien Calendly

**⚠️ Important :** Assurez-vous que votre Calendly est bien synchronisé avec votre agenda.

### 3.5 Étape 5 : Révision et Lancement

Vérifiez tous les paramètres :

- ✅ Nom de campagne
- ✅ Critères de ciblage
- ✅ Template d'email
- ✅ Disponibilités

Puis cliquez sur **Créer la Campagne**.

**Note :** La campagne est créée en mode "Brouillon". Pour la lancer, cliquez sur **Lancer la Campagne**.

---

## 4. GÉRER LES LEADS

### 4.1 Vue Liste des Leads

Accédez à tous vos prospects via **Leads** dans le menu.

**Filtres disponibles :**
- Par campagne
- Par statut (Nouveau, Qualifié, Contacté, etc.)
- Par score BANT
- Par date

### 4.2 Statuts des Leads

| Statut | Signification |
|--------|---------------|
| 🆕 **Nouveau** | Vient d'être trouvé |
| 📊 **Enrichi** | Données complétées |
| ✅ **Qualifié** | Score BANT > seuil |
| ❌ **Rejeté** | Score trop faible |
| 📧 **Contacté** | Email envoyé |
| 💬 **Répondu** | A répondu |
| 📅 **Meeting** | RDV planifié |
| 🎯 **Converti** | Opportunité créée |

### 4.3 Détail d'un Lead

Cliquez sur un lead pour voir :

- **Profil complet** : Nom, poste, entreprise, coordonnées
- **Score BANT** : Détail du scoring (Budget, Authority, Need, Timeline)
- **Historique** : Toutes les interactions
- **Email généré** : L'email prêt à être envoyé
- **Notes** : Vos notes personnelles

### 4.4 Score BANT Expliqué

Le score BANT évalue la qualité du prospect sur 4 critères :

| Critère | Question | Points |
|---------|----------|--------|
| **Budget** | L'entreprise a-t-elle les moyens ? | 0-25 |
| **Authority** | Est-ce un décideur ? | 0-25 |
| **Need** | Ont-ils besoin de notre solution ? | 0-25 |
| **Timeline** | Y a-t-il une urgence ? | 0-25 |

**Score total : 0-100**

- ≥ 60 : Qualifié → Email envoyé
- 40-59 : À nurturiser
- < 40 : Non qualifié

**💡 Vous pouvez ajuster le seuil** dans les paramètres de campagne.

---

## 5. APPROUVER LES EMAILS

### 5.1 Pourquoi approuver ?

Vectra génère des emails personnalisés, mais vous gardez le contrôle. Avant tout envoi, vous pouvez :

- **Approuver** l'email tel quel
- **Modifier** et approuver
- **Rejeter** si inapproprié
- **Régénérer** si besoin d'un nouvel angle

### 5.2 File d'Approbation

1. Allez dans **Emails** ou cliquez sur la notification
2. Vous voyez la liste des emails en attente
3. Cliquez sur un email pour le prévisualiser

### 5.3 Actions Possibles

| Action | Quand l'utiliser |
|--------|------------------|
| ✅ **Approuver** | L'email est parfait |
| ✏️ **Modifier** | Petite correction à faire |
| 🔄 **Régénérer** | Besoin d'un angle différent |
| ❌ **Rejeter** | Ne pas contacter ce prospect |

### 5.4 Bonnes Pratiques

- **Approuvez rapidement** : Les prospects "froids" refroidissent vite
- **Personnalisez si pertinent** : Ajoutez une référence spécifique
- **Faites confiance à l'IA** : Elle apprend de vos corrections

---

## 6. SUIVRE LES PERFORMANCES

### 6.1 Dashboard Analytics

Accédez aux **Analytics** pour voir vos performances.

### 6.2 Métriques Clés

| Métrique | Signification | Bon niveau |
|----------|---------------|------------|
| **Taux d'ouverture** | % d'emails ouverts | > 40% |
| **Taux de réponse** | % de réponses reçues | > 8% |
| **Taux de clic** | % de clics sur Calendly | > 5% |
| **Taux de RDV** | % de RDV pris | > 2% |
| **Coût par lead** | Coût moyen par lead | < $5 |
| **Coût par RDV** | Coût moyen par meeting | < $150 |

### 6.3 Analyser par Campagne

Comparez les performances de vos différentes campagnes :

1. Allez dans **Analytics**
2. Sélectionnez **Par Campagne**
3. Identifiez les campagnes les plus performantes

**💡 Conseil :** Dupliquez les campagnes qui marchent et ajustez celles qui sous-performent.

### 6.4 Période de Temps

Analysez sur différentes périodes :
- Aujourd'hui
- 7 derniers jours
- 30 derniers jours
- Période personnalisée

---

## 7. PARAMÈTRES

### 7.1 Paramètres du Compte

**Profil :**
- Nom et prénom
- Email
- Avatar
- Mot de passe

**Préférences :**
- Thème (Clair / Sombre)
- Langue
- Fuseau horaire
- Notifications email

### 7.2 Paramètres de l'Organisation

*(Admins uniquement)*

**Général :**
- Nom de l'organisation
- Logo
- Seuil BANT par défaut

**Équipe :**
- Gérer les utilisateurs
- Attribuer les rôles
- Inviter de nouveaux membres

**Intégrations :**
- HubSpot
- Calendly
- SendGrid

### 7.3 Rôles et Permissions

| Rôle | Droits |
|------|--------|
| **Owner** | Tout (dont facturation) |
| **Admin** | Gestion opérationnelle |
| **Manager** | Supervision + validation |
| **Operator** | Exécution des tâches |
| **Viewer** | Consultation seule |

---

## 8. FAQ

### Campagnes

**Q: Combien de temps avant de voir des résultats ?**
R: Les premiers prospects sont trouvés en 24-48h. Les premiers RDV arrivent généralement après 1-2 semaines.

**Q: Puis-je avoir plusieurs campagnes en même temps ?**
R: Oui, selon votre plan. Chaque campagne peut cibler un segment différent.

**Q: Comment modifier une campagne en cours ?**
R: Mettez-la en pause, modifiez les paramètres, puis relancez-la.

### Leads

**Q: D'où viennent les données des prospects ?**
R: Nous utilisons des sources publiques (LinkedIn, sites web) et des APIs d'enrichissement professionnelles.

**Q: Un prospect peut-il apparaître dans plusieurs campagnes ?**
R: Non, notre système de déduplication évite les doublons.

**Q: Comment supprimer un lead ?**
R: Vous pouvez le "rejeter", il ne sera plus contacté.

### Emails

**Q: Combien d'emails sont envoyés par jour ?**
R: Par défaut, 50/jour maximum pour éviter les problèmes de délivrabilité. Ajustable dans les paramètres.

**Q: Les emails arrivent-ils en spam ?**
R: Nous utilisons les meilleures pratiques (authentification, warm-up). Le taux de délivrabilité est > 95%.

**Q: Puis-je personnaliser le template pour tous les emails ?**
R: Oui, dans les paramètres de campagne.

### Facturation

**Q: Comment fonctionne la facturation ?**
R: Abonnement mensuel + commission sur les rendez-vous (selon votre plan).

**Q: Où voir ma facture ?**
R: Dans Paramètres > Facturation.

---

## 9. SUPPORT

### 9.1 Chat en Direct

Cliquez sur le bouton de chat en bas à droite pour parler à notre équipe.

**Disponibilité :** Lun-Ven, 9h-18h (heure de Paris)

### 9.2 Email

Envoyez-nous un email : **support@vectra.io**

Temps de réponse moyen : < 4 heures (jours ouvrés)

### 9.3 Centre d'Aide

Plus d'articles et tutoriels sur : **help.vectra.io**

### 9.4 Statut du Service

Vérifiez si nos services fonctionnent normalement : **status.vectra.io**

---

## RACCOURCIS CLAVIER

| Raccourci | Action |
|-----------|--------|
| `G` puis `D` | Aller au Dashboard |
| `G` puis `C` | Aller aux Campagnes |
| `G` puis `L` | Aller aux Leads |
| `G` puis `E` | Aller aux Emails |
| `/` | Recherche globale |
| `?` | Afficher les raccourcis |
| `Esc` | Fermer le panneau |

---

## GLOSSAIRE

| Terme | Définition |
|-------|------------|
| **BANT** | Framework de qualification : Budget, Authority, Need, Timeline |
| **Lead** | Prospect potentiel |
| **Campagne** | Ensemble de paramètres pour une prospection ciblée |
| **Nurture** | Maintenir le contact avec un prospect pas encore prêt |
| **Calendly** | Outil de prise de rendez-vous en ligne |
| **Taux d'ouverture** | % de personnes ayant ouvert votre email |
| **CTA** | Call-to-Action, l'action que vous demandez (ex: prendre RDV) |

---

**Besoin d'aide supplémentaire ?**

📧 support@vectra.io  
💬 Chat en direct dans l'app  
📚 help.vectra.io

---

*Vectra - Powering your pipeline, simply.*

*Documentation v1.0 - 14 Janvier 2026*
