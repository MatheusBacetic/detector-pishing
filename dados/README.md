# PhiUSIIL Phishing URL (Website)

Autores: Arvind Prasad e Shalini Chandra (2024). UCI Machine Learning Repository, ID 967.

Fonte oficial: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset

Licença dos dados: Creative Commons Attribution 4.0 International (CC BY 4.0). Atribuir autores e fonte ao redistribuir. A licença do dataset não é automaticamente uma licença do código do grupo.

CSV: 235.795 registros, 54 atributos, identificador FILENAME e alvo label (56 colunas). `0 = phishing`, `1 = legítimo`. O experimento remove FILENAME e quatro atributos textuais, restando 50 entradas numéricas.

O CSV original não acompanha este pacote; ele é obtido automaticamente por `python src/experimento.py`. SHA-256 e endereço de download são registrados em `resultados/final/execucao.json`. A aquisição não visita nenhum endereço listado no dataset. Os autores originais coletaram os atributos das URLs e páginas; este trabalho não reimplementa essa extração.

Não abrir URLs presentes na base. Utilize o CSV como dados tabulares. Nenhuma credencial é necessária.
