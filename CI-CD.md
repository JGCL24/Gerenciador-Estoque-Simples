# 🔄 Pipeline CI/CD - GitHub Actions

## O que é a Pipeline?

A **CI/CD Pipeline** é um fluxo automatizado que testa e compila o código a cada `push` ou `pull request`.

- **CI** = Continuous Integration (testes automáticos)
- **CD** = Continuous Deployment (deploy automático, opcional)

---

## Como Funciona

```
Você faz commit e push
         ↓
GitHub detecta mudanças
         ↓
Inicia workflow (ci.yml)
         ↓
┌─────────────────────────────────┐
│   Backend Tests (Python)        │
│   - 3.10, 3.11                  │
│   - pytest -v                   │
└─────────────────────────────────┘
         ↓ (após sucesso)
┌─────────────────────────────────┐
│   Frontend Build (Node.js)      │
│   - npm run build               │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│   Summary                       │
│   ✅ Sucesso ou ❌ Falha       │
└─────────────────────────────────┘
```

---

## Arquivo de Configuração (`.github/workflows/ci.yml`)

### Job 1: Backend Tests

```yaml
backend-tests:
  runs-on: ubuntu-latest
  strategy:
    matrix:
      python-version: ['3.10', '3.11']
```

**O que faz:**
- Roda em servidor Linux da GitHub
- Testa em DUAS versões do Python (3.10 e 3.11)
- Se falhar em qualquer uma, falha a pipeline

**Passos:**
1. ✅ Checkout (clonar repo)
2. ✅ Setup Python
3. ✅ Cache pip (acelera)
4. ✅ Instalar dependências
5. ✅ Rodar `pytest -v`
6. ✅ Gerar relatório de cobertura

**Tempo:** ~30-60s

---

### Job 2: Frontend Build

```yaml
frontend-build:
  needs: backend-tests  # Aguarda backend passar
  runs-on: ubuntu-latest
```

**O que faz:**
- Roda APÓS backend passar
- Compila React/Vite para produção
- Valida se não há erros de build

**Passos:**
1. ✅ Checkout
2. ✅ Setup Node.js 18
3. ✅ Cache npm
4. ✅ `npm ci` (clean install)
5. ✅ `npm run build`

**Tempo:** ~20-40s

---

### Job 3: Summary

```yaml
summary:
  needs: [backend-tests, frontend-build]
  if: always()  # Executa mesmo se falhar
```

**O que faz:**
- Verifica se TUDO passou
- Retorna status geral
- Marca como ✅ ou ❌

---

## Triggers (Quando Executa)

```yaml
on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master, develop ]
```

**Executa quando:**
- ✅ Push em `main`, `master`, `develop`
- ✅ Pull Request para essas branches
- ❌ Push em branches feature (por padrão)

**Para executar em toda branch:**
```yaml
on:
  push:
    branches: [ '**' ]
```

---

## Status da Pipeline

### Ver status no GitHub

1. Ir para repositório
2. Aba **"Actions"**
3. Ver workflows executados
4. Clicar em workflow para detalhes

### Badge no README

Adicionar ao `README.md`:
```markdown
[![CI/CD](https://github.com/seu-usuario/Gerenciador-Estoque/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/Gerenciador-Estoque/actions)
```

---

## Cacheing (Otimização)

### O que é cache?
Armazena dependências para não redownload em cada run.

**Economiza:**
- pip packages: 10-30s
- npm packages: 20-40s

### Como funciona:
1. Primeira execução: Baixa e armazena
2. Próximas execuções: Usa cache
3. Invalida se arquivo `requirements.txt` muda

---

## Variáveis de Ambiente

Para usar variáveis na pipeline:

### Secrets (valores sensíveis)
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

Configurar em: GitHub → Settings → Secrets and variables → Actions

### Variáveis normais
```yaml
env:
  ENVIRONMENT: production
```

### Usar em Python
```python
import os
api_key = os.getenv('API_KEY')
```

---

## Exemplo: Adicionar Novo Passo

Para adicionar linting de Python:

```yaml
- name: Lint with flake8
  run: |
    pip install flake8
    flake8 app --count --select=E9,F63,F7,F82
```

Para adicionar teste de cobertura mínima:

```yaml
- name: Check coverage
  run: |
    pytest --cov=app --cov-fail-under=80
```

---

## Troubleshooting

### Pipeline falha mas testes locais passam
1. Verificar versão Python (use 3.11 em ambos)
2. Limpar pip cache: `pip install --no-cache-dir`
3. Usar `pip-compile` para lock de dependências

### Dependência não instalada na pipeline
Adicionar ao `requirements.txt`:
```
package-name==1.2.3
```

### Build frontend falha
```yaml
- name: Debug build
  run: |
    npm list  # Ver dependências
    npm audit # Verificar vulnerabilidades
```

---

## Boas Práticas

✅ **Fazer:**
- Nomes descritivos para jobs
- Cache para acelerar
- Matrix para testar múltiplas versões
- Notifications (Slack, email)
- Status badges

❌ **Evitar:**
- Executar em main branch (usar develop)
- Artefatos grandes (100MB+)
- Secrets em logs
- Sleep/wait fixo

---

## Próximos Passos

### 1. Adicionar Linting
```bash
pip install flake8 black pylint
```

### 2. Deploy Automático
```yaml
deploy:
  needs: [backend-tests, frontend-build]
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to server
      run: ssh user@server 'cd app && git pull && ./deploy.sh'
```

### 3. Notificações
- Slack
- Email
- GitHub Discussions

### 4. Análise de Cobertura
- Codecov
- Coveralls

---

## Recursos

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Actions Marketplace](https://github.com/marketplace?type=actions)
- [FastAPI CI/CD](https://fastapi.tiangolo.com/deployment/concepts/)
- [Python Best Practices](https://peps.python.org/pep-0008/)
