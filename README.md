# ansible-okta-modules
Ansible modules for the Okta API

A full example playbook can be found in `main.yml`.

### In Progress

* SAML apps

### Modules

The following modules are available with the corresponding actions:

* okta_users
  * create
  * update
  * delete
  * list
  * activate
  * deactivate
* okta_groups
  * create
  * update
  * delete
  * list
  * add_user
  * remove_user
* okta_apps_swa
  * create
  * update
* okta_apps_saml
  * create
  * update
* okta_apps
  * delete
  * list
  * activate
  * deactivate
  * assign_user
  * remove_user
  * assign_group
  * remove_group

### Examples

#### Create User

```
- name: Create Okta user
  okta_users:
    action: create
    organization: "{{ organization }}"
    api_key: "{{ api_key }}"
    login: "{{ email }}"
    first_name: "First"
    last_name: "Last"
    activate: true
    password: "{{ password }}"
    group_ids:
      - "{{ okta_group.json.id }}"
    email: "{{ email }}"
  register: okta_user

- name: Print user information
  debug:
    msg: "{{ okta_user.json }}"
```

#### Create Group

```
- name: Create Okta group
  okta_groups:
    action: "create"
    name: "Test"
    description: ""
    organization: "{{ organization }}"
    api_key: "{{ api_key }}"
  register: okta_group

- name: Print group information
  debug:
    msg: "{{ okta_group.json }}"
```

#### Create custom SWA app

```
- name: Create Okta app
  okta_apps_swa:
    action: create
    organization: "{{ organization }}"
    api_key: "{{ api_key }}"
    label: "Test SWA App"
    login_url: "https://unicorns.lol/login"
    redirect_url: "https://unicorns.lol/redirect"
  register: okta_app

- name: Print app information
  debug:
    msg: "{{ okta_swa_app.json }}"
```

#### Create custom SAML app

```
- name: Create SAML app
  okta_apps_saml:
    action: create
    organization: "{{ organization }}"
    api_key: "{{ api_key }}"
    label: "Test SAML App"
    ssoAcsUrl: "https://app.unicorns.lol/saml/acs"
    idpIssuer: "http://www.okta.com/${org.externalKey}"
    audience: "https://app.unicors.lol/saml/metadata"
    recipient: "https://app.unicorns.lol/saml/acs"
    destination: "https://app.unicorns.lol/saml/acs"
  register: okta_saml_app

- name: Print app information
  debug:
    msg: "{{ okta_saml_app.json }}"
```
