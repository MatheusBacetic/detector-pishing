Detector de Phishing com Inteligência Artificial

Projeto desenvolvido para a disciplina de Inteligência Artificial do curso de Ciência da Computação da Universidade Presbiteriana Mackenzie.

O objetivo é utilizar técnicas de Aprendizado de Máquina Supervisionado para classificar websites como phishing ou legítimos a partir de características estruturais e de conteúdo.

Integrantes

Alexandre Eiji Tomimura Carvalho — RA 10371680

João Pedro Pioltini de Oliveira — RA 10425643

Matheus Veiga Bacetic Joaquim — RA 10425638

Dataset

Foi utilizado o PhiUSIIL Phishing URL (Website) Dataset, disponibilizado pelo UCI Machine Learning Repository.

Link: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset

O conjunto possui:

235.795 registros;

54 atributos;

1 variável alvo (label);

0 = phishing;

1 = legítimo.

Distribuição das classes:

100.945 registros de phishing — 42,81%;

134.850 registros legítimos — 57,19%.

Etapas do projeto

O desenvolvimento foi dividido nas seguintes etapas:

Carregamento do dataset;

Análise exploratória dos dados;

Verificação de valores nulos e duplicados;

Análise da distribuição das classes;

Análise de correlação dos atributos;

Preparação dos dados;

Divisão em treino e teste;

Treinamento dos modelos;

Avaliação dos resultados;

Comparação entre os modelos.

Preparação dos dados

O dataset não apresentou valores nulos nem registros duplicados.

As colunas textuais abaixo foram retiradas do conjunto utilizado diretamente pelos modelos:

URL

Domain

TLD

Title

Foram utilizadas 50 características numéricas para o treinamento.

Os dados foram divididos em:

80% para treinamento;

20% para teste.

A divisão foi estratificada para preservar a proporção entre phishing e sites legítimos.

Modelos utilizados

Foram avaliados três algoritmos de classificação:

Regressão Logística;

Árvore de Decisão;

Random Forest.

Para a Regressão Logística foi utilizado StandardScaler para padronização dos atributos.

Métricas de avaliação

Os modelos foram avaliados utilizando:

Accuracy;

Precision;

Recall;

F1-Score;

Matriz de Confusão.

Como o objetivo principal do projeto é detectar ataques, a classe phishing (0) foi considerada como classe positiva nas métricas de Precision, Recall e F1-Score.

Resultados

A Regressão Logística apresentou desempenho elevado no conjunto de teste:

Accuracy: 0,9999;

Precision para phishing: 1,0000;

Recall para phishing: 0,9997;

F1-Score para phishing: 0,9999.

Na matriz de confusão, apenas 6 registros de phishing foram classificados como legítimos, enquanto nenhum site legítimo foi classificado incorretamente como phishing.

Também foi realizada uma análise removendo o atributo URLSimilarityIndex. Mesmo sem esse atributo, a Regressão Logística manteve desempenho elevado, indicando que a classificação não depende exclusivamente de uma única característica.

Os resultados completos da Árvore de Decisão, Random Forest e a comparação entre os modelos estão disponíveis no notebook do projeto.

Estrutura do repositório

projeto-phishing-ia/
│
├── README.md
├── artigo/
│   └── artigo_parcial.pdf
│
├── notebooks/
│   └── Projeto_IA.ipynb
│
├── dados/
│   └── README.md
│
└── resultados/
    ├── distribuicao_classes.png
    ├── correlacoes_top10.png
    ├── matriz_regressao.png
    ├── matriz_arvore.png
    ├── matriz_random_forest.png
    ├── importancia_arvore.png
    ├── importancia_random_forest.png
    ├── comparacao_modelos.png
    └── comparacao_modelos.csv

Como executar

O projeto pode ser executado no Google Colab.

Abra o arquivo Projeto_IA.ipynb;

Execute as células em ordem;

O dataset é carregado diretamente do UCI Machine Learning Repository;

Ao final do notebook serão exibidas as métricas, matrizes de confusão e comparações entre os modelos.

Principais bibliotecas utilizadas:

pandas
numpy
matplotlib
scikit-learn
ucimlrepo

Aspectos éticos

Um detector de phishing pode cometer dois tipos importantes de erro:

Falso negativo: um site de phishing é classificado como legítimo;

Falso positivo: um site legítimo é classificado como phishing.

Por isso, o modelo deve ser utilizado como uma ferramenta de apoio à segurança e não como garantia absoluta de que um site é seguro.

Também é importante atualizar periodicamente os dados e os modelos, já que novas estratégias de phishing surgem constantemente.

Artigo

O artigo parcial do projeto está disponível na pasta artigo/.

Status

Parte 2 — análise exploratória, preparação dos dados, implementação dos modelos e resultados parciais concluídos.
