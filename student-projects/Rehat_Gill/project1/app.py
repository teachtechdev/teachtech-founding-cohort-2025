from google.colab import drive
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

drive.mount('/content/drive', force_remount=True)
CSV_PATH = '/content/drive/MyDrive/weather_classification_data.csv'
MODEL_PATH = '/content/drive/MyDrive/weather_text_classifier.pkl'
LE_PATH = MODEL_PATH.replace('.pkl','_label_encoder.pkl')

df = pd.read_csv(CSV_PATH)
orig_cols = df.columns.tolist()
if len(orig_cols)<2:
  raise ValueError(f"Expected ≥2 columns in CSV but got {orig_cols}")

df = df.rename(columns={orig_cols[0]: 'text', orig_cols[1]: 'weather'})
df = df.dropna(subset=['text', 'weather'])
df['text'] = df['text'].astype(str)

le = LabelEncoder()
df['weather_label'] = le.fit_transform(df['weather'])
joblib.dump(le, LE_PATH)

X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['weather_label'],
    stratify=df['weather_label'],
    test_size=0.2,
    random_state=42
)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        lowercase=True,
        stop_words='english',
        max_df=0.8,
        min_df=5
    )),
    ('clf'  , LogisticRegression(max_iter=1000, random_state=42))
])


pipeline.fit(X_train, y_train)

acc = pipeline.score(X_test, y_test)
print(f'Validation accuracy: {acc:.3f}')

joblib.dump(pipeline, MODEL_PATH)
print('Saved model to:', MODEL_PATH)
print('Saved label encoder to:', LE_PATH)

print("\nLabel → Weather category mapping:")
for idx, category in enumerate(le.classes_):
    print(f"  {idx} → {category}")

sample_text = "Looks like it's going to pour all afternoon with heavy clouds."
pred_label   = pipeline.predict([sample_text])[0]

pred_weather = le.inverse_transform([pred_label])[0]

print('\nUser sample text:')
print(f'  "{sample_text}"')

print(f'Predicted weather category: {pred_weather}')
