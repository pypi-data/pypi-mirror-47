# Vxapi Client
The Vxfiber API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes, authentication, and verbs.

This Python library provides convenient access to the Vxfiber API from applications written in the Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically from API responses which makes it compatible with a wide range of versions of the vxfiber API.

## Examples

#### Client initialization
Give url and path for swagger's cache (it automatically call spec endpoint to known all specification's endpoints)
> client = Client(url='https://vxapitest-test-test.vx.se', cache_path='/tmp/pyvxclient.swagger')
> token = client.get_token('massimo', 'password')
> client.api_key = token['api_key']
> client.setup()

#### Actions

- get customers with limit results
> client.Customers.Get(limit=5)
- get just customers on first page
> client.Customers.Get(page=1, per_page=20)
- get customers filtered and ordered
> client.Customers.Get(limit=5, q=["country_code:it","city:Milan"], sort="-created")

- get single customer
> client.Customers.Get(limit=5, q=["id:D28E299D-8673-41AB-89B4-1B20F64F8E02"])

- create customer
> ret = client.Customers.Create(first_name='pluto',
                          last_name='pluto',
                          password='ciao#1234',
                          email='ciao@test.it',
                          province='',
                          city='',
                          customer_type='Residential',
                          postal_code='',
                          language='English',
                          mobile_number='',
                          phone_number='',
                          street_address='')
> idc = ret.data['id']

- modify customer
> client.Customers.Update(id=idc, first_name='pluto2')

There are many others resources (partially or full implemented):

- client.ApiUser
- client.Inventory
- client.NetworkOperator
- client.Network
- client.ObjectGroup
- client.Objects
- client.Orders
- client.Customers
- client.Services
