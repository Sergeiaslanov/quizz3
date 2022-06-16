import requests
import json
import sqlite3
conn = sqlite3.connect("ip_address_data.sqlite")
cursor = conn.cursor()

# 1

token = 'd9e18e625f5d4f'
ipaddress = str(input("Enter your ip address: "))
url = f'https://ipinfo.io/{ipaddress}?token={token}'
r = requests.get(url)
# print(r)
# print(r.status_code)
# print(r.headers)
# print(r.headers['content-type'])

# print(r.text)
result = json.loads(r.text)                       # dict
# print(result)
res_structured = json.dumps(result, indent=4)      # structured dict
print(res_structured)
# print(result["ip"])

# 2 Save info into the file

with open('ip_data.json', 'w') as file:
    json.dump(result, file, indent=4)

# 3 Read info from file

with open("ip_data.json", "r") as file:
    res = json.load(file)
    print(f'The postal code for {res["ip"]} ip address is --> {res["postal"]}')

# Save info in the database

cursor.execute('''CREATE TABLE IF NOT EXISTS IP_data
                (ID INTEGER PRIMARY key AUTOINCREMENT,
                IP VARCHAR(50),
                City VARCHAR(100),
                Region VARCHAR(50),
                Country VARCHAR(50),
                Loc VARCHAR(50),
                Org VARCHAR(50),
                Postal code VARCHAR(50),
                Timezone VARCHAR(50)
                )
                ''')                    # Create a table with the following attributes : ID, IP, city, region, country,
# loc, org, postal, time zone

try:
    list = []
    list.append((res["ip"], res["city"], res["region"], res["country"], res["loc"], res["org"], res["postal"],
                 res["timezone"]))

    cursor.executemany("INSERT into IP_data (IP, City, Region, Country, Loc, Org, Postal, Timezone)"
                       " VALUES (?, ?, ?, ?, ?, ?, ?, ?)", list)
    conn.commit()
except KeyError:
    print("Info did not add in database because it has not all parameters.")


# 68.87.41.40
# 1.1.1.1
# 2.2.2.2
# 68.88.41.41
# 68.88.41.42
