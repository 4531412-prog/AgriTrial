import csv
import os
import sqlite3

from app.models import Observations
from app.database import insert_obs

from decimal import Decimal, InvalidOperation

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'agritrial.db') #absolute path instead of relative
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'AgriTrial+Data+Canola.csv')

print("CSV_PATH:", CSV_PATH)
print("Exists:", os.path.exists(CSV_PATH))

def safe_decimal(value):
    cleaned = value.strip().replace(' ', '')  # strips stray internal/trailing spaces
    if cleaned != value.strip():
        print(f"Warning: cleaned malformed value '{value}' -> '{cleaned}'")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None
def get_treatment_map(con):
    cur = con.cursor()
    cur.execute("SELECT id, name FROM treatments")
    return {row['name']: row['id'] for row in cur.fetchall()}
def clean_number(value):
    value = value.strip().replace(' ', '')
    return float(value) if value else None
def import_canola():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    treatment_map = get_treatment_map(con)
    con.close()

    inserted = 0
    skipped = 0

    with open(CSV_PATH, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            treatment_id = treatment_map.get(row['Block'])
            if treatment_id is None:
                print(f"Skipping record. Unknown Block={row['Block']}, Year={row['Year']}, Rep={row['Replicates']}")
                skipped += 1
                continue

            record = Observations(
                treatment_id=treatment_id,
                year=int(row['Year']),
                rep=int(row['Replicates']),
                device_id="import-script",
                yield_=safe_decimal(row['Yield']),
                bio_yield=safe_decimal(row['Bio Yield']),
                pods_per_plant=safe_decimal(row['pod/plant']),
                thousand_seed_wt=safe_decimal(row['1000sw']),
                oil_pct=safe_decimal(row['Oil%']),
                n=safe_decimal(row['N']),
                p=safe_decimal(row['P']),
                k=safe_decimal(row['K']),
                na=safe_decimal(row['Na']),
                ca=safe_decimal(row['Ca']),
                mg=safe_decimal(row['Mg']),
                fe=safe_decimal(row['Fe']),
                mn=safe_decimal(row['Mn']),
                zn=safe_decimal(row['Zn']),
                cu=safe_decimal(row['Cu']),
                chl_a=safe_decimal(row['Chl a']),
                chl_b=safe_decimal(row['Chl b']),
                rwc=safe_decimal(row['RWC']),
                ionic_leakage=safe_decimal(row['Ionic L']),
                proline=safe_decimal(row['Prolin']),
            )
            insert_obs(record)
            inserted += 1


if __name__ == "__main__":
    import_canola()