# Todo API using Python and FlaskRESTPlus

A Todo API to keep track of tasks with OAuth2 authenticated endpoints.

## Serving the API

### Replicate the codebase

```
git clone https://github.com/karthik-d/Flask-Todo-API-with-Auth-from-scratch
```  

### Move to the app's directory

```
cd Flask-Todo-API-with-Auth-from-scratch/Task1-TodoAPI
```  

### Create a fresh Database Schema

```
flask refresh-db
```

### Run the server

```
python app.py
```  
or with,
```
FLASK_APP=app.py && flask run
```

## Querying the API

The API is authenticated using oAuth2 Implicit-Flow and therefore
requires a valid token to query the endpoints

### Generating a Token

```
GET http://localhost:<port>/oauth/authorize
```

The following parameters have to be passed as query-strings in the URL,
as per the conventions of oAuth2 authentication scheme:

 - `client_id`: Registered client ID of the server that will query the API. For testing, use `test_todoapp`. More client-ids can be added in the [config.py](./config.py) file in the app's root directory.
 - `response_type`: Must be `token` to render back a token.
 - `scope`: The scopes of access that the client requires. Can be `readonly`,`readwrite` or `admin`.
 - `state` : An arbitraray string that will be passed back along with the token to prevent CSRF attacks.
 - `redirect_uri` : The URI to redirected to with the generated token.

 The request will redirect to a `credentials` page where the admin username and password will need to be entered. The test values are set in [config.py](./config.py) (username: `admin`; password: `admin`).

 If the credentials validate, the api-token is rendered back as JSON along with the `state` passed initially.
     

 > **Note that** the actual response would be to redirect to the supplied `redirect_uri` with the values for `token` and `state` set as query strings. The client server would then pass this token with the Authorization-Header during each request. The code for this is 'commented out' in [views.py](./todoapp/authpages/views.py). For testing the API from a browser client, the token is simply returned and diplayed as JSON on the browser and has to be manually added to the header.

 On each API request that requires token-authentication, attach the token to the request header under the field `X-Api-Token`.
