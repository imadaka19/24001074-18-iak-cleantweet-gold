import sqlite3
import pandas as pd

def read_db():
    conn = sqlite3.connect('challenge_database.db')
    #read stopword_table
    stopword_table = pd.read_sql_query("""
                    SELECT 
                        *
                    FROM stopword_table
                  """, conn)
    #read abusive_table
    abusive_table = pd.read_sql_query("""
                    SELECT 
                        *
                    FROM abusive_table
                  """, conn)
    #read kamus_alay_table
    kamus_alay_table = pd.read_sql_query("""
                    SELECT 
                        *
                    FROM kamus_alay_table
                  """, conn)
    conn.close()
    return stopword_table, abusive_table, kamus_alay_table
  

def create_db(df):
    conn = sqlite3.connect('challenge_database.db')
    cursor = conn.cursor()
    # data = list(zip(tweet, tweet_cleaned))

    #create tweet_table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweet_table (
        Tweet TEXT,
        HS INTEGER,
        Abusive INTEGER,
        HS_Individual INTEGER,
        HS_Group INTEGER,
        HS_Religion INTEGER,
        HS_Race INTEGER,
        HS_Physical INTEGER,
        HS_Gender INTEGER,
        HS_Other INTEGER,
        HS_Weak INTEGER,
        HS_Moderate INTEGER,
        HS_Strong INTEGER,
        Tweet_Cleaned TEXT
    )
    ''')
    # tweet.to_sql('tweet_table', conn, if_exists='replace', index=False)
    #write tweet_table
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO tweet_table VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row))
    # cursor.executemany('''
    # INSERT INTO tweet_table (Tweet, Tweet_Cleaned) VALUES (?, ?)
    # ''', data)
    
    conn.commit()
    conn.close()

def create_text_db(dict):
    conn = sqlite3.connect('challenge_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweet_table (
        Tweet TEXT,
        HS INTEGER,
        Abusive INTEGER,
        HS_Individual INTEGER,
        HS_Group INTEGER,
        HS_Religion INTEGER,
        HS_Race INTEGER,
        HS_Physical INTEGER,
        HS_Gender INTEGER,
        HS_Other INTEGER,
        HS_Weak INTEGER,
        HS_Moderate INTEGER,
        HS_Strong INTEGER,
        Tweet_Cleaned TEXT
    )
    ''')
    columns = ', '.join(dict.keys())
    placeholders = ', '.join(['?'] * len(dict))
    values = list(dict.values())

    query = f"INSERT INTO tweet_table ({columns}) VALUES ({placeholders})"
    cursor.execute(query, values)
    conn.commit()
    conn.close()