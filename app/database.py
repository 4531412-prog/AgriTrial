from datetime import datetime
import sqlite3
from app.models import Observations
import os
from dotenv import load_dotenv
from supabase import create_client
import uuid


load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agritrial.db')


def to_float(value):
    return float(value) if value is not None else None

def create_database():
    # 1. Connect to a database file called "agritrial.db" (this creates it if it doesn't exist)
    con1 = sqlite3.connect(DB_PATH)
    cur1 = con1.cursor()

    cur1.execute('''CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    synced BOOLEAN DEFAULT 0,
    device_id TEXT,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMP,
    supabase_id INTEGER,
    client_record_id TEXT
    )
    ''')

    ##use dropdown for Sites in data caprute form

    cur1.execute('''CREATE TABLE IF NOT EXISTS trials (
    id INTEGER PRIMARY KEY,
    site_id INTEGER, 
    crop TEXT,
    variety TEXT,
    synced BOOLEAN DEFAULT 0,
    device_id TEXT,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMP,
    supabase_id INTEGER,
    client_record_id TEXT,
    FOREIGN KEY (site_id) REFERENCES Sites(id)
    )
    ''')

    cur1.execute('''CREATE TABLE IF NOT EXISTS treatments (
    id INTEGER PRIMARY KEY,
    trial_id INTEGER, 
    name TEXT,
    synced BOOLEAN DEFAULT 0,
    device_id TEXT,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMP,
    supabase_id INTEGER,
    client_record_id TEXT,
    FOREIGN KEY (trial_id) REFERENCES Trials(id)
    )
    ''')


    cur1.execute('''CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY,
    treatment_id INTEGER NOT NULL, 
    year INTEGER NOT NULL, 
    rep INTEGER,
    
    yield               NUMERIC,
    bio_yield           NUMERIC,
    pods_per_plant      NUMERIC,                      
    thousand_seed_wt    NUMERIC,                        
    oil_pct             NUMERIC,                        
    n                   NUMERIC,
    p                   NUMERIC,
    k                   NUMERIC,
    na                  NUMERIC,                     
    ca                  NUMERIC,
    mg                  NUMERIC,
    fe                  NUMERIC,
    mn                  NUMERIC,
    zn                  NUMERIC,
    cu                  NUMERIC,
    chl_a               NUMERIC,
    chl_b               NUMERIC,
    rwc                 NUMERIC,
    ionic_leakage       NUMERIC,                        
    proline             NUMERIC,                                              

    synced BOOLEAN DEFAULT 0,
    device_id TEXT,
    version integer DEFAULT 1, 
    updated_at timestamp,
    supabase_id INTEGER,
    client_record_id TEXT,
    
    FOREIGN KEY (treatment_id) REFERENCES Treatments(id)
    )
    ''')

    cur1.execute('''CREATE TABLE IF NOT EXISTS device_info (
        id INTEGER PRIMARY KEY,
        device_id TEXT NOT NULL
    )
    ''')

    con1.commit()
    con1.close()

def insert_obs(record: Observations):
    con2 = sqlite3.connect(DB_PATH)
    cur2 = con2.cursor()

    cur2.execute('''INSERT INTO observations (
        treatment_id,
        year,
        rep,
        device_id,
        yield,
        bio_yield,
        pods_per_plant,
        thousand_seed_wt,
        oil_pct,
        n,
        p,
        k,
        na,
        ca,
        mg,
        fe,
        mn,
        zn,
        cu,
        chl_a,
        chl_b,
        rwc,
        ionic_leakage,
        proline,
        updated_at,
        synced,
        version
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
        record.treatment_id,
        record.year,
        record.rep,
        record.device_id,
        to_float(record.yield_),
        to_float(record.bio_yield),
        to_float(record.pods_per_plant),
        to_float(record.thousand_seed_wt),
        to_float(record.oil_pct),
        to_float(record.n),
        to_float(record.p),
        to_float(record.k),
        to_float(record.na),
        to_float(record.ca),
        to_float(record.mg),
        to_float(record.fe),
        to_float(record.mn),
        to_float(record.zn),
        to_float(record.cu),
        to_float(record.chl_a),
        to_float(record.chl_b),
        to_float(record.rwc),
        to_float(record.ionic_leakage),
        to_float(record.proline),
        datetime.now(),
        False,
        1
    ))
    con2.commit()
    con2.close()

def update_obs(obs_id: int, record: Observations):
    con3 = sqlite3.connect(DB_PATH)
    cur3 = con3.cursor()

    cur3.execute("SELECT id FROM observations WHERE id = ?", (obs_id,))
    existing = cur3.fetchone()

    if existing is None:
        con3.close()
        return False

    cur3.execute('''UPDATE observations SET
        treatment_id = ?,
        year = ?,
        rep = ?,
        device_id = ?,
        yield = ?,
        bio_yield = ?,
        pods_per_plant = ?,
        thousand_seed_wt = ?,
        oil_pct = ?,
        n = ?,
        p = ?,
        k = ?,
        na = ?,
        ca = ?,
        mg = ?,
        fe = ?,
        mn = ?,
        zn = ?,
        cu = ?,
        chl_a = ?,
        chl_b = ?,
        rwc = ?,
        ionic_leakage = ?,
        proline = ?,
        updated_at = ?,
        synced = ?,
        version = version + 1
        WHERE id = ?''', (
        record.treatment_id,
        record.year,
        record.rep,
        record.device_id,
        to_float(record.yield_),
        to_float(record.bio_yield),
        to_float(record.pods_per_plant),
        to_float(record.thousand_seed_wt),
        to_float(record.oil_pct),
        to_float(record.n),
        to_float(record.p),
        to_float(record.k),
        to_float(record.na),
        to_float(record.ca),
        to_float(record.mg),
        to_float(record.fe),
        to_float(record.mn),
        to_float(record.zn),
        to_float(record.cu),
        to_float(record.chl_a),
        to_float(record.chl_b),
        to_float(record.rwc),
        to_float(record.ionic_leakage),
        to_float(record.proline),
        datetime.now(),
        False,
        obs_id
    ))
    con3.commit()
    con3.close()
    return True

def sync_table(table_name, con, device_id, fk_column=None, parent_table=None):
    cur_sync = con.cursor()
    cur_sync.execute(f"SELECT * FROM {table_name} WHERE synced = ?", (False,))
    rows_sync = cur_sync.fetchall()

    succeeded = 0
    failed = []


    for row_sync in rows_sync:
        row_sync = dict(row_sync)
        local_id = row_sync['id']
        client_record_id = f"{device_id}_{local_id}"

        if fk_column is not None: ##>>
            old_fk_value = row_sync[fk_column]
            cur_sync.execute(f"SELECT supabase_id FROM {parent_table} WHERE id = ? ", (old_fk_value,))
            parent_result = cur_sync.fetchone()
            row_sync[fk_column] = parent_result["supabase_id"]

        del row_sync['id']
        row_sync.pop('supabase_id', None)
        row_sync['client_record_id'] = client_record_id
        row_sync['device_id'] = device_id
        row_sync['synced'] = True


        try:
            response = supabase.table(table_name).upsert(row_sync, on_conflict="client_record_id").execute()
        except Exception as e:
            print(f"unable to sync {table_name}; row {local_id}: {e}")
            failed.append({"id": local_id, "error": str(e)})
            continue

        new_supabase_id = response.data[0]['id']

        cur_sync.execute(f"UPDATE {table_name} SET synced = ?, supabase_id = ? WHERE id = ?", (True, new_supabase_id, local_id))
        succeeded += 1

    con.commit()
    message = {"table": table_name, "synced": succeeded, "failed": failed}

    return message

def sync_all():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    device_id = get_device_id(con)

    sites_result = sync_table("sites", con, device_id)
    trials_result =sync_table("trials", con, device_id, fk_column="site_id", parent_table="sites")
    treatments_result =sync_table("treatments", con, device_id, fk_column="trial_id", parent_table="trials")
    observations_result =sync_table("observations", con, device_id, fk_column="treatment_id", parent_table="treatments")

    results = [sites_result, trials_result, treatments_result, observations_result]

    con.close()
    return results

def get_device_id(con):
    cur_device = con.cursor()
    cur_device.execute("SELECT * FROM device_info")
    row_device = cur_device.fetchone()

    if row_device is not None: #get the already existing device id
        row_device = dict(row_device)
        return row_device['device_id']
    else:# generate new uuid, insert it, commit,return it
        new_device_id = str(uuid.uuid4())

        cur_device.execute("INSERT INTO device_info (device_id) VALUES (?)", (new_device_id,))

        con.commit()

        return new_device_id

def get_observations():
    response = supabase.table("observations").select(
        "yield, bio_yield,pods_per_plant,thousand_seed_wt,oil_pct,n,p,k,na,ca,mg,fe,mn,zn,cu,chl_a,chl_b,rwc,ionic_leakage,proline, year, rep, treatments(name,trials(crop, sites(name)))").execute()

    flat = []
    for row in response.data:
        if row["treatments"] is None:
            continue

        flat.append({
            "treatment": row["treatments"]["name"],
            "site": row["treatments"]["trials"]["sites"]["name"],
            "crop": row["treatments"]["trials"]["crop"],
            "year": row["year"],
            "rep": row["rep"],
            "yield": row["yield"],
            "oil_pct": row["oil_pct"],
        })
    return flat

