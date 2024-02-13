# St John's Hostpital Cryptosystem

## Running

The login secret is: `a-very-long-secret-pls-dont-steal`

```bash

$ pip3 install -r requirements.txt
$ python3 run.py

```


## Sequence Diagrams


### Server Initialisation

```mermaid
sequenceDiagram
    Client ->> Program: Start
    Program ->> Client: Provide key
    Client ->> Program: Secret key
    Program ->> Encrypted "Database": Decrypt with secret key
    Encrypted "Database" ->> Program: Successfully decrypted database
    
    Program ->> Client: Running
```

### SSO

```mermaid
sequenceDiagram
    Client->>Application: Request Page
    Application->>Client: Unauthorised - redirect
    Client->>SSO Server: Authorise username, password, OTP
    SSO Server->>Client: Authorised redirect
    Client->>Application: Authorisation token set
    Application->>Client: Session cookie set
    Client->>Application: Request page
    Application->>Client: Authorised page response
```

### MediCloud

```mermaid
sequenceDiagram
    Authenticated Client "u1" ->> Server: View file "f1"
    Server ->> Encrypted "Database": Get files named "f1" where "u1" has access
    Encrypted "Database" ->> Server: File "f1": iv=... key=...
    Server ->> Encrypted File Store: Get file "f1" content
    Encrypted File Store ->> Server: Encrypted file "f1" content
    Server ->> Authenticated Client "u1": Plaintext from decrypting file with iv, key.
```