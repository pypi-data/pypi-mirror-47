## Usage

### Install 
```
pip install mlc_auth
```

### Initialize
Before initializing MLC_Auth, the app.config['SECRET_KEY'] must be set.
```python
from mlc_auth import MLC_Auth

mlc_auth = MLC_Auth(app=app)
```

### Use on routes
The accessable_by parameter is optional. When accessable_by is None, all logged in users have access.
```python

@app.route('/edit', methods=['GET'])
@mlc_auth.auth_required(accessable_by=['guest', 'user', 'manager', 'administrator'])
def edit_page():
    return render_template('edit.html')
```

### Current user model
User model properties:
- id
- email
- name
- role
- organisation_id
- organisation_name

usage:
```python
from flask_login import current_user

print(current_user.id) 
```

### Fetch data from the API

```python
from mlc_auth import MLC_Auth

organisation_info = MLC_Auth.api.get(endpoint='/api/organisation/1', params={'key':'value'})

response = MLC_Auth.api.put(endpoint='/api/user/1/settings', body={'key': 'value'}, params={'key':'value'})
```

### Development environment

1. The following line needs to be added to your Hosts file:
```
127.0.0.1 local-<Your app name here>.mlc-services.com
```
2. Start the application development server.
3. Go to `http://local-<Your app name here>.mlc-services.com:5000`
