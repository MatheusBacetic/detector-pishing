"""Demonstração offline do classificador treinado, usando amostras de teste.
Integrantes: Alexandre Eiji Tomimura Carvalho (10371680), João Pedro Pioltini
de Oliveira (10425643), Matheus Veiga Bacetic Joaquim (10425638).
Histórico: 2026-11-18 | assistência Codex, para revisão do grupo | demonstração.
"""
from pathlib import Path
import argparse
import json
import joblib
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def predict(attributes, bundle):
    expected=bundle['atributos']
    if set(attributes)!=set(expected):
        raise ValueError(f'Forneça exatamente os {len(expected)} atributos do modelo.')
    frame=pd.DataFrame([{k:attributes[k] for k in expected}])
    if frame.isna().any().any(): raise ValueError('Atributos ausentes')
    return int(bundle['modelo'].predict(frame)[0])

def main():
    parser=argparse.ArgumentParser(description='Classificação offline de atributos PhiUSIIL; não consulta URLs.')
    parser.add_argument('--json',type=Path,help='Objeto JSON com os atributos numéricos, sem o rótulo.')
    args=parser.parse_args()
    bundle=joblib.load(ROOT/'modelos/arvore.joblib')
    if args.json:
        pred=predict(json.loads(args.json.read_text(encoding='utf-8')),bundle)
        print('Previsão:', 'PHISHING' if pred==0 else 'LEGÍTIMO')
    else:
        samples=json.loads((ROOT/'resultados/final/amostras_demo.json').read_text(encoding='utf-8'))
        print('DEMONSTRAÇÃO OFFLINE - amostras reservadas do teste\n')
        print('O rótulo real é usado somente para comparar, nunca como entrada.\n')
        for sample in samples:
            pred=predict(sample['atributos'],bundle)
            print(f"Registro {sample['id']:6d} | previsto: {'PHISHING' if pred==0 else 'LEGÍTIMO':8s} | real: {'PHISHING' if sample['real']==0 else 'LEGÍTIMO'}")
        print('\nEscopo: atributos já extraídos. Não é um verificador de links em tempo real.')

if __name__=='__main__': main()
