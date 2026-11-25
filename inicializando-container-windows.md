#### Inicializando o contêiner no Windows:

**Resumo do problema:**

Ao subir o projeto no Docker pelo Windows, dois problemas comuns costumam derrubar o contêiner da API:

1. **Incompatibilidade de quebra de linha (`CRLF` vs. `LF`):** O Windows salva o arquivo `entrypoint.sh` no formato `CRLF`, fazendo com que o Linux dentro do container falhe ao executar o script (`env: 'bash\r': No such file or directory`).
2. **Conflito de portas:** Se outra API ou banco de dados já estiver usando a mesma porta na máquina local (como a `8000` ou `5432`), o novo container é encerrado por não conseguir alocar a porta.

Siga os passos abaixo para preparar o ambiente e iniciar a aplicação:

**1. Preparação do ambiente**

- **Inicie o Docker Desktop** e aguarde o motor ficar ativo.
- **Ajuste o `entrypoint.sh`:** Abra o arquivo no VS Code, clique em **`CRLF`** (canto inferior direito), altere para **`LF`** e salve (**`Ctrl + S`**).
- **Evite conflito de portas (se já tiver uma API inicializada):** No `docker-compose.yml`, caso já tenha serviços rodando, altere a porta externa da API (ex.: de `"8000:8000"` para **`"8002:8000"`**) e verifique a porta do banco de dados (ex.: `5432`). Salve o arquivo.

**2. Construção e inicialização**

No terminal (PowerShell), acesse a pasta do projeto e suba os contêineres:

```powershell
cd api-saas
docker compose up -d --build
```

**3. Verificação e logs**

Confirme se o contêiner está ativo e acompanhe os logs para garantir que as *migrations* e o servidor subiram sem erros:

```powershell
docker ps
docker compose logs -f api
```

**4. Teste e documentação**

- **Health check (via terminal):** *Resposta esperada:* `{"status":"ok"}`

  ```powershell
  curl.exe http://localhost:8002/health
  ```

- **Documentação interativa (via navegador):**
  - **Swagger UI:** `http://localhost:8002/docs`
  - **ReDoc:** `http://localhost:8002/redoc`
