from typing import Dict, List
from os import listdir, environ
from os.path import join

import requests
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension

workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')

envs: Dict[str, str] = {}
for key in ['from', 'to', 'cloud', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value

with open(join(workspace, envs['from'])) as f:
    md = f.read()

current = requests.get(
    f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/{envs['to']}",
    auth=(envs['user'], envs['token'])
).json()

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

updated = requests.put(
    f"https://{envs['cloud']}.atlassian.net/wiki/rest/api/content/{envs['to']}",
    json=content,
    auth=(envs['user'], envs['token'])
).json()

print(updated)
