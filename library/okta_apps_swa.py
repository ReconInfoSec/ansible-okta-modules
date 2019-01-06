#!/usr/bin/python
# (c) 2019, Whitney Champion <whitney.ellis.champion@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: okta_apps_swa
short_description: Communicate with the Okta API to manage applications
description:
    - The Okta apps module manages Okta applications
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
      - Action to take against apps API.
    required: false
    default: list
    choices: [ create, update, delete, list ]
  id:
    description:
      - ID of the app.
    required: false
    default: None
  login_url:
    description:
      - Login URL for the app.
    required: false
    default: None
  redirect_url:
    description:
      - Redirect URL for the app.
    required: false
    default: yes
  limit:
    description:
      - List limit.
    required: false
    default: 20
"""

EXAMPLES = '''
# List apps
- okta_apps_swa:
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    limit: 20

# Create app
- okta_apps_swa:
    action: create
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    label: "I Love Unicorns"
    redirect_url: "https://iloveunicorns.lol/redirect"
    login_url: "https://iloveunicorns.lol/signin"

# Delete app
- okta_apps_swa:
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

def create(module,base_url,api_key,label,login_url,redirect_url):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    payload = {}
    settings = {}
    signOn = {}

    if label is not None:
        payload['label'] = label
    if login_url is not None:
        signOn['loginUrl'] = login_url
    if redirect_url is not None:
        signOn['redirectUrl'] = redirect_url

    settings['signOn'] = signOn
    payload['settings'] = settings
    payload['label'] = label

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
            login_url  = dict(type='str', default=None),
            redirect_url  = dict(type='str', default=None),
            label  = dict(type='str', default=None),
            limit     = dict(type='int', default=20)
        )
    )

    organization = module.params['organization']
    api_key = module.params['api_key']
    action = module.params['action']
    id = module.params['id']
    login_url = module.params['login_url']
    redirect_url = module.params['redirect_url']
    label = module.params['label']
    limit = module.params['limit']

    base_url = "https://%s-admin.okta.com/api/v1/apps" % (organization)

    if action == "create":
        status, message, content, url = create(module,base_url,api_key,label,login_url,redirect_url)
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
