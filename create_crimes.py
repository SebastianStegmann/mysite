import sqlite3 as sql
from faker import Faker
import random
fake = Faker("da")
from faker.providers import profile
fake.add_provider(profile)


con = sql.connect("crimes.db")
crime_categories = [
    "Homicide", "Assault", "Robbery", "Kidnapping", "Domestic Violence",
    "Burglary", "Theft", "Auto Theft", "Arson", "Vandalism",
    "Fraud", "Embezzlement", "Money Laundering", "Identity Theft", "Counterfeiting",
    "Drug Possession", "Drug Distribution/Trafficking", "Drug Manufacturing", "Prescription Drug Fraud",
    "Hacking", "Phishing", "Cyberbullying", "Online Scams",
    "Insider Trading", "Bribery", "Tax Evasion", "Corporate Fraud",
    "Rape", "Sexual Assault", "Sexual Harassment", 
    "Truancy", "Curfew Violations", 
    "DUI/DWI", "Reckless Driving", "Hit and Run", "Driving Without a License", "Speeding"
]
gender_list = ["male","female"]
cursor = con.cursor()

# cursor.execute("DROP TABLE IF EXISTS criminals")
cursor.execute('''CREATE TABLE IF NOT EXISTS criminals (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        gender TEXT,
                        category TEXT,
                        degree INTEGER,
                        address TEXT,
                        name TEXT,
                        cpr TEXT,
                        created_at INTEGER DEFAULT (strftime('%s', 'now'))
                        )''')
for _ in range(9):
    # generate gender and non-gender-specific things
    gender = random.choice(gender_list)
    category = random.choice(crime_categories)
    degree = random.randint(1,5)
    address = fake.address().replace('\n', ' ')
    first_three = random.randint(100,999)
    # generate gender specific things
    if gender == "male":
        name = fake.first_name_male() + " " + fake.last_name()
        last_digit = random.choice([1,3,5,7,9])
    else: 
        name = fake.first_name_female() + " " + fake.last_name()
        last_digit = random.choice([0,2,4,6,8])
        
    birthdate = fake.profile("birthdate")
    birthdate_formatted = birthdate['birthdate'].strftime('%d%m%y')
    cpr = str(str(birthdate_formatted) + str(first_three) + str(last_digit))
    print(gender, category, degree, address, name, "cpr:", cpr)
    
    # Create a table
    #insert user
    cursor.execute("INSERT INTO criminals (gender, category, degree, address, name, cpr) VALUES (?, ?, ?, ?, ?, ?)",
                   (gender, category, degree, address, name, cpr))


cursor.execute("SELECT * FROM criminals")
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)
con.commit()
con.close()
