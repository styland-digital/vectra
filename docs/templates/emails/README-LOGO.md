# Logo Vectra - Instructions Email

## 📍 Emplacement du Logo

**Chemin:** `backend/app/templates/emails/assets/logo.svg` (ou `logo.png`)

## 📐 Format Recommandé

### Format 1: SVG (Recommandé)

- **Fichier:** `logo.svg`
- **Avantages:** Scalable, léger, net à toutes les tailles
- **Taille:** Largeur 150-200px recommandée
- **Couleur:** Logo monochrome ou couleur selon identité Vectra

### Format 2: PNG @2x (Alternative)

- **Fichier:** `logo.png`
- **Taille:** 300-400px de largeur (pour @2x)
- **Format:** PNG avec transparence si nécessaire
- **Utilisation:** Si SVG non disponible

## 🎨 Design Logo

Selon les Design Tokens Vectra:

- **Primary Color:** `#2E5BFF` (pour logo couleur)
- **Contraste:** Logo doit être lisible sur fond blanc `#FFFFFF`
- **Style:** Professionnel, clean, aligné avec l'identité Vectra

## 🔧 Intégration dans Templates

Le logo est intégré dans le template `base.html` de deux façons:

### Option 1: URL Externe (Production)

```html
<img src="https://app.vectra.io/logo.svg" alt="Vectra" class="logo" width="150">
```

### Option 2: Base64 Data URI (Recommandé pour emails)

```html
<img src="data:image/svg+xml;base64,PHN2Zy4uLj4=" alt="Vectra" class="logo" width="150">
```

**Avantage Base64:** Pas de dépendance externe, compatible tous clients email

### Option 3: Placeholder Texte (Fallback)

Si logo non disponible, affiche "VECTRA" en texte stylé selon Design Tokens.

## 📝 Configuration

Le logo peut être configuré via variable `logo_url` dans le contexte du template:

```python
context = {
    "logo_url": "data:image/svg+xml;base64,...",  # Base64
    # ou
    "logo_url": "https://app.vectra.io/logo.svg",  # URL externe
}
```

## ⚠️ Note Importante

**Pour l'instant:** Le template utilise un placeholder texte "VECTRA" stylé.
**Action requise:** Ajouter le logo SVG/PNG dans `backend/app/templates/emails/assets/logo.svg` (ou `.png`)

---

*Instructions Logo Email - 15 Janvier 2026*
