import pandas as pd
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification,
    TrainingArguments, 
    Trainer,
    DataCollatorWithPadding,
    pipeline
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import numpy as np
from datasets import Dataset
import os

# Configurações
MODEL_NAME = "Adilmar/caramelo-smile-2"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "avaliacoes_kabum_sentimento.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "caramelo-smile-kabum-finetuned")

# Carregar dados
df = pd.read_csv(DATASET_PATH)
print("Distribuição dos sentimentos:")
print(df['sentimento'].value_counts())

# Mapear sentimentos e converter para int
label_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
df['label'] = df['sentimento'].map(label_mapping)
df = df.dropna(subset=['label', 'avaliacao'])
df['avaliacao'] = df['avaliacao'].astype(str)
df['label'] = df['label'].astype(int)

# Dividir dados
train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
print(f"Treino: {len(train_df)}, Validação: {len(eval_df)}")

# Carregar modelo
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Tokenizar - forma mais simples e direta
def tokenize_function(examples):
    return tokenizer(
        examples["avaliacao"], 
        padding="max_length",
        truncation=True, 
        max_length=256
    )

# Criar datasets sem as colunas do pandas
train_dataset = Dataset.from_dict({
    "avaliacao": train_df['avaliacao'].tolist(),
    "label": train_df['label'].tolist()
})

eval_dataset = Dataset.from_dict({
    "avaliacao": eval_df['avaliacao'].tolist(),
    "label": eval_df['label'].tolist()
})

# Tokenizar
train_dataset = train_dataset.map(tokenize_function, batched=True)
eval_dataset = eval_dataset.map(tokenize_function, batched=True)

# Remover colunas originais
train_dataset = train_dataset.remove_columns(['avaliacao'])
eval_dataset = eval_dataset.remove_columns(['avaliacao'])

# Configurar treinamento
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=2e-5,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    remove_unused_columns=True,
)

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    accuracy = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='weighted')
    return {'accuracy': accuracy, 'f1': f1}

# Treinar
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

print("Iniciando fine-tuning...")
trainer.train()

# Salvar modelo
trainer.save_model()
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Modelo salvo em: {OUTPUT_DIR}")

# Avaliar
results = trainer.evaluate()
print(f"Acurácia: {results['eval_accuracy']:.4f}")
print(f"F1-Score: {results['eval_f1']:.4f}")

# Testar
classifier = pipeline("sentiment-analysis", model=OUTPUT_DIR, tokenizer=OUTPUT_DIR)

test_samples = [
    "Produto excelente, chegou rápido e funcionando perfeitamente!",
    "Não gostei, veio com defeito e o suporte foi péssimo.",
    "O produto é ok, mas a entrega atrasou um pouco.",
]

for sample in test_samples:
    result = classifier(sample)[0]
    print(f"Texto: {sample}")
    print(f"Sentimento: {result['label']} (Score: {result['score']:.4f})")
    print("-" * 50)