# Authentication module
The guide below is directed to developers.

1. [Requests Examples](#requests-examples)
   1. [Sign up](#sign-up)
   2. [Authorization token generation](#authorization-token-generation)
   3. [Access token generation](#access-token-generation)
   3. [Access token Validation](#access-token-validation)
   3. [Remove User](#remove-user)
2. [Building and deploying](#building-and-deploying)
   1. [Kubernetes](#kubernetes)
   2. [Docker](#docker)
      1. [Mongo](#mongo-image)
      2. [Auth](#auth-image)
3. [Miscellaneous](#miscellaneous)
   1. [Access code deadline corruption](#access-code-deadline-corruption)
   2. [Server Password](#private-key-password)

This is the authentication providing service of the moviefan
app. It provides basic _sign-in_, _log-in_ and _oauth_ operations, such as:
 * Authorization token generation
 * Access token generation
 * Access token validation

See ![OpenAPI Specification](src/swagger_server/swagger/swagger.yaml) for
full details over the API.

## Requests examples
The following examples use python to construct the
http requests.

### Sign-up
```python
import requests
response = requests.post(
            "http://idp.moviefans.k3s:80/deti-egs-moviefan/Authentication/1.0.0/v1/signup",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
# Print the response
response.json()
```

The API response will contain:
* A status description
* A status code

Example responses:

```json
{"status": "OK / Operation success", "status_code": "0"}
```

```json
{"status": "Can't add user, he already exists!", "status_code": "5"}
```

### Authorization Token Generation
In this operation, you will send the credentials in your
POST request.
```python
import requests
response = requests.post(
"http://idp.moviefans.k3s:80/deti-egs-moviefan/Authentication/1.0.0/v1/auth-token",
json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
)
# Print the response
response.json()
```
The API will return:
* A status description
* A status code
* A hexadecimal string - the authorization token

Example responses:
```json
{"auth_code": "5e31a6b534b62dcea6f1f66df08ae90639c7d091931479cac2daa3822432c2e8144303657ef4ac570907182b959987e3c69f8e443ae2feb8311d8b7f0e503ef60f350d6f593e96677367a7d5cfe47efb6de01cc07087cdd08671238cd0663d6fa3948178cfc5de28ff62497bbfcdfe3061d8a145fbd3b222ec2748ac27d0ccf42b1a2c2ada996c52ac4ebfc163bd10ebd0c5fad8c575e9e6ea3176476fb46833b16bb985d1ded98d813a18b563081b444264918a383a83ef4a1c18f590a6c46fdc760c588b09cca8b3c0270d83aa9504aee7f1c27e54aef2148a3564130e5b93f8519d9976c600e43a3a5c16c2bc93e4a90747076dad269fb7afdb9852bc7c5f", "status": "OK / Operation success", "status_code": "0"}
```
```json
{"auth_code": "", "status": "Password incorrect", "status_code": "43"}
```

### Access Token Generation
In this operation, you will send your credentials and
your previously obtained authorization token in the POST
request.

```python
import requests
response = requests.post(
            "http://idp.moviefans.k3s:80/deti-egs-moviefan/Authentication/1.0.0/v1/access-token",
            json=dict(
                authtoken='31d38d6e8ce7ab42f34467135aa19225982f9e8965595bbe74f8734'
                          '8a16a9455c4387cc5d66f02b68d76f5310e7cdd76db98a09cfdeffcb1a50f7e145122b044',
                username="user1", email="user1@it.org", password="user1Pa$$"
            )
        )
# Print the result
response.json()
```
The API will return:
* A status description
* A status code
* A hexadecimal string - the authorization token

Example responses:
```json
{"access_token": "20f9d503961dc47cafb66887821e3dc0422d88f0648c9bbc008e74e24e0792a44a247f73be6d0e5488e82d22a7f01fe07c5807d5684b2e83c1af80c2160d3fc8f525cc33d46662d118be820938216e1636e750365e4701b70593d230d1faa9e0eef4a9aa2fa384b39222245af6eb5a1cc913fc465d7b193c51fbbe75ed991743f6e5e26aa8c7e9e623cf5d7a2cd7a61b49dd7e2f4e272d4e4f3a10526a974b6794f411957be7a874070c58a757d7685a51d050e1abc1e6e142be604ac1762f715033a29751949bbb8204acbeb3d61e88536b4fc4b85b8d098a671c344a0d9efccd611678d33ff5cf2b6f481295e1fd2fec6651a7407aaf37fa4a23d5798bd3f4-ds1657477224170707406", "status": "OK / Operation success", "status_code": 0}
```
```json
{"access_token": "", "status": "Authorization code is invalid!", "status_code": 61}
```

### Access Token Validation
In this operation, you will need to provide the access
token and the authorization token generated with the
generation endpoints.

```python
import requests
response = requests.post(
            url='http://idp.moviefans.k3s:80/deti-egs-moviefan/Authentication/1.0.0/v1/validate-access-token',
            json=dict(
                auth_code='31d38d6e8ce7ab42f34467135aa19225982f9e8965595bbe74f8734'
                          '8a16a9455c4387cc5d66f02b68d76f5310e7cdd76db98a09cfdeffcb1a50f7e145122b044',
                access_token='07cad294e65af23925cc85cf9a435ba2d8cd6e3bd52433736a0dfba29e50c499f79f31'
                             '1870ece437b16a62c79ee9f7b74a495020d68c43d1db17d5880efadb13-ds1652374634009943200'
            )
        )
response.json()
```

The API will return:
* A status description
* A status code

Example responses:
```json
{"status": "OK / Operation success", "status_code": "0"}
```
```json
{"status": "Access token is no longer valid!", "status_code": "63"}
```
```json
{"status": "Access token is not valid!", "status_code": "62"}
```

### Remove user
In this operation, you will send your credentials
in the POST request in order to remove the user from the
database.
```python
import requests
response = requests.post(
            "http://idp.moviefans.k3s:80/deti-egs-moviefan/Authentication/1.0.0/v1/signout",
            json=dict(username="user1", email="user1@it.org", password="user1Pa$$")
        )
response.json()
```

The API will return:
* A status description
* A status code

Example responses:
```json
{"status": "OK / Operation success", "status_code": "0"}
```
```json
{"status": "User with requested credentials does not exist", "status_code": "4"}
```

## Building and Deploying


For this part, you will need to have [docker]() and 
[kubernetes]() installed on your machine.

[//]: # (For a more detailed guide on kubernetes, see this [guide]&#40;&#41;.)

For going through the next parts, you will need:
* Your machine connected the local network of the university
* An OpenVPN network with the configurations as shown
  in the official course page

After the above requirements are met, you can proceed.

### Kubernetes

To apply the configurations, run:
```shell
# Remember to run these in the authentication dir
kubectl apply -f deploy_auth/storage.yaml
kubectl apply -f deploy_auth/mongo.yaml
kubectl apply -f deploy_auth/deployment.yaml
```

To delete the resources created with the above
command, run:
```shell
# Remember to run this in the authentication dir
kubectl delete -f deploy_auth/deployment.yaml
kubectl delete -f deploy_auth/mongo.yaml 
kubectl delete -f deploy_auth/storage.yaml
```

### Docker

#### Mongo Image

You will pull the image from the docker repositories and push it to the private registry:

Pull mongodb image:
```shell
sudo docker pull mongo:4.4
```

Rename the image:
```shell
sudo docker image tag mongo:4.4 registry.deti:5000/egs9/auth-mongodb:20220615
```

Push mongodb image:
```shell
sudo docker push registry.deti:5000/egs9/auth-mongodb:20220615
```

#### Auth Image
You will build the image and push it to the private
registry of the university.

Build the image:
```shell
# Remember to run this in the authentication dir - YYYYMMDDHHmm
sudo docker build -t registry.deti:5000/egs9/auth:202206171147 -f deploy_authentication/Dockerfile.dev .
```

Run the container:
```shell
sudo docker run --name auth -d -p 8001:8001 registry.deti:5000/egs9/auth:202206171147
```

Push it to the registry:
```shell
sudo docker push registry.deti:5000/egs9/auth:202206171147
```

## Miscellaneous

### Access code deadline corruption
This is a vulnerability.
The access token deadline part, the number after the "-ds",
can be corrupted without the knowledge of the module.
That is because that part is not signed, and thus it
cannot be verified with the public key belonging to
the authentication entity.

### Private key password
This part is critical for running the entire module.
The ![pem file](src/auth_lib/auth_private_key.pem) 
contains the serialized private key of this module
which is password-protected. The program will try to
find the password in a text file named _password_.
This file is not in version control, and thus it must be
created with the password in its contents.

If you know the password, but not yet have the password file,
run the following command:
```shell
# Switch $password with the password
echo $password > src/auth_lib/password
```