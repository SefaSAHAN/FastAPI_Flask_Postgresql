import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres')
cur = conn.cursor()
cur.execute("COMMIT")
cur.execute("CREATE DATABASE flask")
conn.commit()
cur.close()
conn.close()

conn = psycopg2.connect(dbname='flask', user='postgres', password='postgres')
cur = conn.cursor()
cur.execute("CREATE TABLE inputs (id SERIAL PRIMARY KEY, input TEXT, created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW())")
conn.commit()
cur.close()
conn.close()