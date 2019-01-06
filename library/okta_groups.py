#!/usr/bin/python
# (c) 2019, Whitney Champion <whitney.ellis.champion@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: okta_groups
short_description: Communicate with the Okta API to manage users
description:
    - The Okta user module manages Okta users
version_added: "1.0"
author: "Whitney Champion (@shortstack)"
options:
  organization:
    description:
      - Okta subdomain for your organization. (i.e.
        mycompany.okta.com).
    required: true
    default: None
  api_key:
    description:
      - Okta API key.
    required: true
    default: None
  action:
    description:
      - Action to take against user API.
    required: false
    default: list
    choices: [ create, update, delete, list ]
  id:
    description:
      - ID of the user.
    required: false
    default: None
  name:
    description:
      - Group name.
    required: false
    default: None
  description:
    description:
      - Group description.
    required: false
    default: yes
  limit:
    description:
      - List limit.
    required: false
    default: 200
"""

EXAMPLES = '''
# List groups
- okta_groups:
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    limit: 200

# Create group
- okta_groups:
    action: create
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    name: "Imaginary Creatures"
    description: "They are so majestic"

# Delete group
- okta_groups:
    action: delete
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
'''

RETURN = r'''
json:
  description: The JSON response from the Okta API
  returned: always
  type: complex
msg:
  description: The HTTP message from the request
  returned: always
  type: str
  sample: OK (unknown bytes)
status:
  description: The HTTP status code from the request
  returned: always
  type: int
  sample: 200
url:
  description: The actual URL used for the request
  returned: always
  type: str
  sample: https://www.ansible.com/
'''

def create(module,base_url,api_key,name,description):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    payload = {}
    profile = {}

    if name is not None:
        profile['name'] = name
    if description is not None:
        profile['description'] = description

    payload['profile'] = profile

    url = base_url+"/?activate=%s" % (activate)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST', data=payload)

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def delete(module,base_url,api_key,id):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='DELETE') # deactivate
    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='DELETE') # delete

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def list(module,base_url,api_key,limit):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/?limit=%s" % (limit)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='GET')

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def main():
    module = AnsibleModule(
        argument_spec = dict(
            organization      = dict(type='str', required=False, default=None),
            api_key       = dict(type='str', required=True, no_log=True),
            action         = dict(type='str', required=False, default='list', choices=['create', 'delete', 'list']),
            id     = dict(type='str', default=None),
            name    = dict(type='str', default=None),
            description    = dict(type='str', default=None),
            limit    = dict(type='int', default=200)
        )
    )

    organization = module.params['organization']
    api_key = module.params['api_key']
    action = module.params['action']
    id = module.params['id']
    name = module.params['name']
    description = module.params['description']
    limit = module.params['limit']

    base_url = "https://%s-admin.okta.com/api/v1/groups" % (organization)

    if action == "create":
        status, message, content, url = create(module,base_url,api_key,name,description)
    elif action == "delete":
        status, message, content, url = delete(module,base_url,api_key,id)
    elif action == "list":
        status, message, content, url = list(module,base_url,api_key,limit)

    uresp = {}
    content = to_text(content, encoding='UTF-8')
    js = json.loads(content)

    uresp['json'] = js
    uresp['status'] = status
    uresp['msg'] = message
    uresp['url'] = url

    module.exit_json(**uresp)

# import module snippets
import json
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
