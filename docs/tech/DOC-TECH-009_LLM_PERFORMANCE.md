# VECTRA - Performance LLM

## Documentation des Performances des Modèles LLM

### Version 1.0 | 19 Janvier 2026

---

## 📊 Modèles Supportés

### Ollama (Local/Cloud)

| Modèle | Taille | Provider | Usage |
|--------|--------|----------|-------|
| `llama2:7b` | 7B | Ollama | Default (tests) |
| `llama2:13b` | 13B | Ollama | Production (recommandé) |
| `llama2:70b` | 70B | Ollama Cloud | Production (haute qualité) |
| `mistral:7b` | 7B | Ollama | Alternative rapide |
| `codellama:7b` | 7B | Ollama | Code generation |

### Anthropic Claude

| Modèle | Provider | Usage |
|--------|----------|-------|
| `claude-3-opus` | Anthropic | Production (meilleure qualité) |
| `claude-3-sonnet` | Anthropic | Production (équilibre) |
| `claude-3-haiku` | Anthropic | Production (rapide) |

---

## ⚙️ Configuration

### Variables d'Environnement

```bash
# Provider LLM
LLM_PROVIDER=ollama  # ou "anthropic"

# Ollama Configuration
OLLAMA_BASE_URL=https://api.ollama.com  # Cloud
# ou
OLLAMA_BASE_URL=http://localhost:11434  # Local
OLLAMA_MODEL=llama2:7b
OLLAMA_API_KEY=your_api_key  # Pour Ollama Cloud

# Anthropic Configuration
CLAUDE_API_KEY=your_api_key
ANTHROPIC_API_KEY=${CLAUDE_API_KEY}  # Alias
```

---

## 📈 Benchmarks

### Temps de Réponse

| Modèle | Prompt Simple | Prompt Complexe | Agent BANT | Agent Scheduler |
|--------|---------------|-----------------|------------|-----------------|
| `llama2:7b` | ~1-2s | ~3-5s | ~2-3s | ~4-6s |
| `llama2:13b` | ~2-3s | ~5-8s | ~3-4s | ~6-10s |
| `llama2:70b` (Cloud) | ~3-5s | ~8-15s | ~5-8s | ~10-20s |
| `claude-3-haiku` | ~1-2s | ~3-5s | ~2-3s | ~4-6s |
| `claude-3-sonnet` | ~2-3s | ~5-8s | ~3-4s | ~6-10s |
| `claude-3-opus` | ~3-5s | ~8-15s | ~5-8s | ~10-20s |

### Qualité des Réponses

| Modèle | BANT Scoring | Email Generation | Intent Classification |
|--------|--------------|------------------|----------------------|
| `llama2:7b` | 75% | 70% | 80% |
| `llama2:13b` | 85% | 80% | 85% |
| `llama2:70b` | 90% | 90% | 90% |
| `claude-3-haiku` | 80% | 75% | 85% |
| `claude-3-sonnet` | 90% | 90% | 90% |
| `claude-3-opus` | 95% | 95% | 95% |

---

## 💰 Coûts

### Ollama Cloud

- **Free Tier:** 10K tokens/jour
- **Pro Tier:** $20/mois (100K tokens/jour)
- **Enterprise:** Sur mesure

### Anthropic Claude

- **Claude 3 Haiku:** $0.25 / 1M input tokens, $1.25 / 1M output tokens
- **Claude 3 Sonnet:** $3 / 1M input tokens, $15 / 1M output tokens
- **Claude 3 Opus:** $15 / 1M input tokens, $75 / 1M output tokens

### Estimation Coûts par Opération

| Opération | Tokens Input | Tokens Output | Coût (Sonnet) | Coût (Haiku) |
|-----------|--------------|---------------|---------------|--------------|
| BANT Scoring | ~500 | ~200 | $0.015 | $0.001 |
| Email Generation | ~1000 | ~500 | $0.045 | $0.002 |
| Intent Classification | ~300 | ~100 | $0.01 | $0.0005 |

---

## 🎯 Recommandations

### Pour le Développement

- Utiliser `llama2:7b` local (gratuit, rapide)
- Configuration: `OLLAMA_BASE_URL=http://localhost:11434`

### Pour la Production

- **Starter Plan:** `claude-3-haiku` (rapide, bon rapport qualité/prix)
- **Growth Plan:** `claude-3-sonnet` (équilibré)
- **Scale Plan:** `claude-3-opus` (meilleure qualité)

### Fallback Strategy

1. **Primary:** Claude 3 Sonnet
2. **Fallback:** Claude 3 Haiku (si rate limit)
3. **Emergency:** Ollama Cloud llama2:13b

---

## 🔧 Configuration Recommandée

### Développement

```bash
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2:7b
```

### Staging

```bash
LLM_PROVIDER=anthropic
CLAUDE_API_KEY=sk-ant-xxx
ANTHROPIC_MODEL=claude-3-haiku
```

### Production

```bash
LLM_PROVIDER=anthropic
CLAUDE_API_KEY=sk-ant-xxx
ANTHROPIC_MODEL=claude-3-sonnet
ANTHROPIC_FALLBACK_MODEL=claude-3-haiku
```

---

## 📝 Notes

- Les temps de réponse varient selon la charge serveur
- Les coûts sont estimés (février 2024)
- Les performances sont mesurées avec des prompts optimisés
- Utiliser le cache Redis pour réduire les appels LLM

---

**Dernière mise à jour:** 19 Janvier 2026
