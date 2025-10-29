import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

class MedalPredictor:
    """Predict medal winners using ML"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.model = None
        self.encoders = {}
        
    def prepare_data(self):
        """Prepare data for ML"""
        # Encode categorical variables
        categorical_cols = ['Country', 'Sport', 'Gender', 'Discipline']
        
        for col in categorical_cols:
            le = LabelEncoder()
            self.df[f'{col}_encoded'] = le.fit_transform(self.df[col])
            self.encoders[col] = le
        
        # Create binary target (1 if medal won, 0 otherwise)
        self.df['won_medal'] = 1  # All rows in dataset have medals
        
        # Features and target
        feature_cols = [f'{col}_encoded' for col in categorical_cols]
        X = self.df[feature_cols]
        y = self.df['won_medal']
        
        return X, y
    
    def train_model(self, test_size=0.3, model_type='logistic'):
        """Train ML model"""
        X, y = self.prepare_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Choose model
        if model_type == 'logistic':
            self.model = LogisticRegression(max_iter=1000)
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Train
        print(f"Training {model_type} model...")
        self.model.fit(X_train, y_train)
        
        # Predict
        y_pred = self.model.predict(X_test)
        
        # Evaluate
        print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return self.model, X_test, y_test, y_pred
    
    def save_model(self, filepath='src/models/medal_predictor.pkl'):
        """Save trained model"""
        joblib.dump({'model': self.model, 'encoders': self.encoders}, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='src/models/medal_predictor.pkl'):
        """Load trained model"""
        loaded = joblib.load(filepath)
        self.model = loaded['model']
        self.encoders = loaded['encoders']
        print(f"Model loaded from {filepath}")

if __name__ == "__main__":
    df = pd.read_csv('data/processed/olympics_cleaned.csv')
    predictor = MedalPredictor(df)
    predictor.train_model(model_type='random_forest')
    predictor.save_model()