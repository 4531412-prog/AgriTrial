from datetime import datetime
import sqlite3

def create_database():
    # 1. Connect to a database file called "agritrial.db" (this creates it if it doesn't exist)
    con = sqlite3.connect('agritrial.db')
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Sites (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL
    )
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Trials (
    id INTEGER PRIMARY KEY,
    site_id INTEGER, 
    crop TEXT,
    variety TEXT,
    FOREIGN KEY (site_id) REFERENCES Sites(id)
    )
    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Treatments (
    id INTEGER PRIMARY KEY,
    trial_id INTEGER, 
    name TEXT,
    FOREIGN KEY (trial_id) REFERENCES Trials(id)
    )
    ''')


    cur.execute('''CREATE TABLE IF NOT EXISTS Observations (
    id INTEGER PRIMARY KEY,
    treatment_id INTEGER, 
    plot_number INTEGER, 
    rep INTEGER,
    plant_height_cm REAL,
    synced BOOLEAN,
    yield_kg_per_plot REAL,
    spad REAL,
    disease_pct REAL,
    root_mass_g REAL, 
    device_id text,
    version integer, 
    updated_at timestamp,
    FOREIGN KEY (treatment_id) REFERENCES Treatments(id)
    )
    ''')

    con.commit()
    con.close()



def insert_obs(record: Observations):
    con = sqlite3.connect('agritrial.db')
    cur = con.cursor()

    cur.execute('''INSERT INTO Observations (
    treatment_id,
    plot_number,
    rep, device_id, 
    plant_height_cm, 
    yield_kg_per_plot, 
    spad, 
    disease_pct, 
    root_mass_g,
    updated_at,
    synced,
    version)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (record.treatment_id,record.plot_number, record.rep, record.device_id, record.plant_height_cm, record.yield_kg_per_plot, record.spad, record.disease_pct, record.root_mass_g, datetime.now(), False, 1))



    con.commit()
    con.close()
