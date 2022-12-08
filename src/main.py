from os import environ
from os.path import join
from typing import Dict

import requests
from dotenv import load_dotenv
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

load_dotenv()

workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    print('No workspace is set')
    exit(1)

envs: Dict[str, str] = {}
for key in ['from', 'to', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        print(f'Missing value for {key}')
        exit(1)
    envs[key] = value

with open(join(workspace, envs['from'])) as f:
    md = f.read()

url = f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/{envs['to']}"

current = requests.get(url, auth=(envs['user'], envs['token'])).json()

html = markdown(md, extensions=[GithubFlavoredMarkdownExtension()])
content = {
    'id': current['id'],
    'type': current['type'],
    'title': current['title'],
    'version': {'number': current['version']['number'] + 1},
    'body': {
        'editor': {
            'value': html,
            'representation': 'editor'
        }
    }
}

updated = requests.put(url, json=content, auth=(
    envs['user'], envs['token'])).json()
link = updated['_links']['base'] + updated['_links']['webui']
print(f'Uploaded content successfully to page {link}')
