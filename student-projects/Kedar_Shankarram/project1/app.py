import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

# Google Drive file paths
CLEAN_CSV_PATH    = '/content/drive/MyDrive/Clean_Dataset.csv'
BUSINESS_CSV_PATH = '/content/drive/MyDrive/business.csv'
ECONOMY_CSV_PATH  = '/content/drive/MyDrive/economy.csv'

# Load datasets
clean_df = pd.read_csv(CLEAN_CSV_PATH)
business_df = pd.read_csv(BUSINESS_CSV_PATH)
economy_df = pd.read_csv(ECONOMY_CSV_PATH)

# === Create prior booking preference probabilities by airline ===
business_counts = business_df['airline'].value_counts().rename("business_count")
economy_counts = economy_df['airline'].value_counts().rename("economy_count")

prior_df = pd.concat([business_counts, economy_counts], axis=1).fillna(0)
prior_df['total'] = prior_df['business_count'] + prior_df['economy_count']
prior_df['business_prior'] = prior_df['business_count'] / prior_df['total']
prior_df['economy_prior'] = prior_df['economy_count'] / prior_df['total']
prior_df = prior_df[['business_prior', 'economy_prior']]
prior_df.index.name = 'airline'
prior_df.reset_index(inplace=True)

# === Merge prior probabilities into the clean dataset ===
df = clean_df.merge(prior_df, on='airline', how='left')

# === Clean up common word-number values if present ===
text_to_number = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5
}

if 'stops' in df.columns and df['stops'].dtype == object:
    df['stops'] = df['stops'].replace(text_to_number)

#  Encode categorical features
label_encoders = {}
categorical_cols = df.select_dtypes(include='object').columns.drop('class', errors='ignore')

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

#  Encode target variable
df['class'] = df['class'].map({'Economy': 0, 'Business': 1})

#  Drop any remaining rows with missing values
df.dropna(inplace=True)

# Split into train and test
X = df.drop(columns=['class'])
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Train the Logistic Regression model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

#  evaluate model
y_pred = clf.predict(X_test)
print("  Accuracy:", accuracy_score(y_test, y_pred))
print("\n Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred))

#  visualize confuson matrix
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Logistic Regression: Business vs Economy")
plt.show()

# predict the class of a sample flight
example = X_test.iloc[0]
example_df = pd.DataFrame([example])
predicted_class = clf.predict(example_df)[0]
predicted_label = "Business" if predicted_class == 1 else "Economy"

print("\n Example Flight Prediction")
print("--------------------------------")
print("Airline:", label_encoders['airline'].inverse_transform([int(example['airline'])])[0])
print("From:", label_encoders['source_city'].inverse_transform([int(example['source_city'])])[0])
print("To:", label_encoders['destination_city'].inverse_transform([int(example['destination_city'])])[0])
print("Stops:", int(example['stops']) if 'stops' in example else "N/A")
print("Price: ₹", int(example['price']))
print("Predicted Class:", predicted_label)
