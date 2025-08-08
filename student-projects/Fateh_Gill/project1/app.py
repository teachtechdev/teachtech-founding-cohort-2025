# Memory‑Efficient Glass Classifier in Google Colab
# Full workflow: train, save, load, and predict on glass.csv (Drive mount only)

# 1) Mount Google Drive and verify file path
from google.colab import drive
import os
import pandas as pd

drive.mount('/content/drive', force_remount=True)
CSV_PATH   = '/content/drive/MyDrive/glass.csv'   # adjust if needed
MODEL_PATH = '/content/drive/MyDrive/glass_clf.pkl'
assert os.path.exists(CSV_PATH), f"File not found: {CSV_PATH}"

# 2) Inspect CSV headers to confirm column names
df_header = pd.read_csv(CSV_PATH, nrows=0)
print("CSV columns:", df_header.columns.tolist())

# 3) Import dependencies
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 4) Configuration (update as needed)
CHUNKSIZE    = 500                     # rows per batch
LABEL_COL    = 'Type'                  # name of the target column in your CSV
FEATURE_COLS = [c for c in df_header.columns if c != LABEL_COL]
print("Feature columns:", FEATURE_COLS)

# 4b) Mapping from numeric class to human‑readable glass type
TYPE_MAPPING = {
    1: "building_windows_float_processed",
    2: "building_windows_non_float_processed",
    3: "vehicle_windows_float_processed",
    4: "vehicle_windows_non_float_processed",  # none in this dataset, but included
    5: "containers",
    6: "tableware",
    7: "headlamps"
}

# 5) Training function (incremental)
def train_and_save(csv_path, model_path):
    # verify specified columns exist in CSV
    cols = pd.read_csv(csv_path, nrows=0).columns.tolist()
    if LABEL_COL not in cols or any(f not in cols for f in FEATURE_COLS):
        raise KeyError(f"Required columns not found. Available: {cols}")

    encoder    = LabelEncoder()
    classifier = SGDClassifier(
        loss='log_loss',      # logistic regression
        max_iter=1,
        tol=None,
        learning_rate='optimal',
        random_state=42
    )

    first_pass = True
    classes    = None

    # incremental training over chunks
    for chunk in pd.read_csv(csv_path, chunksize=CHUNKSIZE):
        X = chunk[FEATURE_COLS].values.astype(float)
        y_raw = chunk[LABEL_COL].values

        if first_pass:
            encoder.fit(y_raw)
            classes = encoder.transform(encoder.classes_)
            first_pass = False

        y = encoder.transform(y_raw)
        if not hasattr(classifier, 'classes_'):
            classifier.partial_fit(X, y, classes=classes)
        else:
            classifier.partial_fit(X, y)

    # save the model + encoder
    joblib.dump({'model': classifier, 'encoder': encoder}, model_path)
    print(f"Training complete. Model saved to: {model_path}")

# 6) Prediction helper (returns the numeric class)
def load_and_predict(attr_text, model_path):
    data = joblib.load(model_path)
    model   = data['model']
    encoder = data['encoder']

    values = [float(x) for x in attr_text.strip().split(',')]
    X_new  = np.array(values).reshape(1, -1)
    y_pred = model.predict(X_new)
    return encoder.inverse_transform(y_pred)[0]

# 7) Execute training and example prediction + pretty‑print
if __name__ == '__main__':
    train_and_save(CSV_PATH, MODEL_PATH)

    # --- your sample attributes: one value per FEATURE_COLS, in the same order ---
    sample_attrs = "1.52101,13.64,4.49,1.10,71.78,0.06,8.75,0.00,0.00"
    values = [float(x) for x in sample_attrs.split(',')]

    # print attribute names & values
    print("\nSample attributes:")
    for name, val in zip(FEATURE_COLS, values):
        print(f"  {name}: {val}")

    # get numeric prediction
    pred_num = load_and_predict(sample_attrs, MODEL_PATH)
    print(f"\nPredicted glass type (numeric): {pred_num}")

    # map to human‑readable description
    desc = TYPE_MAPPING.get(int(pred_num), "Unknown type")
    print(f"Predicted glass type (description): {desc}")
