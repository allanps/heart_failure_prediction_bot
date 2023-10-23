from typing import List, Tuple
from sklearn.model_selection import train_test_split
import pandas as pd
from ngboost import NGBClassifier
import pickle as pkl
import joblib


FEATURE_COLUMNS: List["str"] = ["Age", "Cholesterol"]
TARGET_COLUMN: "str" = "HeartDisease"

def load_data() -> pd.DataFrame:
    return pd.read_csv("./assets/heart.csv")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.dropna()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    features = FEATURE_COLUMNS + [TARGET_COLUMN]
    df = df[features]

    return df

def split_data(df: pd.DataFrame):
    X_train, X_test, y_train, y_test = train_test_split(df[FEATURE_COLUMNS], df[TARGET_COLUMN], test_size=0.33, random_state=1)
    return X_train, X_test, y_train, y_test

def fit_model(X_train: pd.DataFrame, y_train: pd.DataFrame):

    classifier = NGBClassifier()
    classifier.fit(X_train, y_train)
    
    return classifier

def save_model(model: NGBClassifier) -> None:
    with open("ng_boost_model.pkl", "wb") as f:
        pkl.dump(model, f, protocol=pkl.HIGHEST_PROTOCOL)
    joblib.dump(model, "ng_boost_model.joblib", protocol=1, compress=0)


def load_model() -> NGBClassifier:
    model = joblib.load("ng_boost_model.joblib")
    return model
    # with open("ng_boost_model.pkl", "rb") as f:
    #     return pkl.load(f)

def predict(model: NGBClassifier, X_test: pd.DataFrame):
    return model.predict_proba(X_test)



df_raw: pd.DataFrame = load_data()
print(df_raw.head(10))

df_cleaned: pd.DataFrame = clean_data(df_raw)
print(df_cleaned.head(2))

X_train, X_test, y_train, y_test = split_data(df_cleaned)
print(y_train)

classifier = fit_model(X_train, y_train)
try:
    save_model(classifier)
    print("Model saved")
except Exception as e:
    print(f"Error while saving the model: {e}")

try:
    loaded_model = load_model()
    print("Model loaded")
except Exception as e:
    print(f"Error while loading the model: {e}")

predictions = predict(loaded_model, X_test)
predictions[:2]

