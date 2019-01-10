#!/usr/bin/python
# (c) 2019, Whitney Champion <whitney.ellis.champion@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
module: okta_apps_saml
short_description: Communicate with the Okta API to manage SAML applications
description:
    - The Okta apps module manages Okta applications
version_added: "1.0"
author: "Whitney Champion (@shortstack)"
options:
  organization:
    description:
      - Okta subdomain for your organization. (i.e.
        mycompany.okta.com).
    required: false
    default: None
  api_key:
    description:
      - Okta API key.
    required: false
    default: None
  action:
    description:
      - Action to take against apps API.
    required: false
    default: list
    choices: [ create, update ]
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
  limit:
    description:
      - List limit.
    required: false
    default: 20
  defaultRelayState:
    description:
      - Identifies a specific application resource in an IDP initiated Single Sign-On scenario. In most instances this is blank.
    required: false
    default: None
  ssoAcsUrl:
    description:
      - The location where the SAML assertion is sent with a HTTP POST. This is often referred to as the SAML Assertion Consumer Service (ACS) URL for your application.
    required: false
    default: None
  idpIssuer:
    description:
      - SAML IdP issuer ID.
    required: false
    default: None
  audience:
    description:
      - The application-defined unique identifier that is the intended audience of the SAML assertion. This is most often the SP Entity ID of your application.
    required: false
    default: None
  recipient:
    description:
      - Recipient URL.
    required: false
    default: None
  destination:
    description:
      - Destination URL.
    required: false
    default: None
  subjectNameIdTemplate:
    description:
      - Application username template.
    required: false
    default: "${user.userName}"
  subjectNameIdFormat:
    description:
      - Application username format.
    required: false
    default: "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"
  responseSigned:
    description:
      - Determines whether the SAML authentication response message is signed or not.
    required: false
    default: True
  assertionSigned:
    description:
      - Determines whether the SAML assertion is signed or not.
    required: false
    default: True
  signatureAlgorithm:
    description:
      - Signing algorithm to sign SAML assertion and response.
    required: false
    default: "RSA_SHA256"
  digestAlgorithm:
    description:
      - Digest algorithm to sign SAML assertion and response.
    required: false
    default: "SHA256"
  honorForceAuthn:
    description:
      - Prompt user to reauthenticate if SP asks for it.
    required: false
    default: True
  authnContextClassRef:
    description:
      - SAML authentication context class.
    required: false
    default: "urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport"
  spIssuer:
    description:
      - SP issuer.
    required: false
    default: None
  requestCompressed:
    description:
      - Request compressed, true or false.
    required: false
    default: False
  attributeStatements:
    description:
      - Attribute statements.
    required: false
    default: None
"""

EXAMPLES = '''
# List apps
- okta_apps_saml:
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    limit: 20

# Create app
- okta_apps_saml:
    action: create
    organization: "unicorns"
    api_key: "TmHvH4LY9HH9MDRDiLChLGwhRjHsarTCBzpwbua3ntnQ"
    label: "Unicorn Login"
    ssoAcsUrl: "https://iloveunicorns.lol/saml/redirect"
    idpIssuer: "http://www.okta.com/${org.externalKey}"
    audience: "https://iloveunicorns.lol/saml/metadata"
    recipient: "https://iloveunicorns.lol/saml/redirect"
    destination: "https://iloveunicorns.lol/saml/redirect"
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

def create(module,base_url,api_key,label,defaultRelayState,ssoAcsUrl,idpIssuer,audience,recipient,destination,subjectNameIdTemplate,subjectNameIdFormat,responseSigned,assertionSigned,signatureAlgorithm,digestAlgorithm,honorForceAuthn,authnContextClassRef,spIssuer,requestCompressed,attributeStatements):

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
    if defaultRelayState is not None:
        signOn['defaultRelayState'] = defaultRelayState
    if ssoAcsUrl is not None:
        signOn['ssoAcsUrl'] = ssoAcsUrl
    if idpIssuer is not None:
        signOn['idpIssuer'] = idpIssuer
    if audience is not None:
        signOn['audience'] = audience
    if recipient is not None:
        signOn['recipient'] = recipient
    if destination is not None:
        signOn['destination'] = destination
    if subjectNameIdTemplate is not None:
        signOn['subjectNameIdTemplate'] = subjectNameIdTemplate
    if subjectNameIdFormat is not None:
        signOn['subjectNameIdFormat'] = subjectNameIdFormat
    if responseSigned is not None:
        signOn['responseSigned'] = responseSigned
    if assertionSigned is not None:
        signOn['assertionSigned'] = assertionSigned
    if signatureAlgorithm is not None:
        signOn['signatureAlgorithm'] = signatureAlgorithm
    if digestAlgorithm is not None:
        signOn['digestAlgorithm'] = digestAlgorithm
    if honorForceAuthn is not None:
        signOn['honorForceAuthn'] = honorForceAuthn
    if authnContextClassRef is not None:
        signOn['authnContextClassRef'] = authnContextClassRef
    if spIssuer is not None:
        signOn['spIssuer'] = spIssuer
    if requestCompressed is not None:
        signOn['requestCompressed'] = requestCompressed
    if attributeStatements is not None:
        signOn['attributeStatements'] = attributeStatements

    settings['signOn'] = signOn
    payload['signOnMode'] = "SAML_2_0"
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

def update(module,base_url,api_key,label,defaultRelayState,ssoAcsUrl,idpIssuer,audience,recipient,destination,subjectNameIdTemplate,subjectNameIdFormat,responseSigned,assertionSigned,signatureAlgorithm,digestAlgorithm,honorForceAuthn,authnContextClassRef,spIssuer,requestCompressed,attributeStatements):

    headers = '{ "Content-Type": "application/json", "Authorization": "SSWS %s", "Accept": "application/json" }' % (api_key)

    payload = {}

    url = base_url+"/%s" % (id)

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='GET', data=module.jsonify(payload))

    try:
        content = response.read()
        payload = json.loads(content)
    except AttributeError:
        content = info.pop('body', '')

    if label is not None:
        payload['label'] = label
    if defaultRelayState is not None:
        signOn['defaultRelayState'] = defaultRelayState
    if ssoAcsUrl is not None:
        signOn['ssoAcsUrl'] = ssoAcsUrl
    if idpIssuer is not None:
        signOn['idpIssuer'] = idpIssuer
    if audience is not None:
        signOn['audience'] = audience
    if recipient is not None:
        signOn['recipient'] = recipient
    if destination is not None:
        signOn['destination'] = destination
    if subjectNameIdTemplate is not None:
        signOn['subjectNameIdTemplate'] = subjectNameIdTemplate
    if subjectNameIdFormat is not None:
        signOn['subjectNameIdFormat'] = subjectNameIdFormat
    if responseSigned is not None:
        signOn['responseSigned'] = responseSigned
    if assertionSigned is not None:
        signOn['assertionSigned'] = assertionSigned
    if signatureAlgorithm is not None:
        signOn['signatureAlgorithm'] = signatureAlgorithm
    if digestAlgorithm is not None:
        signOn['digestAlgorithm'] = digestAlgorithm
    if honorForceAuthn is not None:
        signOn['honorForceAuthn'] = honorForceAuthn
    if authnContextClassRef is not None:
        signOn['authnContextClassRef'] = authnContextClassRef
    if spIssuer is not None:
        signOn['spIssuer'] = spIssuer
    if requestCompressed is not None:
        signOn['requestCompressed'] = requestCompressed
    if attributeStatements is not None:
        signOn['attributeStatements'] = attributeStatements

    response, info = fetch_url(module=module, url=url, headers=json.loads(headers), method='PUT', data=module.jsonify(payload))

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
            organization      = dict(type='str', default=None),
            api_key       = dict(type='str', no_log=True),
            action         = dict(type='str', default='list', choices=['create', 'update', 'delete', 'list', 'assign_group', 'remove_group', 'assign_user', 'remove_user', 'activate', 'deactivate']),
            id     = dict(type='str', default=None),
            label  = dict(type='str', default=None),
            limit     = dict(type='int', default=20),
            defaultRelayState     = dict(type='str', default=""),
            ssoAcsUrl     = dict(type='str', default=None),
            idpIssuer     = dict(type='str', default="http://www.okta.com/${org.externalKey}"),
            audience     = dict(type='str', default=None),
            recipient     = dict(type='str', default=None),
            destination     = dict(type='str', default=None),
            subjectNameIdTemplate     = dict(type='str', default="${user.userName}"),
            subjectNameIdFormat     = dict(type='str', default="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified"),
            responseSigned     = dict(type='bool', default=True),
            assertionSigned     = dict(type='bool', default=True),
            signatureAlgorithm     = dict(type='str', default="RSA_SHA256"),
            digestAlgorithm     = dict(type='str', default="SHA256"),
            honorForceAuthn     = dict(type='bool', default=True),
            authnContextClassRef     = dict(type='str', default="urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport"),
            spIssuer     = dict(type='str', default=None),
            requestCompressed     = dict(type='bool', default=False),
            attributeStatements     = dict(type='str', default=None),
            send_email     = dict(type='str', default='false')
        )
    )

    organization = module.params['organization']
    api_key = module.params['api_key']
    action = module.params['action']
    id = module.params['id']
    label = module.params['label']
    limit = module.params['limit']
    defaultRelayState = module.params['defaultRelayState']
    ssoAcsUrl = module.params['ssoAcsUrl']
    idpIssuer = module.params['idpIssuer']
    audience = module.params['audience']
    recipient = module.params['recipient']
    destination = module.params['destination']
    subjectNameIdTemplate = module.params['subjectNameIdTemplate']
    subjectNameIdFormat = module.params['subjectNameIdFormat']
    responseSigned = module.params['responseSigned']
    assertionSigned = module.params['assertionSigned']
    signatureAlgorithm = module.params['signatureAlgorithm']
    digestAlgorithm = module.params['digestAlgorithm']
    honorForceAuthn = module.params['honorForceAuthn']
    authnContextClassRef = module.params['authnContextClassRef']
    spIssuer = module.params['spIssuer']
    requestCompressed = module.params['requestCompressed']
    attributeStatements = module.params['attributeStatements']
    send_email = module.params['send_email']

    base_url = "https://%s-admin.okta.com/api/v1/apps" % (organization)

    if action == "create":
        status, message, content, url = create(module,base_url,api_key,label,defaultRelayState,ssoAcsUrl,idpIssuer,audience,recipient,destination,subjectNameIdTemplate,subjectNameIdFormat,responseSigned,assertionSigned,signatureAlgorithm,digestAlgorithm,honorForceAuthn,authnContextClassRef,spIssuer,requestCompressed,attributeStatements)
    elif action == "update":
        status, message, content, url = update(module,base_url,api_key,label,defaultRelayState,ssoAcsUrl,idpIssuer,audience,recipient,destination,subjectNameIdTemplate,subjectNameIdFormat,responseSigned,assertionSigned,signatureAlgorithm,digestAlgorithm,honorForceAuthn,authnContextClassRef,spIssuer,requestCompressed,attributeStatements)

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
