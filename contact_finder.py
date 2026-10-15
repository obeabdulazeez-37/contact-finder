# Contact Finder
# Takes a company domain and a department, searches Hunter.io,
# filters job titles with keyword lists, and prints ranked contacts.

import requests, os
import sys

# ---------------------------- DATA (WILL EDIT IN V2) ---------------------------------

#set keywords_sets that would be used to filter positions for priority contacts

keyword_sets = { 
"hr": 
     {
        "strong": ["recruiter", "recruiting", "recruitment", "talent acquisition", "talent partner", "sourcer", "staffing", "hiring",
                 "campus", "university", "student", "early careers"],
        "weak": ["talent", "human resources", "hr generalist", "hr advisor", "hr manager", "people", "coordinator", "onboarding"],
        "exclude": ["hris", "payroll", "compensation", "benefits", "diversity", "inclusion", "learning", "policy", "labor",
                     "labour"],
     },
"it": 
    {
     "strong": ["security", "cybersecurity", "cyber", "soc", "infosec", "ciso", "information security", "threat",
                    "incident", "vulnerability"],
     "weak": ["it manager", "it director", "analyst", "engineer", "infrastructure", "network", "systems", "technology"],
     "exclude": ["sales", "marketing", "procurement"]
     }                 
}


# Set valid_status_rank to rank email verification.
# Valid is the best, Accept_all cannot be confirmed but follows companys' emaill creation e.g {first_name + last_name}@domain.com,
# Null means never checked. 
valid_status_rank = {"valid" : 1, "accept_all" : 2, "null" : 3}
max_result = 10



# ---------------------------------  INPUT  -----------------------------------------------

domain = input("Enter companys' domain: ").strip().lower()
domain = domain.removeprefix("https://").removeprefix("http://")
domain = domain.removeprefix("www.")
domain = domain.split("/")[0]

if domain == "":
     print("Domain is empty")
     sys.exit()

dept = input("Enter department you would love to filter through: ").strip().lower()

if not dept in keyword_sets:
     print(f"These are the available departments you can pick from: {keyword_sets.keys()}")
     sys.exit()

try:
    with open('API_key.txt', 'r') as f:
     API_key = f.read().strip()
except FileNotFoundError:
    print("Sorry API key not found!")
    sys.exit()

if API_key == "":
     print("Api key is missing.")
     sys.exit()


# -------------------------------------------- REQUEST ------------------------------------- 

contacts = list()

try:
    url = "https://api.hunter.io/v2/domain-search"

    params = {"domain": domain,
              "department": dept,
              "limit": 10,
              "api_key": API_key
             }
    r = requests.get(url, params=params, timeout=10)
    
    if r.status_code >= 400 and r.status_code < 600:
        raise requests.exceptions.HTTPError(f"Bad status: {r.status_code}")
    elif r.status_code == 200:
        print(f"Good status: {r.status_code}")
    
    data = r.json()

    contacts = data["data"]["emails"]

except requests.exceptions.JSONDecodeError:
    print("Invalid JSON!")
except requests.exceptions.HTTPError as e:
    print("Request failed!", e)
except Exception as e:
    print("Unexpected error!", type(e).__name__)

finally:
    print("Search finished!")

if not contacts:
    print("No contacts found!")
    sys.exit()


# ------------------------------------------- FILTER AND SCORE -----------------------------------------------

words = keyword_sets[dept]
matches = list()

for contact in contacts:
    title = (contact['position'] or "").lower()
    
    if title == "":
        continue
    
    if any(word in title for word in words["exclude"]):
        continue

    if any(word in title for word in words["strong"]):
        score = 2
    elif any(word in title for word in words["weak"]):
        score = 1
    else:
        continue

matches.append({"contact": contact, "score": score})

if not matches:
    print("No relevant contacts found!")
    sys.exit()



# ------------------------------------------------ RANK ------------------------------------------------------

def sort_key(m):
    c = m["contact"]
    status = c["verification"]["status"]
    return(
        -m["score"],
        valid_status_rank.get(status, 3),
        -(c["confidence"] or 0),
        )

matches.sort(key=sort_key)


# ------------------------------------------------ OUTPUT ------------------------------------------------------

top = matches[:max_result]

print(f"Showing {len(top)} of {len(matches)} contacts at {domain} ({dept})")

for m in matches:
    c = m["contact"]
    name = {f"{c['first_name']} {c['last_name']}"}
    status = c["verification"]["status"] or "unverified"
    linkedin = c["linkedin"] or "none"
    print(name, c["position"], c["value"], c["confidence"], status, linkedin, sep= " | ")

