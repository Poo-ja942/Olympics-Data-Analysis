import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

class MySQLQueryEngine:
    """Execute SQL queries on Olympics MySQL database"""
    
    def __init__(self, host='localhost', user='root', password='Root', database='Olympics_project'):
        self.engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{database}'
        )
    
    def execute_query(self, query):
        """Execute SQL query and return DataFrame"""
        return pd.read_sql(query, self.engine)
    
    def top_countries(self, limit=10):
        """Get top countries by medal count"""
        query = f"""
        SELECT Country, COUNT(*) as medal_count
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
    
    def country_performance_by_sport(self, country):
        """Get country's performance by sport"""
        query = f"""
        SELECT Sport, 
               COUNT(*) as total_medals,
               SUM(CASE WHEN Medal = 'Gold' THEN 1 ELSE 0 END) as gold_medals
        FROM olympics_medals
        WHERE Country = '{country}'
        GROUP BY Sport
        ORDER BY total_medals DESC
        """
        return self.execute_query(query)

# Usage
if __name__ == "__main__":
    qe = MySQLQueryEngine(
        host='localhost',
        user='root',
        password='Root',
        database='Olympics_project'
    )
    
    print("Top 10 Countries:")
    print(qe.top_countries())
    
    print("\nTop 10 Athletes:")
    print(qe.top_athletes())