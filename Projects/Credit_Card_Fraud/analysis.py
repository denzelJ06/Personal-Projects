import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, average_precision_score

df = pd.read_csv("data/cleaned_fraudTest.csv")

#print(df.nunique())
#print(df.info())    #showed an issue of the collumns for date and time and cc_num
                     #being read as the wrong data type

df["trans_Date_&_Time"] = pd.to_datetime(df["trans_Date_&_Time"],format="%Y-%m-%d %H:%M:%S")
df["cc_num"] = (df["cc_num"]).astype(str)
#print(d_time)

fraud_cases = np.count_nonzero(df["is_fraud"])
#print(fraud_cases)  2145 fraud cases

#checking for relationships between fraud cases
for col in df:
    if pd.api.types.is_numeric_dtype(df[col]):
        print("relationship between is_fraud and ",col)
        print(df.groupby('is_fraud')[col].describe())
    else:
        pass

#heatmap

#realised that a stratified sample needed to be taken as the 
#correlations were all below 0.2 which signifies no correlation
#This was due to the low number of fraud cases compared to total

fraud_cases = df[df['is_fraud'] == 1]
non_fraud_cases = df[df['is_fraud'] == 0]
seed = 7
non_fraud_sample = non_fraud_cases.sample(n=len(fraud_cases), random_state=seed)

# 3. Concatenate and shuffle the balanced dataset
balanced_df = pd.concat([fraud_cases, non_fraud_sample]).sample(frac=1, random_state=seed).reset_index(drop=True)

# Verify class balance
print(balanced_df['is_fraud'].value_counts())

#heatmap_cols = ["is_fraud","amt","city_pop","day_of_week","age","distance_km","hour"]
#corr = balanced_df[heatmap_cols].corr()
#sns.heatmap(corr,cmap="coolwarm",annot=True,linewidths=0.5)
#plt.tight_layout()
#plt.savefig("Projects/Credit_Card_Fraud/correlation_heatmap.png", bbox_inches="tight")

#bar chart for category
#df.groupby('category')['is_fraud'].mean().sort_values(ascending=False).plot(kind='bar')
#plt.tight_layout()
#plt.savefig("Projects/Credit_Card_Fraud/correlation_bar_chart.png", bbox_inches="tight")

# ---------------------------------------------------------
# 2. Feature Selection & One-Hot Encoding
# ---------------------------------------------------------
feature_cols = ['amt', 'category', 'city_pop', 'age', 'distance_km', 'hour', 'day_of_week']
X = balanced_df[feature_cols]
y = balanced_df['is_fraud']

# One-hot encode the categorical 'category' feature
X = pd.get_dummies(X, columns=['category'], drop_first=True)

# ---------------------------------------------------------
# 3. Train-Test Split (80% Train, 20% Test)
# ---------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, 
    y, 
    test_size=0.20, 
    random_state=42, 
    stratify=y
)

print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}\n")

# ---------------------------------------------------------
# 4. Train the Model
# ---------------------------------------------------------
rf_model = RandomForestClassifier(
    n_estimators=100, 
    max_depth=12, 
    random_state=42, 
    n_jobs=-1
)

print("Training Random Forest on balanced data...")
rf_model.fit(X_train, y_train)
print("Training complete!\n")

# ---------------------------------------------------------
# 5. Evaluate Performance
# ---------------------------------------------------------
y_pred = rf_model.predict(X_test)
y_probs = rf_model.predict_proba(X_test)[:, 1]

print("=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, digits=4))

print("=== Evaluation Scores ===")
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_probs):.4f}")
print(f"PR-AUC Score:  {average_precision_score(y_test, y_probs):.4f}")