import os
import json
from github import Github
from collections import Counter
from datetime import date

"""
# Secrets
with open(os.path.join(os.getcwd(),'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    return secrets[setting]

g = Github(get_secret('ACCESS_TOKEN'))
"""

g = Github(os.environ['ACCESS_TOKEN'])

lang_dict = dict()
today_langs = dict()
total_langs = {}

for repo in g.get_user().get_repos():
    
    # Filter only personal repos
    if repo.owner.login != 'Microntel' and repo.fork == False:
        lang_dict = repo.get_languages()
        today_langs = dict(Counter(lang_dict)+Counter(today_langs))

# Mark with current date
today = date.today()
total_langs = {today: today_langs}

# output
print(total_langs)

# Write record on SQLite database

