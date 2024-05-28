from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import json
from datasets import Dataset
import pandas as pd

# Ruta al archivo JSON
json_file_path = 'corpus_deporte.json'

# Cargar datos desde el archivo JSON
with open(json_file_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Convertir el corpus a un DataFrame y luego a un Dataset de Hugging Face
df = pd.DataFrame(corpus["json_input"])
dataset = Dataset.from_pandas(df)

# Dividir el conjunto de datos en entrenamiento y evaluación
train_test_split = dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']

# Tokenizador y modelo
tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')

# Especificar el número de etiquetas
num_labels = 36  # Asegúrate de que esto corresponde al número de etiquetas en tu dataset

model = BertForSequenceClassification.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased', num_labels=num_labels)

# Función de tokenización
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=512)

train_dataset = train_dataset.map(tokenize_function, batched=True)
eval_dataset = eval_dataset.map(tokenize_function, batched=True)

# Remover columnas innecesarias
train_dataset = train_dataset.remove_columns(['text'])
eval_dataset = eval_dataset.remove_columns(['text'])
train_dataset.set_format('torch')
eval_dataset.set_format('torch')

# Argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Entrenador
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

# Entrenar el modelo
trainer.train()

# Guardar el modelo entrenado
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")