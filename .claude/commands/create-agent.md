---

## 1. create-agent.md

```markdown
# Créer un Nouvel Agent IA

## Usage
```
/create-agent <nom_agent>
```

## Ce que cette commande fait

1. Crée la structure de fichiers dans `backend/app/agents/<nom>/`
2. Génère le squelette de l'agent avec CrewAI
3. Crée le fichier de prompts
4. Crée les tests unitaires
5. Enregistre l'agent dans `__init__.py`

## Structure créée

```
backend/app/agents/<nom>/
├── __init__.py
├── agent.py      # Logique principale
├── prompts.py    # Prompts LLM
└── tools.py      # Outils si nécessaire
```

## Template agent.py

```python
from crewai import Agent, Task
from app.agents.base import BaseVectraAgent
from app.agents.<nom>.prompts import MAIN_PROMPT

class <Nom>Agent(BaseVectraAgent):
    """
    Agent <Nom>: <description>
    """
    
    def __init__(self, config=None):
        super().__init__(config)
        self.agent = Agent(
            role="<role>",
            goal="<goal>",
            backstory="<backstory>",
            tools=self._get_tools(),
            llm=self.llm
        )
    
    def _get_tools(self):
        return []
    
    async def execute(self, input_data: dict) -> dict:
        task = Task(
            description=MAIN_PROMPT.format(**input_data),
            agent=self.agent,
            expected_output="JSON with results"
        )
        result = await self._execute_task(task)
        return self._parse_result(result)
    
    def _parse_result(self, raw: str) -> dict:
        # Parse logic
        return {}
```

## Checklist après création

- [ ] Définir les prompts dans prompts.py
- [ ] Implémenter la logique dans agent.py
- [ ] Ajouter les tests dans tests/unit/agents/
- [ ] Créer la task Celery si async
- [ ] Mettre à jour la documentation
```

---