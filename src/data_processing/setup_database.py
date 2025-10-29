import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pymysql

class OlympicsQueryEngine:
    """Setup MySQL database for Olympics data"""
    
    def __init__(self, host='localhost', user='root', password='Root', database='olympics_project'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def create_database(self):
        """Create database if it doesn't exist"""
        try:
            # Connect without specifying database
            self.engine = create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}")
            print("✅ Connected to MySQL database successfully!")
        except Exception as e:
            print("❌ Database connection failed:", e)
            
    
    def load_data_from_csv(self, csv_path):
        """Load CSV data into MySQL"""
        try:
            # Read CSV
            print("Reading CSV file...")
            df = pd.read_csv(csv_path, encoding='latin1')
            
            # Clean data
            df = df.drop(['Event_gender', 'Country_Code'], axis=1, errors='ignore')
            df = df.dropna(how='all')
            df['Year'] = df['Year'].astype('int')
            
            # Create SQLAlchemy engine
            engine = create_engine(
                f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}'
            )
            
            # Load to MySQL
            print("Loading data to MySQL...")
            df.to_sql('olympics_medals', engine, if_exists='replace', index=False, chunksize=1000)
            
            print(f"Successfully loaded {len(df)} records to MySQL!")
            print(f"Table: olympics_medals")
            print(f"Database: {self.database}")
            
            return df
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def create_indexes(self):
        """Create indexes for better query performance"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()
            
            # Create indexes
            indexes = [
                "CREATE INDEX idx_country ON olympics_medals(Country)",
                "CREATE INDEX idx_year ON olympics_medals(Year)",
                "CREATE INDEX idx_sport ON olympics_medals(Sport)",
                "CREATE INDEX idx_athlete ON olympics_medals(Athlete)",
                "CREATE INDEX idx_medal ON olympics_medals(Medal)"
            ]
            
            for idx_query in indexes:
                try:
                    cursor.execute(idx_query)
                    print(f"Created index: {idx_query.split()[2]}")
                except:
                    pass  # Index might already exist
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print("Indexes created successfully!")
            
        except mysql.connector.Error as err:
            print(f"Error creating indexes: {err}")

# Usage
if __name__ == "__main__":
    # Configure your MySQL credentials
    setup = OlympicsQueryEngine(
        host='localhost',
        user='root',
        password='Root',  # Change this!
        database='olympics_project'
    )
    
    # Create database
    setup.create_database()
    
    # Load data
    setup.load_data_from_csv('data/raw/Olympic-medals.csv')
    
    # Create indexes
    setup.create_indexes()