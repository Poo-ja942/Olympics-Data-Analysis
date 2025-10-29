import pandas as pd
from sqlalchemy import create_engine

class OlympicsQueryEngine:
    """Execute SQL queries on Olympics MySQL database"""
    
    def __init__(self, host='localhost', user='root', password='Root', database='olympics_project'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        
        # Create SQLAlchemy engine
        self.engine = create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
        )
        print(f"✓ Connected to MySQL: {database}")
    
    def execute_query(self, query):
        """Execute SQL query and return DataFrame"""
        return pd.read_sql(query, self.engine)
    
    def get_all_data(self):
        """Get all data from database"""
        query = "SELECT * FROM olympics_medals"
        return self.execute_query(query)
    
    def top_countries(self, limit=10):
        """Get top countries by medal count"""
        query = f"""
        SELECT Country, 
               COUNT(*) as medal_count,
               SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END) as gold,
               SUM(CASE WHEN Medal = 'Silver' THEN 1 ELSE 0 END) as silver,
               SUM(CASE WHEN Medal = 'Bronze' THEN 1 ELSE 0 END) as bronze
        FROM olympics_medals
        GROUP BY Country
        ORDER BY medal_count DESC
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def medals_by_year(self):
        """Get medals distribution by year"""
        query = """
        SELECT Year, 
               COUNT(*) as total_medals,
               SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END) as gold,
               SUM(CASE WHEN Medal = 'Silver' THEN 1 ELSE 0 END) as silver,
               SUM(CASE WHEN Medal = 'Bronze' THEN 1 ELSE 0 END) as bronze
        FROM olympics_medals
        GROUP BY Year
        ORDER BY Year
        """
        return self.execute_query(query)
    
    def top_athletes(self, limit=10):
        """Get top athletes by medal count"""
        query = f"""
        SELECT Athlete, Country, COUNT(*) as medal_count
        FROM olympics_medals
        GROUP BY Athlete, Country
        ORDER BY medal_count DESC
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def country_by_sport(self, country):
        """Get country's medals by sport"""
        query = f"""
        SELECT Sport, 
               COUNT(*) as total_medals,
               SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END) as gold,
               SUM(CASE WHEN Medal = 'Silver' THEN 1 ELSE 0 END) as silver,
               SUM(CASE WHEN Medal = 'Bronze' THEN 1 ELSE 0 END) as bronze
        FROM olympics_medals
        WHERE Country = '{country}'
        GROUP BY Sport
        ORDER BY total_medals DESC
        """
        return self.execute_query(query)
    
    def gender_distribution(self):
        """Get gender distribution"""
        query = """
        SELECT Gender, 
               COUNT(*) as count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM olympics_medals WHERE Gender IS NOT NULL), 2) as percentage
        FROM olympics_medals
        WHERE Gender IS NOT NULL
        GROUP BY Gender
        """
        return self.execute_query(query)
    
    def sport_analysis(self):
        """Get sport statistics"""
        query = """
        SELECT Sport,
               COUNT(*) as total_medals,
               COUNT(DISTINCT Event) as unique_events,
               COUNT(DISTINCT Country) as countries_participated
        FROM olympics_medals
        GROUP BY Sport
        ORDER BY total_medals DESC
        """
        return self.execute_query(query)

if __name__ == "__main__":
    # Test queries
    qe = OlympicsQueryEngine()
    
    print("\n" + "="*60)
    print("OLYMPICS DATA - SQL QUERY RESULTS")
    print("="*60)
    
    print("\n📊 Top 10 Countries:")
    print(qe.top_countries())
    
    print("\n🏅 Top 10 Athletes:")
    print(qe.top_athletes())
    
    print("\n👥 Gender Distribution:")
    print(qe.gender_distribution())
    
    print("\n📈 Medals by Year (first 5):")
    print(qe.medals_by_year().head())