# Detector de Phishing com Inteligência Artificial

Projeto de Inteligência Artificial, Ciência da Computação, Universidade Presbiteriana Mackenzie, turma 7º N. Professor Ivan Carlos Alcântara de Oliveira.

## Integrantes

- Alexandre Eiji Tomimura Carvalho — RA 10371680 — 10371680@mackenzista.com.br
- João Pedro Pioltini de Oliveira — RA 10425643 — 10425643@mackenzista.com.br
- Matheus Veiga Bacetic Joaquim — RA 10425638 — 10425638@mackenzista.com.br

## Solução

Classificação offline de websites como phishing (0) ou legítimos (1), com 50 atributos numéricos previamente extraídos da base PhiUSIIL. São comparados Regressão Logística, Árvore de Decisão e Random Forest. O protótipo não acessa as páginas da base nem verifica URLs arbitrárias em tempo real.

## Arquivos da entrega

- `artigo/Artigo_Final.pdf`: artigo no formato SBC solicitado.
- `entrega/Rubrica_N2_identificada.docx`: autoavaliação atual de 75/100.
- `notebooks/Projeto_IA_Final.ipynb`: análise e experimento com saídas salvas.
- `src/experimento.py`: aquisição, preparação, treinamento e avaliação.
- `src/demonstrar.py`: inferência offline com exemplos reservados de teste.
- `modelos/arvore.joblib`: modelo treinado para demonstração.
- `resultados/final/`: métricas, matrizes, previsões, estatísticas e metadados.
- `dados/README.md`: origem, licença e acesso à base.

## Como executar

Python 3.12 recomendado. Abra um terminal na raiz deste projeto:

```powershell
python -m pip install -r requirements.txt
python src/experimento.py
python src/demonstrar.py
```

O experimento baixa o CSV da UCI automaticamente para `dados/` se ele não existir. A base grande não acompanha a entrega pelo navegador. Para apenas demonstrar o modelo já treinado, execute `python src/demonstrar.py`; não é preciso baixar a base.

Para usar o notebook, abra a pasta inteira do projeto em um ambiente Jupyter e execute `notebooks/Projeto_IA_Final.ipynb`. O notebook importa o código de `src/`; preserve essa estrutura de pastas.

## Resultados e limites

Na divisão estratificada 80/20, a Regressão Logística teve seis falsos negativos e nenhum falso positivo; árvore e floresta acertaram os 47.159 registros de teste. Na separação por domínio literal, a regressão teve cinco falsos negativos, e cada modelo de árvores teve dois, sem falsos positivos. A ablação sem URLSimilarityIndex aumentou os erros.

Métricas completas: `resultados/final/metricas.csv`. A auditoria identificou 808 repetições de vetores numéricos e 2.110 domínios compartilhados na divisão aleatória. Resultados altos nesta base não garantem detecção de golpes novos. Não houve validação temporal nem em base externa, e a extração original dos atributos pré-computados não foi reconstruída. Utilizar como experimento acadêmico, com revisão humana de decisões em eventual aplicação futura.

## Dados

PhiUSIIL Phishing URL (Website), Arvind Prasad e Shalini Chandra (2024), UCI Machine Learning Repository, ID 967. Licença CC BY 4.0.

Fonte: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset

O código registra a origem, versões e SHA-256 do CSV em `resultados/final/execucao.json`. Não abrir os endereços contidos na base.

## Pendências antes da submissão

A versão final do projeto está publicada neste repositório. Falta gravar e publicar no YouTube o vídeo de até cinco minutos, inserir seu link no artigo e concluir a revisão do grupo. A autoavaliação atual é 75/100 e considera o vídeo ainda ausente; após disponibilizá-lo, revisar o critério de apresentação conforme as evidências. Um integrante envia o artigo PDF e a rubrica Word pelo AVA no prazo da disciplina.

## Assistência de IA

A proposta inicial registra Gemini. Esta etapa contou com assistência do Codex/ChatGPT na programação, redação e revisão. O grupo deve revisar e compreender integralmente o material, declarar corretamente o uso das ferramentas e assumir responsabilidade pela entrega.
