# DÉCISIONS PRODUIT VERROUILLÉES
## Règles UX/UI Non-Négociables
### Vectra - Janvier 2026

---

## 1️⃣ MOBILE-FIRST (RÈGLE N°1)

Le desktop n'est plus la base. C'est une **vue étendue**.

### Implications directes
- Navigation compacte
- Actions prioritaires visibles en 1 écran
- Pas de dashboards surchargés
- Hiérarchie verticale stricte

> **📌 Si ça ne fonctionne pas sur mobile, ça ne passe pas sur desktop.**

---

## 2️⃣ DARK MODE NATIF (RÈGLE N°2)

### Comportement
- **Dark = mode par défaut**
- Light = option utilisateur
- Choix sauvegardé par user et organization
- Override possible par utilisateur

### Technique
- Design tokens dual
- Pas d'inversion brute
- Couleurs pensées dès le départ

---

## 3️⃣ UX PHILOSOPHIE VECTRA (RÈGLE N°3)

### Montrer peu. Exécuter bien.

- 1 action principale par écran
- Les chiffres avant les graphiques
- Les décisions avant l'analyse
- Zéro bruit visuel

---

## 4️⃣ LAYOUT DES PAGES

### Page 1: Organization Dashboard (Mobile First)

**Objectif** : En 10 secondes, l'utilisateur sait :
- Si le système tourne
- S'il produit des résultats
- S'il doit agir

### Structure

**🔝 HEADER (compact)**
- Logo wordmark
- Org selector
- Avatar user (menu)

**📊 SECTION 1 — SYSTEM STATUS (Card prioritaire)**
- Campaigns running
- Leads qualified (today / week)
- Meetings booked
- Style: chiffres grands, texte minimal, aucune animation inutile

**🎯 SECTION 2 — ACTION PRINCIPALE (Card CTA)**
- Bouton: "Start campaign" ou "Review pending approvals"
- Le système décide ce qui est prioritaire

**📋 SECTION 3 — LAST ACTIVITY**
- Dernières actions IA
- Statuts clairs
- Timestamps

**⚠️ SECTION 4 — ALERTS (si besoin)**
- Erreurs
- Quota
- Validation requise
- ❌ Invisible si vide

**🔽 BOTTOM NAV (MOBILE)**
```
Overview | Campaigns | Leads | Analytics | Settings
```

### Desktop (Extension)
- Même structure
- Grille 2 colonnes
- Side nav latéral
- Aucune info nouvelle

---

## 5️⃣ DARK / LIGHT MODE — EXÉCUTION

### Dark (default)
- Background profond
- Surfaces contrastées
- Accent orange très parcimonieux

### Light
- Fond clair
- Même hiérarchie
- Aucune perte d'information

---

## 6️⃣ RÔLES & VISIBILITÉ (UX)

| Rôle | Actions visibles |
|------|------------------|
| Owner | Tout |
| Admin | Opérations |
| Manager | Supervision |
| Operator | Exécution |
| Viewer | Lecture |

👉 UI identique, capacités différentes

---

## 7️⃣ ORDRE DE DESIGN DES PAGES

1. ✅ Organization Dashboard
2. Campaigns (liste + création)
3. Campaign detail
4. Leads inbox
5. Lead detail
6. Meetings
7. Analytics
8. Settings org
9. Platform Admin (en dernier)

---

*Décisions verrouillées - Aucune modification sans validation*
