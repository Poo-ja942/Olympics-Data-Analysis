import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class OlympicsVisualizer:
    """Create visualizations for Olympics data"""
    
    def __init__(self, df):
        self.df = df
        sns.set_style('whitegrid')
    
    def plot_top_countries(self, top_n=10):
        """Plot top countries by medal count"""
        medals_by_country = self.df.groupby('Country')['Medal'].count().sort_values(ascending=False).head(top_n)
        
        plt.figure(figsize=(12, 6))
        medals_by_country.plot(kind='bar', color='gold')
        plt.title(f"Top {top_n} Countries by Medal Count", fontsize=16)
        plt.xlabel("Country", fontsize=12)
        plt.ylabel("Total Medals", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('reports/top_countries.png', dpi=300)
        plt.show()
    
    def plot_medals_over_years(self):
        """Plot medal trend over years"""
        medals_over_years = self.df.groupby('Year')['Medal'].count()
        
        plt.figure(figsize=(12, 6))
        plt.plot(medals_over_years.index, medals_over_years.values, 
                marker='o', linestyle='-', color='b', linewidth=2)
        plt.title("Total Medals Won Over the Years", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Total Medals", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('reports/medals_over_years.png', dpi=300)
        plt.show()
    
    def plot_gender_distribution(self):
        """Plot gender distribution"""
        gender_dist = self.df['Gender'].value_counts()
        
        plt.figure(figsize=(8, 8))
        colors = ['#ff9999', '#66b3ff']
        plt.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%',
                colors=colors, startangle=90, explode=[0.05, 0])
        plt.title("Gender Distribution in Olympics Events", fontsize=16)
        plt.tight_layout()
        plt.savefig('reports/gender_distribution.png', dpi=300)
        plt.show()
    
    def plot_top_athletes(self, top_n=10):
        """Plot top athletes by medal count"""
        athlete_medals = self.df.groupby('Athlete')['Medal'].count().sort_values(ascending=False).head(top_n)
        
        plt.figure(figsize=(12, 6))
        athlete_medals.plot(kind='barh', color='silver')
        plt.title(f"Top {top_n} Athletes by Medal Count", fontsize=16)
        plt.xlabel("Total Medals", fontsize=12)
        plt.ylabel("Athlete", fontsize=12)
        plt.tight_layout()
        plt.savefig('reports/top_athletes.png', dpi=300)
        plt.show()

if __name__ == "__main__":
    df = pd.read_csv('data/processed/olympics_cleaned.csv')
    viz = OlympicsVisualizer(df)
    viz.plot_top_countries()
    viz.plot_medals_over_years()
    viz.plot_gender_distribution()
    viz.plot_top_athletes()