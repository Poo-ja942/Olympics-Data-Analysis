import pandas as pd
import numpy as np

class OlympicsDataCleaner:
    """Clean and prepare Olympics data"""
    filepath = 'data\raw\Olympic-medals.csv'
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath, encoding='latin1')
        
    def clean(self):
        """Main cleaning pipeline"""
        print("Starting data cleaning...")
        
        # Drop unnecessary columns
        self.df = self.df.drop(['Event_gender', 'Country_Code'], axis=1, errors='ignore')
        
        # Handle missing values
        print(f"Missing values before: {self.df.isnull().sum().sum()}")
        self.df = self.df.dropna(how='all')
        print(f"Missing values after: {self.df.isnull().sum().sum()}")
        
        # Fix data types
        self.df = self.df.astype({'Year': 'int'})
        
        print("Data cleaning completed!")
        return self.df
    
    def save_cleaned_data(self, output_path):
        """Save cleaned data"""
        self.df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    cleaner = OlympicsDataCleaner('data/raw/Olympic-medals.csv')
    cleaned_df = cleaner.clean()
    cleaner.save_cleaned_data('data/processed/olympics_cleaned.csv')