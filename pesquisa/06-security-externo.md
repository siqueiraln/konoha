# 06 — Security: referências externas atuais

Pesquisa feita em 2026-09-26, só com páginas abertas nesta sessão. Legenda: **[fato]** = está na página linkada; **[dedução]** = conclusão minha para o nosso stack (React + Vite na Vercel, Supabase, WhatsApp Cloud API, n8n, LLM).

---

## 1. OWASP Top 10 (web)

- [fato] A edição vigente é a **OWASP Top 10:2025**: "This is the 2025 version of the OWASP Top 10". — https://top10.owasp.org/2025
- [fato] A lista:
  - A01:2025 Broken Access Control
  - A02:2025 Security Misconfiguration
  - A03:2025 Software Supply Chain Failures
  - A04:2025 Cryptographic Failures
  - A05:2025 Injection
  - A06:2025 Insecure Design
  - A07:2025 Authentication Failures
  - A08:2025 Software or Data Integrity Failures
  - A09:2025 Security Logging and Alerting Failures
  - A10:2025 Mishandling of Exceptional Conditions
- [fato] Mudanças em relação a 2021 (https://top10.owasp.org/2025/0x00_2025-Introduction/):
  - Categorias novas: A03 Software Supply Chain Failures (amplia o antigo "Vulnerable and Outdated Components") e A10 Mishandling of Exceptional Conditions.
  - O SSRF (antigo A10:2021) entrou em A01 Broken Access Control.
  - Security Misconfiguration subiu de #5 para #2. Cryptographic Failures caiu de #2 para #4, Injection de #3 para #5 e Insecure Design de #4 para #6.
  - Renomeações: "Identification and Authentication Failures" virou "Authentication Failures", e "Security Logging and Monitoring Failures" virou "…Logging & Alerting Failures".
  - Os autores passaram a priorizar a causa raiz em vez do sintoma. A base de dados agora tem 589 CWEs e 2,8 milhões de aplicações.
- [fato] O A03:2025 recomenda: gerar e gerenciar SBOM, monitorar dependências continuamente, usar só fontes oficiais (de preferência pacotes assinados), fazer rollout escalonado, proteger CI/CD e estações de desenvolvimento com MFA, e separar funções para que ninguém promova código para produção sozinho. A página cita o worm Shai-Hulud (2025) como exemplo. — https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/
- [dedução] No nosso stack, A01 corresponde principalmente a **RLS ausente ou fraca no Supabase** e a Edge Functions sem checagem de autorização. A02 corresponde a headers ausentes, `verify_jwt` desligado sem substituto e buckets públicos. A03 corresponde a npm e a nós comunitários do n8n.

## 2. OWASP ASVS

- [fato] A versão estável vigente é a **ASVS 5.0.0 (maio de 2025)**, "Released LIVE on stage at Global AppSec EU Barcelona 2025". A próxima prevista é a 5.0.1. Está publicada em PDF, Word e **CSV**. Licença CC BY-SA 4.0. — https://github.com/OWASP/ASVS
- [fato] Níveis (https://raw.githubusercontent.com/OWASP/ASVS/v5.0.0/5.0/en/0x03-What-is-the-ASVS.md):
  - **L1**: "the minimum requirements to consider when securing an application". Cobre cerca de 20% dos requisitos.
  - **L2**: "Most applications should be striving to achieve this level of security". Cobre cerca de 50% dos requisitos, e L1+L2 somam cerca de 70% do total.
  - **L3**: para quem quer demonstrar o nível mais alto de segurança. Cobre os ~30% restantes (defesa em profundidade).
  - Cada nível inclui o anterior. A escolha depende do risco: um exemplo do texto é uma startup com poucos dados sensíveis mirar L1, enquanto um banco miraria L3.
  - Escopo: requisitos verificáveis do software em si. Ficam de fora DNS, backups e políticas puramente administrativas.
- [fato] Os 17 capítulos (https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en): V1 Encoding and Sanitization, V2 Validation and Business Logic, V3 Web Frontend Security, V4 API and Web Service, V5 File Handling, V6 Authentication, V7 Session Management, V8 Authorization, V9 Self-contained Tokens, V10 OAuth and OIDC, V11 Cryptography, V12 Secure Communication, V13 Configuration, V14 Data Protection, V15 Secure Coding and Architecture, V16 Security Logging and Error Handling, V17 WebRTC.
- [fato] Uma fonte secundária aponta cerca de 345 requisitos: L1 = 70, L2 = 183, L3 = 92. — resultado de busca (https://www.securecodinghub.com/blog/owasp-asvs-4-vs-5-changes-developers). Não conferi no CSV.
- [dedução] Capítulos que mais importam para SaaS B2B em Supabase:
  - **V8 Authorization**: RLS e isolamento entre tenants.
  - **V4 API**: Edge Functions e PostgREST.
  - **V3 Web Frontend**: CSP e headers da SPA.
  - **V13 Configuration**: segredos e configuração de deploy.
  - **V14 Data Protection**: LGPD.
  - **V16 Logging**.
  - **V5 File Handling**: Supabase Storage.
  - **V6/V7/V9**: Supabase Auth, sessões e JWT.
  - **V2 Business Logic**.
  - V17 WebRTC não se aplica.
- [dedução] Sugestão: o agente mira **L2 como padrão** e usa o CSV da 5.0.0 como checklist verificável, citando o ID do requisito, no formato `capítulo.seção.requisito`, como está no repositório.

## 3. OWASP para LLM e agentes

### 3a. Top 10 for LLM Applications — a edição vigente é **2026**
- [fato] A edição 2026 foi publicada em agosto de 2026: a página oficial diz 3 de agosto e o repositório diz 4 de agosto. — https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ e https://github.com/GenAI-Security-Project/GenAI-LLM-Top10
- [fato] A lista, conforme o repositório oficial:
  - LLM01:2026 Prompt Injection
  - LLM02:2026 Sensitive Information Disclosure
  - LLM03:2026 **Excessive Agency**
  - LLM04:2026 Supply Chain
  - LLM05:2026 Data and Model Poisoning
  - LLM06:2026 Unbounded Consumption
  - LLM07:2026 Misinformation
  - LLM08:2026 **Hidden Context Exposure** (antes chamada "System Prompt Leakage")
  - LLM09:2026 Vector and Embedding Weaknesses
  - LLM10:2026 Improper Output Handling
- [fato] Mudanças em relação a 2025 (https://www.helpnetsecurity.com/2026/08/06/owasp-2026-llm-top-10-released/ e https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/):
  - Excessive Agency subiu para #3.
  - Output Handling caiu de #5 para #10.
  - Prompt Injection passou a cobrir ataques cross-modal (imagem e áudio).
  - Pela primeira vez, a metodologia pesou 75% em votos de especialistas e 25% em incidentes reais.
  - Frase-guia: "Build the system around it, so that when the model is fooled, and it will be, nothing important breaks."
- [fato] Um site secundário (cybersecuritynews.com) publicou uma ordem **diferente** para a lista 2026. Usei a do repositório oficial.
- [fato] Edição anterior (2025), ainda muito citada: LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation, LLM10 Unbounded Consumption. — https://genai.owasp.org/llm-top-10/
- [fato] Também em setembro de 2026 saiu o **Agent Control Standard (ACS)**, voltado a "practical runtime enforcement" (aplicação de controles em tempo de execução). — mesma página de 01/09/2026

### 3b. Top 10 for Agentic Applications (2026)
- [fato] Publicado em 9 de dezembro de 2025. — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- [fato] A lista (https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/):
  - ASI01 Agent Goal Hijack (ex.: EchoLeak)
  - ASI02 Tool Misuse
  - ASI03 Identity & Privilege Abuse
  - ASI04 Agentic Supply Chain Vulnerabilities (ex.: exploit do GitHub MCP)
  - ASI05 Unexpected Code Execution
  - ASI06 Memory & Context Poisoning
  - ASI07 Insecure Inter-Agent Communication
  - ASI08 Cascading Failures
  - ASI09 Human-Agent Trust Exploitation
  - ASI10 Rogue Agents

### 3c. Mitigações oficiais relevantes (páginas 2025, que ainda estão no ar)
- [fato] **Prompt injection** (https://genai.owasp.org/llmrisk/llm01-prompt-injection/):
  - A injeção **indireta** chega por sites ou arquivos com instruções escondidas.
  - Mitigações listadas:
    - Restringir o comportamento do modelo no system prompt.
    - Validar o formato da saída com código.
    - Filtrar entrada e saída.
    - Dar ao modelo o menor privilégio possível.
    - Exigir aprovação humana para operações de alto risco.
    - Segregar e marcar conteúdo externo.
    - Fazer testes adversariais.
- [fato] **Excessive Agency** (https://genai.owasp.org/llmrisk/llm062025-excessive-agency/):
  - Três causas: funcionalidade, permissão e autonomia em excesso.
  - Mitigações listadas:
    - Evitar ferramentas abertas, como shell ou busca de URL arbitrária.
    - Executar extensões no contexto do usuário.
    - Exigir aprovação humana para ações de alto impacto.
    - "Enforce authorization in downstream systems, not LLMs": a autorização fica no sistema de destino, não no modelo.
    - Registrar em log as ações das ferramentas.
    - Aplicar rate limit.
- [fato] **Sensitive Information Disclosure** (https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/): sanitizar dados antes do treino ou do contexto, dar menor privilégio às fontes, restringir acesso ao system prompt, não vazar detalhes em mensagens de erro e redigir dados com tokenização ou padrões.
- [dedução] Pontos de atenção no nosso stack:
  - **Mensagens de WhatsApp recebidas** são entrada não confiável e podem trazer injeção indireta.
  - O LLM nunca deve usar a `service_role`/secret key. Ações devem rodar com o JWT do usuário, para a RLS valer.
  - Envio de mensagens, exclusões e cobranças pedem confirmação humana.
  - Limite de tokens e custo por tenant (Unbounded Consumption).

## 4. Cadeia de suprimentos npm

### Incidentes 2025–2026
- [fato] **Shai-Hulud (set/2025)**:
  - Worm autorreplicante que comprometeu mais de 500 pacotes.
  - Roubava PATs do GitHub e chaves de AWS, GCP e Azure, e publicava versões trojanizadas com os tokens roubados.
  - Recomendações da CISA:
    - Auditar `package-lock.json` e `yarn.lock`.
    - Fixar versões anteriores a 16/09/2025.
    - Rotacionar credenciais.
    - Adotar MFA resistente a phishing.
    - Ativar branch protection, GitHub Secret Scanning e Dependabot.
  - Fonte: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
- [fato] **Shai-Hulud 2.0 (24/11 a 01/12/2025)**:
  - Usava script `preinstall` que instalava o runtime Bun e rodava o TruffleHog para colher segredos.
  - Afetou pacotes de Zapier, PostHog e Postman, entre outros.
  - Houve uma nova onda ("Mini Shai-Hulud") em **11/05/2026**, com mais de 170 pacotes npm.
  - Fonte: https://www.microsoft.com/en-us/security/blog/2025/12/09/shai-hulud-2-0-guidance-for-detecting-investigating-and-defending-against-the-supply-chain-attack/
- [fato] **axios (31/03/2026)**:
  - Versões `axios@1.14.1` e `0.30.4` maliciosas, com a dependência `plain-crypto-js@4.2.1` carregando um trojan de acesso remoto (RAT).
  - A CISA recomenda `ignore-scripts=true` e `min-release-age=7` no `.npmrc`.
  - Fonte: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager
- [fato] **keyv/cacheable, worm "ChainDrop" (04/08/2026)**:
  - Conta GitHub de um mantenedor comprometida. Mais de 1.300 versões afetadas, cerca de 2 bilhões de downloads por mês.
  - Mecanismo: `preinstall` rodando `setup.mjs` com Bun para roubar credenciais, inclusive da memória do GitHub Actions.
  - Fontes: https://www.csa.gov.sg/alerts-and-advisories/advisories/ad-2026-009/ e https://securitylabs.datadoghq.com/articles/npm-worm-compromises-popular-npm-packages/
- [fato] Os resultados de busca citaram um caso via `binding.gyp`/node-gyp (Snyk), mas **não abri** a página. As duas fontes que abri sobre o keyv não confirmam esse vetor.

### Recomendações oficiais
- [fato] **GitHub/npm (22/09/2025)** (https://github.blog/security/supply-chain-security/our-plan-for-a-more-secure-npm-supply-chain/):
  - Publicar só de três formas: localmente com 2FA, com tokens granulares de no máximo 7 dias, ou por **trusted publishing**.
  - Os tokens clássicos serão descontinuados e a 2FA por TOTP será substituída por FIDO/WebAuthn.
- [fato] **Configurações da CLI do npm** (https://docs.npmjs.com/cli/v11/using-npm/config):
  - `min-release-age`: instala só versões publicadas há mais de N dias.
  - `before`: instala só versões publicadas até uma data.
  - `ignore-scripts` (padrão `false`): pula scripts de ciclo de vida.
  - `allow-git` (`all`/`none`/`root`): restringe dependências que vêm de repositórios git.
  - `allow-scripts`: allowlist de pacotes cujos scripts podem rodar em `npm exec`/`npx`.
- [fato] **Provenance** (https://docs.npmjs.com/generating-provenance-statements):
  - Funciona com Sigstore e publicação em GitHub Actions ou GitLab CI com runner na nuvem. O consumidor verifica com `npm audit signatures`.
  - Limite declarado: "provenance does not guarantee the package has no malicious code".
- [fato] **OpenSSF** (https://github.com/ossf/package-manager-best-practices/blob/main/published/npm.md):
  - Versionar o lockfile, que fixa hashes.
  - Usar `npm ci` em CI e produção, porque ele trata o lockfile como somente leitura.
  - Usar `npm install` só para mudar dependências de propósito.
  - Consultar Scorecard e deps.dev, rodar `npm audit` periodicamente e usar Dependabot ou Renovate.
  - Usar escopo `@org` contra dependency confusion.
  - Observação: o repositório foi **arquivado em 09/10/2023**, mas o conteúdo continua válido como referência.
- [fato] Alternativa ao `npm audit`: o OSV-Scanner (Google) cruza as dependências com a base aberta OSV. — https://google.github.io/osv-scanner/
- [dedução] Checklist para o agente:
  - Lockfile versionado e `npm ci` no build da Vercel e no CI.
  - `.npmrc` com `ignore-scripts=true` e `min-release-age=7`, com exceções justificadas.
  - Toda dependência nova ou mudança de lockfile passa por revisão: idade da versão, mantenedor, scripts de instalação.
  - `npm audit` ou OSV-Scanner mais `npm audit signatures`.
  - Nunca usar `latest` nem `*`.
  - O mesmo cuidado vale para nós comunitários do n8n e para imports remotos em Edge Functions Deno. Isso é dedução por analogia: não achei fonte específica.

## 5. Segredos

- [fato] **GitHub Secret Scanning** (https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning):
  - Varre todo o histórico git, em todos os branches, além de issues, PRs, wikis e gists.
  - É grátis em repositórios públicos. Em privados, exige **GitHub Secret Protection** (planos Team ou Enterprise).
  - Oferece checagem de validade do segredo, padrões customizados e detecção com IA.
- [fato] **Push protection** (https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection):
  - Bloqueia o push que contém o segredo.
  - Vem ligada por padrão na conta do usuário, mas só para pushes em repositórios públicos.
  - No nível do repositório vem desligada: um admin precisa ativar.
- [fato] **gitleaks** (https://github.com/gitleaks/gitleaks):
  - Modos `git`, `dir` e `stdin`. Funciona como hook de pre-commit.
  - Gera relatório em SARIF, JSON e outros formatos. Aceita `.gitleaksignore` e comentários `gitleaks:allow`.
  - O projeto se declara **feature-complete**: daqui em diante, só correções de segurança.
- [fato] **Se vazou**, o GitHub manda primeiro **revogar ou rotacionar**:
  - "as a first step you need to revoke and/or rotate that secret".
  - Só depois, se ainda for preciso, reescrever o histórico com `git-filter-repo` (versão 2.47 ou mais, flag `--sensitive-data-removal`).
  - Efeitos colaterais da reescrita: clones antigos podem reintroduzir o segredo, hashes mudam, diffs de PR somem, assinaturas se perdem.
  - Fonte: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- [fato] **Supabase** (https://supabase.com/docs/guides/api/api-keys):
  - A chave publishable pode ficar exposta, porque "it only reaches what Row Level Security allows".
  - A secret key nunca vai para navegador, app distribuído ou repositório, porque "bypass every Row Level Security policy".
  - Rotação: criar a chave nova, atualizar os componentes e depois apagar a vazada.
  - A doc diz: "Fix the root cause of the leak before you rotate anything".
- [dedução] Há tensão entre as fontes: o GitHub manda rotacionar primeiro; o Supabase manda corrigir a causa antes. Proposta de ordem:
  1. Revogar ou rotacionar já, se o segredo estiver público.
  2. Corrigir a origem do vazamento.
  3. Limpar o histórico, se necessário.
  4. Checar logs de uso.
- [fato] **Vite**: "VITE_* variables should _not_ contain sensitive information such as API keys", porque vão para o bundle do cliente. — https://vite.dev/guide/env-and-mode
- [dedução] Regra do agente: todo `VITE_*` é público. Se aparecer `service_role`, `sb_secret_`, token da Meta, chave de LLM ou webhook do n8n com `VITE_`, é bloqueante.

## 6. Webhooks Meta / WhatsApp

- [fato] **GET de verificação** (https://developers.facebook.com/docs/graph-api/webhooks/getting-started):
  - Chegam os parâmetros `hub.mode=subscribe`, `hub.challenge` e `hub.verify_token`.
  - O endpoint "must verify that the hub.verify_token value matches the string you set in the Verify Token field" e responde com o `hub.challenge`.
- [fato] **POST de evento** (mesma página):
  - Header `X-Hub-Signature-256`.
  - Calcular HMAC-SHA256 do **payload bruto** com o **App Secret** e comparar com o valor depois de `sha256=`.
  - Responder `200 OK`.
  - Se não receber 200, a Meta tenta de novo por até 36 horas, então é preciso **deduplicar**.
  - Certificado autoassinado não é aceito. mTLS é opcional, com CN `client.webhooks.fbclientcerts.com`.
- [fato] **Especificidades do WhatsApp Cloud API** (https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks):
  - Payload de até 3 MB.
  - Retentativas por **até 7 dias** se a resposta não for 200.
  - mTLS disponível. A página também fala em allowlist de IPs da Meta.
- [fato] **Supabase Edge Functions**:
  - `verify_jwt` vem ligado por padrão. Webhooks externos precisam desligá-lo.
  - Aviso da doc: "it will allow anyone to invoke your Edge Function without a valid JWT".
  - Nesse caso, a recomendação é verificar a assinatura criptográfica do webhook.
  - Fonte: https://supabase.com/docs/guides/functions/function-configuration
- [dedução] Checklist para a Edge Function que recebe o webhook:
  1. `verify_jwt=false` só nessa função.
  2. Ler o corpo com `await req.text()` **antes** de fazer `JSON.parse`, para o HMAC bater com o payload bruto.
  3. Comparação em tempo constante.
  4. App Secret em variável de ambiente, nunca no código.
  5. Rejeitar com 401 ou 403 quando a assinatura não bater.
  6. Deduplicar pelo id da mensagem.
  7. Responder 200 rápido e processar de forma assíncrona.
  8. O `verify_token` é diferente do App Secret e não serve para autenticar o POST.

## 7. Headers de segurança para SPA na Vercel

- [fato] **Sintaxe no `vercel.json`**: `"headers": [{ "source": "/(.*)", "headers": [{ "key": "...", "value": "..." }] }]`. O exemplo oficial inclui `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY` e `X-XSS-Protection: 1; mode=block`. Para SPA, o rewrite é `{ "source": "/(.*)", "destination": "/index.html" }`. Doc atualizada em 14/08/2026. A página também menciona `vercel.ts` como configuração programática. — https://vercel.com/docs/project-configuration/vercel-json
- [fato] Atenção: a OWASP recomenda `X-XSS-Protection: 0` ou omitir o header, e usar CSP no lugar. Nisso o exemplo da Vercel está desatualizado. — https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
- [fato] **HSTS na Vercel**: HTTP é sempre redirecionado para HTTPS com 308, e isso não pode ser desligado.
  - Padrão em domínio próprio: `Strict-Transport-Security: max-age=63072000;`, sem `includeSubDomains` e sem `preload`.
  - Em `*.vercel.app`, o padrão já inclui `includeSubDomains; preload`.
  - O header pode ser sobrescrito com headers customizados.
  - Fonte: https://vercel.com/docs/cdn-security/encryption
- [fato] **CSP** (https://vercel.com/docs/cdn-security/security-headers):
  - Começar com `Content-Security-Policy-Report-Only`.
  - Evitar `unsafe-inline` e `unsafe-eval`, e usar nonce ou hash.
  - Listar origens específicas, sem curingas amplos.
- [fato] **Valores de referência da OWASP** (cheat sheet acima):
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`, ou preferir `frame-ancestors` na CSP
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
  - `Cross-Origin-Opener-Policy: same-origin`
  - `Permissions-Policy: geolocation=(), camera=(), microphone=()`
  - CORS com origem exata, sem `*`.
- [dedução] Ponto de partida para a CSP de uma SPA Vite com Supabase: `default-src 'self'; script-src 'self'; connect-src 'self' https://<ref>.supabase.co wss://<ref>.supabase.co; img-src 'self' data: https://<ref>.supabase.co; frame-ancestors 'none'; base-uri 'self'; object-src 'none'`. Validar primeiro em modo Report-Only. O build do Vite normalmente não precisa de `unsafe-inline` em script. Isso é dedução: não verifiquei.

## 8. LGPD / ANPD

- [fato] **Resolução CD/ANPD nº 15, de 24/04/2024** (Regulamento de Comunicação de Incidente de Segurança). Texto: https://bibliotecadigital.mj.gov.br/bitstream/1/12879/2/RES_ANPD_2024_15.html
  - Art. 3º, XII: incidente é "qualquer evento adverso confirmado, relacionado à violação das propriedades de confidencialidade, integridade, disponibilidade e autenticidade da segurança de dados pessoais".
  - Art. 4º: o controlador comunica à ANPD e ao titular o incidente "que possa acarretar risco ou dano relevante".
  - Art. 5º: é **relevante** quando o incidente pode afetar significativamente interesses e direitos fundamentais **e, cumulativamente**, envolve ao menos um destes tipos de dado:
    - dados sensíveis;
    - dados de crianças, adolescentes ou idosos;
    - dados financeiros;
    - **dados de autenticação em sistemas**;
    - dados protegidos por sigilo;
    - dados em larga escala.
  - Art. 5º, §1º: o impacto é significativo quando impede o exercício de direitos ou causa dano material ou moral, por exemplo discriminação, fraude financeira ou roubo de identidade.
  - Art. 6º: o prazo é de **3 dias úteis**, contados do conhecimento de que o incidente afetou dados pessoais. A complementação tem prazo de **20 dias úteis**.
  - Art. 9º: a comunicação ao titular também tem prazo de 3 dias úteis, deve usar "linguagem simples" e ser individual quando possível. Se não for, a divulgação fica em site, app e redes sociais por no mínimo 3 meses.
  - Art. 10: registrar **todo** incidente, inclusive os não comunicados, por **no mínimo 5 anos**.
  - Agentes de pequeno porte têm os prazos contados em dobro (art. 6º, §8º, e art. 9º, §6º).
- [fato] **Canal de comunicação**: SEI!ANPD (https://sei.anpd.gov.br/), processo do tipo "ANPD – Comunicados de Incidentes". Quem comunica é o encarregado (DPO) ou um representante legal. Dúvidas vão para incidentes@anpd.gov.br. — https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis
- [fato] **LGPD, Lei 13.709/2018** (publicação original em https://www2.camara.leg.br/legin/fed/lei/2018/lei-13709-14-agosto-2018-787077-publicacaooriginal-156212-pl.html; o Planalto não abriu):
  - Art. 6º, III (necessidade): "limitação do tratamento ao mínimo necessário para a realização de suas finalidades".
  - Art. 6º, VII: princípio da segurança.
  - Art. 46: medidas técnicas e administrativas de segurança, e §2º: "desde a fase de concepção do produto ou do serviço até a sua execução".
  - Art. 37: o controlador e o operador mantêm registro das operações de tratamento.
- [fato] **Dado pessoal sensível** (art. 5º, II, segundo o glossário da ANPD): origem racial ou étnica, convicção religiosa, opinião política, filiação sindical ou a organização religiosa, filosófica ou política, dado de saúde ou vida sexual, dado genético ou biométrico. — https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/glossario-anpd/d
- [fato] **Logs** (OWASP Logging Cheat Sheet): não registrar diretamente tokens de acesso, IDs de sessão, senhas, connection strings, chaves, dados de pagamento, dados pessoais sensíveis e alguns PII. Nome, telefone e e-mail exigem tratamento especial, como pseudonimização. — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- [dedução] O agente deve sinalizar:
  - Tabelas ou colunas com dado sensível, por exemplo campo de saúde em CRM de clínica, sem RLS por tenant.
  - Coleta de campo sem finalidade clara (necessidade).
  - `console.log` ou log de Edge Function com telefone, CPF, corpo de mensagem de WhatsApp, token ou JWT.
  - Envio de dado pessoal ao LLM ou ao n8n sem necessidade.
  - Bucket de Storage público com documentos.
  - Ausência de registro de incidentes.
  - **Vazamento de credencial (dado de autenticação) é um dos gatilhos do art. 5º**: segredo vazado com acesso a dado pessoal pede avaliação LGPD, não só rotação.

---

## Onde procurei e não achei

- A página do projeto ASVS em owasp.org (`/www-project-application-security-verification-standard/`) deu 404. Usei o repositório GitHub.
- O arquivo `0x03-Using-ASVS.md` e o `0x03-Overview.md` da ASVS 5.0 não existem (404). O conteúdo dos níveis está em `0x03-What-is-the-ASVS.md`.
- A contagem exata de requisitos por nível na ASVS 5.0 veio só de fonte secundária. Não abri o CSV oficial.
- A lista completa da LLM Top 10 2026 não aparece na página de recurso nem no anúncio do genai.owasp.org. Veio do README do repositório GitHub oficial. Um site secundário traz outra ordem.
- Não encontrei página do Agentic Top 10 com mitigações detalhadas por item, só a lista. Também não abri o documento do Agent Control Standard.
- O site do Planalto (texto compilado da LGPD) deu ECONNRESET três vezes. Usei a publicação original da Câmara, que pode não ter alterações posteriores.
- O verbete do glossário da ANPD sobre o princípio da necessidade deu 404.
- Não achei documentação oficial do n8n sobre segurança de nós comunitários, nem da Supabase sobre supply chain em Edge Functions Deno. Não pesquisei a fundo.
- O ataque via `binding.gyp`/node-gyp (Snyk) apareceu na busca, mas não abri a página.
- A página do OSV-Scanner não trouxe a comparação com o `npm audit` nem a lista de lockfiles suportados.
