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
    choices: [ create, update, delete, list, assign_user, remove_user, assign_group, remove_group, activate, deactivate ]
  id:
    description:
      - ID of the app.
    required: false
    default: None
  label:
    description:
      - App label.
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
  group_id:
    description:
      - Group ID to assign an app to.
    required: false
    default: 20
  scheme:
    description:
      - Authentication scheme.
    required: false
    default: None
  username:
    description:
      - Username for the app, requires scheme to be defined.
    required: false
    default: None
  password:
    description:
      - Password for the app, requires scheme to be defined.
    required: false
    default: None
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

# Update app to use shared username and password set by Okta admin
- okta_apps_swa:
    action: update
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    scheme: "SHARED_USERNAME_AND_PASSWORD"
    username: "analyst_user"
    password: "shared_analyst_password"

# Update app to use passwords set by Okta admin
- okta_apps_swa:
    action: update
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    scheme: "ADMIN_SETS_CREDENTIALS"

# Update app login and redirect URLs
- okta_apps_swa:
    action: update
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    redirect_url: "https://iloveunicorns.lol/redirect"
    login_url: "https://iloveunicorns.lol/signin"

# Activate app
- okta_apps_swa:
    action: activate
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"

# Dectivate app
- okta_apps_swa:
    action: deactivate
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"

# Delete app
- okta_apps_swa:
    action: delete
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"

# Assign an app to a group
- okta_apps_swa:
    action: assign_group
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    group_id: "01c5pEucucMPWXjFM457"

# Remove a group from an app
- okta_apps_swa:
    action: remove_group
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    group_id: "01c5pEucucMPWXjFM457"

# Assign an app to a user
- okta_apps_swa:
    action: assign_user
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    user_id: "01c5pEucucMPWXjFM456"
    send_email: "false"

# Remove a user from an app
- okta_apps_swa:
    action: remove_user
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    id: "01c5pEucucMPWXjFM456"
    user_id: "01c5pEucucMPWXjFM456"
    send_email: "false"
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
    features = []
    hide = {}

    hide['iOS'] = "false"
    hide['web'] = "false"

    visibility = {}
    visibility['autoSubmitToolbar'] = "false"
    visibility['hide'] = hide

    if label is not None:
        payload['label'] = label
    if login_url is not None:
        signOn['loginUrl'] = login_url
    if redirect_url is not None:
        signOn['redirectUrl'] = redirect_url

    settings['signOn'] = signOn
    payload['signOnMode'] = "AUTO_LOGIN"
    payload['features'] = features
    payload['visibility'] = visibility
    payload['settings'] = settings

    url = base_url

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST', data=module.jsonify(payload))

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def update(module,base_url,api_key,label,login_url,redirect_url,id,scheme,username,password_input):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    payload = {}
    password = {}

    url = base_url+"/%s" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='GET', data=module.jsonify(payload))

    try:
        content = response.read()
        payload = json.loads(content)
    except AttributeError:
        content = info.pop('body', '')

    if label is not None:
        payload['label'] = label
    if login_url is not None:
        payload['settings']['signOn']['loginUrl'] = login_url
    if redirect_url is not None:
        payload['settings']['signOn']['redirect_url'] = redirect_url

    if (scheme is not None) and (username is not None) and (password_input is not None):
        payload['credentials']['scheme'] = scheme
        payload['credentials']['userName'] = username
        password['value'] = password_input
        payload['credentials']['password'] = password
    elif scheme is not None:
        credentials = {}
        userNameTemplate = {}
        userNameTemplate['template'] = "${source.login}"
        userNameTemplate['type'] = "BUILT_IN"
        credentials['scheme'] = scheme
        credentials['userNameTemplate'] = userNameTemplate
        payload['credentials'] = credentials

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='PUT', data=module.jsonify(payload))

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

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='DELETE')

    if info['status'] != 204:
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

def assign_group(module,base_url,api_key,group_id,id):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/groups/%s" % (id,group_id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='PUT')

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def remove_group(module,base_url,api_key,group_id,id):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/groups/%s" % (id,group_id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='DELETE')

    if info['status'] != 204:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def assign_user(module,base_url,api_key,user_id,id,send_email):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/users/%s?sendEmail=%s" % (id,user_id,send_email)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='POST')

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % (info['msg']))

    try:
        content = response.read()
    except AttributeError:
        content = info.pop('body', '')

    return info['status'], info['msg'], content, url

def remove_user(module,base_url,api_key,user_id,id,send_email):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    url = base_url+"/%s/users/%s?sendEmail=%s" % (id,user_id,send_email)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='DELETE')

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

def main():
    module = AnsibleModule(
        argument_spec = dict(
            organization      = dict(type='str', required=True, default=None),
            api_key       = dict(type='str', required=True, no_log=True),
            action         = dict(type='str', required=False, default='list', choices=['create', 'update', 'delete', 'list', 'assign_group', 'remove_group', 'assign_user', 'remove_user', 'activate', 'deactivate']),
            id     = dict(type='str', default=None),
            group_id     = dict(type='str', default=None),
            user_id     = dict(type='str', default=None),
            login_url  = dict(type='str', default=None),
            redirect_url  = dict(type='str', default=None),
            label  = dict(type='str', default=None),
            scheme  = dict(type='str', default=None, choices=['ADMIN_SETS_CREDENTIALS', 'EDIT_PASSWORD_ONLY', 'EDIT_USERNAME_AND_PASSWORD', 'EXTERNAL_PASSWORD_SYNC	', 'SHARED_USERNAME_AND_PASSWORD']),
            username  = dict(type='str', default=None),
            password  = dict(type='str', default=None, no_log=True),
            limit     = dict(type='int', default=20),
            send_email     = dict(type='str', default='false')
        )
    )

    organization = module.params['organization']
    api_key = module.params['api_key']
    action = module.params['action']
    id = module.params['id']
    group_id = module.params['group_id']
    user_id = module.params['user_id']
    login_url = module.params['login_url']
    redirect_url = module.params['redirect_url']
    label = module.params['label']
    limit = module.params['limit']
    scheme = module.params['scheme']
    username = module.params['username']
    password = module.params['password']
    send_email = module.params['send_email']

    base_url = "https://%s-admin.okta.com/api/v1/apps" % (organization)

    if action == "create":
        status, message, content, url = create(module,base_url,api_key,label,login_url,redirect_url)
    elif action == "update":
        status, message, content, url = update(module,base_url,api_key,label,login_url,redirect_url,id,scheme,username,password)
    elif action == "delete":
        status, message, content, url = deactivate(module,base_url,api_key,id)
        status, message, content, url = delete(module,base_url,api_key,id)
    elif action == "list":
        status, message, content, url = list(module,base_url,api_key,limit)
    elif action == "assign_group":
        status, message, content, url = assign_group(module,base_url,api_key,group_id,id)
    elif action == "remove_group":
        status, message, content, url = remove_group(module,base_url,api_key,group_id,id)
    elif action == "assign_user":
        status, message, content, url = assign_user(module,base_url,api_key,user_id,id,send_email)
    elif action == "remove_user":
        status, message, content, url = remove_user(module,base_url,api_key,user_id,id,send_email)
    elif action == "activate":
        status, message, content, url = activate(module,base_url,api_key,id)
    elif action == "deactivate":
        status, message, content, url = deactivate(module,base_url,api_key,id)

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
