#!/usr/bin/python
# (c) 2019, Whitney Champion <whitney.ellis.champion@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: okta_users
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
  login:
    description:
      - Username.
    required: false
    default: None
  activate:
    description:
      - Whether or not the new user is activate.
    required: false
    default: yes
  password:
    description:
      - Password.
    required: false
    default: None
  first_name:
    description:
      - First name.
    required: false
    default: None
  last_name:
    description:
      - Last name.
    required: false
    default: None
  email:
    description:
      - Email.
    required: false
    default: None
  group_ids:
    description:
      - List of Group IDs to add the user to.
    required: false
    default: None
  limit:
    description:
      - List limit.
    required: false
    default: 25
"""

EXAMPLES = '''
# List users
- okta_users:
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    limit: 25

# Create user
- okta_users:
    action: create
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    login: "whitney@unicorns.lol"
    first_name: "Whitney"
    last_name: "Champion"
    email: "whitney@unicorns.lol"
    password: "cookiesaredelicious"
    activate: yes

# Create user in group(s)
- okta_users:
    action: create
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    login: "whitney@unicorns.lol"
    first_name: "Whitney"
    last_name: "Champion"
    email: "whitney@unicorns.lol"
    password: "cookiesaredelicious"
    group_ids:
      - "00f5b3gqiLpE114tV2M7"
    activate: yes

# Create multiple users in group
- okta_users:
    action: create
    organization: "crypto"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    login: "{{ item.login }}"
    first_name: "{{ item.first_name }}"
    last_name: "{{ item.last_name }}"
    email: "{{ item.email }}"
    password: "{{ item.password }}"
    group_ids:
      - "00f5b3gqiLpE324tV2M7"
    activate: "{{ item.activate }}"
  with_items:
    - { login: "alice@aol.com", first_name: "Alice", last_name: "A", email: "alice@aolcom", password: "ilovebob111", activate: yes }
    - { login: "bob@aol.com", first_name: "Bob", last_name: "B", email: "bob@aolcom", password: "ilovealice111", activate: yes }

# Update user's email address
- okta_users:
    action: update
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    email: "whitney@ihateunicorns.lol"

# Activate user
- okta_users:
    action: activate
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"

# Deactivate user
- okta_users:
    action: deactivate
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"

# Delete user
- okta_users:
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

def create(module,base_url,api_key,login,password_input,email,first_name,last_name,group_ids,activate):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    payload = {}
    profile = {}
    credentials = {}
    password = {}
    groupIds= []

    if first_name is not None:
        profile['firstName'] = first_name
    if last_name is not None:
        profile['lastName'] = last_name
    if email is not None:
        profile['email'] = email
    if login is not None:
        profile['login'] = login
    if password_input is not None:
        password['value'] = password_input
    if group_ids is not None:
        groupIds = group_ids

    credentials['password'] = password
    payload['credentials'] = credentials
    payload['groupIds'] = groupIds
    payload['profile'] = profile

    url = base_url+"?activate=%s" % (activate)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST', data=module.jsonify(payload))

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def update(module,base_url,api_key,id,login,email,first_name,last_name):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url

    payload = {}
    profile = {}

    if first_name is not None:
        profile['firstName'] = first_name
    if last_name is not None:
        profile['lastName'] = last_name
    if email is not None:
        profile['email'] = email
    if login is not None:
        profile['login'] = login

    payload['profile'] = profile

    url = base_url+"/%s" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST', data=module.jsonify(payload))

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

    if info['status'] != 204:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def activate(module,base_url,api_key,id):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/lifecycle/activate" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST')

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def deactivate(module,base_url,api_key,id):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/lifecycle/deactivate" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST')

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
            action         = dict(type='str', required=False, default='list', choices=['create', 'update', 'delete', 'list', 'activate', 'deactivate']),
            id     = dict(type='str', default=None),
            login    = dict(type='str', default=None),
            password    = dict(type='str', default=None, no_log=True),
            first_name  = dict(type='str', default=None),
            last_name  = dict(type='str', default=None),
            email       = dict(type='str', default=None),
            group_ids       = dict(type='list', default=None),
            limit     = dict(type='int', default=25),
            activate   = dict(type='bool', default='yes')
        )
    )

    organization = module.params['organization']
    api_key = module.params['api_key']
    action = module.params['action']
    id = module.params['id']
    login = module.params['login']
    password = module.params['password']
    first_name = module.params['first_name']
    last_name = module.params['last_name']
    email = module.params['email']
    group_ids = module.params['group_ids']
    limit = module.params['limit']
    activate = module.params['activate']

    base_url = "https://%s-admin.okta.com/api/v1/users" % (organization)

    if action == "create":
        status, message, content, url = create(module,base_url,api_key,login,password,email,first_name,last_name,group_ids,activate)
    elif action == "update":
        status, message, content, url = update(module,base_url,api_key,id,login,email,first_name,last_name)
    elif action == "delete":
        status, message, content, url = delete(module,base_url,api_key,id)
    elif action == "activate":
        status, message, content, url = activate(module,base_url,api_key,id)
    elif action == "deactivate":
        status, message, content, url = deactivate(module,base_url,api_key,id)
    elif action == "list":
        status, message, content, url = list(module,base_url,api_key,limit)

    uresp = {}
    content = to_text(content, encoding='UTF-8')

    try:
        js = json.loads(content)
    except ValueError, e:
        js = ""

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
