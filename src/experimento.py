"""Experimento final reproduzível: classificação de websites no PhiUSIIL.
Integrantes: Alexandre Eiji Tomimura Carvalho (10371680), João Pedro Pioltini
de Oliveira (10425643), Matheus Veiga Bacetic Joaquim (10425638).
Histórico: 2026-11-18 | assistência Codex, para revisão do grupo | pipeline final.
Não acessa websites do dataset; trabalha somente com atributos já coletados.
"""
from pathlib import Path
import hashlib
import io
import json
import platform
import time
import urllib.request
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn
import joblib
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'resultados/final'
DATA = ROOT / 'dados/PhiUSIIL_Phishing_URL_Dataset.csv'
URL = 'https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip'
SEED = 42

def load_data():
    DATA.parent.mkdir(exist_ok=True)
    if not DATA.exists():
        print('Baixando dataset oficial UCI...', flush=True)
        req = urllib.request.Request(URL, headers={'User-Agent': 'Academic-Phishing-Project/1.0'})
        with urllib.request.urlopen(req, timeout=180) as response:
            blob = response.read()
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            names = [n for n in archive.namelist() if n.endswith('.csv')]
            if len(names) != 1:
                raise ValueError('Arquivo UCI inesperado')
            DATA.write_bytes(archive.read(names[0]))
    return pd.read_csv(DATA)

def models():
    return {
        'Referência majoritária': DummyClassifier(strategy='most_frequent'),
        'Regressão Logística': make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, random_state=SEED)),
        'Árvore de Decisão': DecisionTreeClassifier(random_state=SEED),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=SEED, n_jobs=4),
    }

def evaluate(name, model, xtr, xte, ytr, yte, protocol, save=False):
    start = time.perf_counter()
    model.fit(xtr, ytr)
    elapsed = time.perf_counter()-start
    pred = model.predict(xte)
    cm = confusion_matrix(yte, pred, labels=[0, 1])
    row = dict(protocolo=protocol, modelo=name, treino=len(ytr), teste=len(yte), atributos=xtr.shape[1],
               acuracia=accuracy_score(yte, pred), precisao=precision_score(yte, pred, pos_label=0, zero_division=0),
               recall=recall_score(yte, pred, pos_label=0, zero_division=0), f1=f1_score(yte, pred, pos_label=0, zero_division=0),
               phishing_detectado=int(cm[0,0]), phishing_liberado=int(cm[0,1]), legitimo_bloqueado=int(cm[1,0]), legitimo_liberado=int(cm[1,1]),
               segundos_treino=elapsed)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    slug={'Regressão Logística':'logistica','Árvore de Decisão':'arvore','Random Forest':'floresta','Referência majoritária':'baseline'}[name]
    if save:
        fig, ax = plt.subplots(figsize=(5,4))
        ConfusionMatrixDisplay(cm, display_labels=['Phishing (0)', 'Legítimo (1)']).plot(ax=ax, colorbar=False, cmap='Blues', values_format='d')
        ax.set(xlabel='Classe prevista', ylabel='Classe real', title=name)
        fig.tight_layout(); fig.savefig(OUT/f'matriz_{slug}.png', dpi=180); plt.close(fig)
        pd.DataFrame({'indice_original': xte.index, 'real': np.asarray(yte), 'previsto': pred}).to_csv(OUT/f'previsoes_{slug}.csv', index=False)
    return row

def run():
    OUT.mkdir(parents=True, exist_ok=True)
    df=load_data()
    y=df['label'].astype(int)
    x=df.drop(columns=['label','FILENAME','URL','Domain','TLD','Title'], errors='ignore').select_dtypes(include=np.number)
    if x.isna().any().any() or not np.isfinite(x.to_numpy()).all():
        raise ValueError('Dados numéricos ausentes ou não finitos: revisar preparação')
    if set(y.unique()) != {0,1}: raise ValueError('Rótulos inesperados')
    meta={'fonte':URL, 'licenca':'CC BY 4.0', 'sha256_csv':hashlib.sha256(DATA.read_bytes()).hexdigest(),
          'linhas':len(df), 'colunas_csv':len(df.columns), 'atributos_numericos':len(x.columns),
          'nulos':int(df.isna().sum().sum()), 'duplicados_completos':int(df.duplicated().sum()),
          'duplicados_atributos_numericos':int(x.duplicated().sum()),
          'classes':{str(k):int(v) for k,v in y.value_counts().items()},
          'python':platform.python_version(),'sklearn':sklearn.__version__,'pandas':pd.__version__,'numpy':np.__version__,
          'semente':SEED, 'classe_positiva':0}
    df.dtypes.astype(str).rename('tipo').to_csv(OUT/'dicionario_tipos.csv')
    x.describe().T.to_csv(OUT/'estatisticas.csv')
    fig,ax=plt.subplots(figsize=(5.5,3.2)); ax.bar(['Phishing','Legítimo'],[int((y==0).sum()),int((y==1).sum())],color=['#30496b','#91a9bf']); ax.set(ylabel='Registros',title='Distribuição das classes'); fig.tight_layout(); fig.savefig(OUT/'classes.png',dpi=180); plt.close(fig)
    tr,te=train_test_split(np.arange(len(df)),test_size=.2,random_state=SEED,stratify=y)
    # Correlações apenas no treino; não orientam seleção de atributos no teste.
    corr=x.iloc[tr].corrwith(y.iloc[tr]).sort_values(key=abs,ascending=False)
    corr.to_csv(OUT/'correlacoes_treino.csv')
    meta['dominios_sobrepostos_divisao_aleatoria']=len(set(df.Domain.iloc[tr].str.lower()) & set(df.Domain.iloc[te].str.lower()))
    pd.DataFrame({'indice_original':np.arange(len(df)), 'particao':np.where(np.isin(np.arange(len(df)),te),'teste','treino')}).to_csv(OUT/'particoes.csv',index=False)
    rows=[]
    trained={}
    for name,m in models().items():
        rows.append(evaluate(name,m,x.iloc[tr],x.iloc[te],y.iloc[tr],y.iloc[te],'aleatorio_80_20',True))
        trained[name]=m
    tree=trained['Árvore de Decisão']
    meta['arvore']={'profundidade':tree.get_depth(),'folhas':tree.get_n_leaves()}
    (OUT/'regras_arvore.txt').write_text(export_text(tree,feature_names=list(x.columns)),encoding='utf-8')
    pd.Series(tree.feature_importances_,index=x.columns).sort_values(ascending=False).to_csv(OUT/'importancias_arvore.csv')
    for name in ['Regressão Logística','Árvore de Decisão']:
        xx=x.drop(columns=['URLSimilarityIndex'])
        rows.append(evaluate(name,models()[name],xx.iloc[tr],xx.iloc[te],y.iloc[tr],y.iloc[te],'ablacao_sem_similaridade'))
    # Diagnóstico adicional: mesmo domínio literal nunca pertence aos dois lados.
    groups=df.Domain.str.lower().str.rstrip('.')
    gtr,gte=next(GroupShuffleSplit(n_splits=1,test_size=.2,random_state=SEED).split(x,y,groups))
    assert not (set(groups.iloc[gtr]) & set(groups.iloc[gte]))
    meta['grupos']={'treino':len(gtr),'teste':len(gte),'sobreposicao':0,'criterio':'Domain literal em minúsculas; não agrupa eTLD+1'}
    for name in ['Regressão Logística','Árvore de Decisão','Random Forest']:
        rows.append(evaluate(name,models()[name],x.iloc[gtr],x.iloc[gte],y.iloc[gtr],y.iloc[gte],'dominios_separados'))
    xt,xv,yt,yv=train_test_split(x,y,test_size=.2,random_state=SEED,stratify=y)
    meta['dominios_em_ambos_aleatorio']=len(set(groups.loc[xt.index]) & set(groups.loc[xv.index]))
    hashes=pd.util.hash_pandas_object(x,index=False)
    meta['vetores_teste_presentes_treino']=int(hashes.loc[xv.index].isin(set(hashes.loc[xt.index])).sum())
    result=pd.DataFrame(rows); result.to_csv(OUT/'metricas.csv',index=False)
    (OUT/'execucao.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2,default=lambda v:v.item()),encoding='utf-8')
    # Modelo compacto e exemplos de teste reservados para demonstração offline.
    (ROOT/'modelos').mkdir(exist_ok=True)
    joblib.dump({'modelo':tree,'atributos':list(x.columns),'classes':{'0':'phishing','1':'legitimo'}},ROOT/'modelos/arvore.joblib')
    chosen=[]
    for cls in [0,1]: chosen.extend([int(i) for i in te if y.iloc[i]==cls][:5])
    samples=[]
    for idx in chosen:
        samples.append({'id':idx, 'real':int(y.iloc[idx]),'atributos':{k:float(v) for k,v in x.iloc[idx].items()}})
    (OUT/'amostras_demo.json').write_text(json.dumps(samples,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Experimento concluído.',flush=True)
    return result

if __name__=='__main__': run()
