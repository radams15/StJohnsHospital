# St John's Hostpital Cryptosystem

## The program

The login secret is: `a-very-long-secret-pls-dont-steal`


### Running:

```bash
$ pip3 install -r requirements.txt
$ python3 run.py
```

This prompts for the secret, then runs the 6 webservers if successful.

To shutdown the webservers, press return.

### Web Addresses:

- sso - https://localhost:1111
- MedRecords - https://localhost:2222
- FinCare - https://localhost:3333
- CareConnect - https://localhost:3355
- Prescriptions - https://localhost:4444
- MediCloud - https://localhost:5555

### Generating one-time passcodes:

Ideally this would be done with OTP applications on phones or computers such as Google authenticator. Whilst this is not possible to submit, the program `gen_otp.py` can generate one-time codes for the SSO system.


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