# Assets Email Templates

## 📍 Emplacement

**Dossier:** `backend/app/templates/emails/assets/`

## 📐 Logo Vectra

### Format Recommandé: SVG

**Fichier:** `logo.svg`

**Spécifications:**

- Format: SVG (Scalable Vector Graphics)
- Taille: Largeur 150-200px recommandée
- Style: Logo monochrome ou couleur selon identité Vectra
- Couleur Primary: `#2E5BFF` (pour logo couleur)

### Format Alternatif: PNG

**Fichier:** `logo.png`

**Spécifications:**

- Format: PNG @2x (pour haute résolution)
- Taille: 300-400px de largeur
- Background: Transparent (si nécessaire)

## 🎨 Design Tokens

Le logo doit respecter:

- Primary Color: `#2E5BFF`
- Contraste: Lisible sur fond blanc `#FFFFFF`
- Style: Professionnel, clean, aligné avec l'identité Vectra

## 🔧 Utilisation dans Templates

Le logo est utilisé dans `base.html`:

```html
{% if logo_url %}
<img src="{{ logo_url }}" alt="Vectra" class="logo" width="150">
{% else %}
<div style="font-size: 24px; font-weight: 700; color: #2E5BFF;">VECTRA</div>
{% endif %}
```

**Pour le moment:** Un placeholder texte "VECTRA" est affiché.  
**Action requise:** Ajouter le logo SVG/PNG dans ce dossier.

## 📝 Base64 Integration

Pour intégrer le logo en base64 (recommandé pour emails):

```python
import base64

with open("app/templates/emails/assets/logo.svg", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode("utf-8")
    logo_url = f"data:image/svg+xml;base64,{logo_base64}"
```

**Avantage:** Pas de dépendance externe, compatible tous clients email.

---

*Assets Email Templates - 15 Janvier 2026*
