# Signup

##### URL Path

    /signup/

##### Method

    /POST

##### Request Body

    {
        "fullname": "John Doe",
        "email": "johndoe@example.com",
        "password": "password"
    }

##### Response

    {
        "message": "User created successfully",
        "user": {
            "id": 1,
            "fullname": "John Doe",
            "email": "johndoe@Enecode.com"
        }
    }

# Login

##### URL Path

    /login/

##### Method

    /POST

##### Request Body

    {
        "email": "johndoe@enemcode.com",
        "password": "8pas8swo8r9d",
    }

##### Response

    {
        "user": {
            "fullname": "John Doe",
            "email": "johndoe@example.com"
        },
        "token": {
            "refresh": "refresh_token_string",
            "access": "access_token_string"
        }
    }

# Logout    

##### URL Path

    /logout/

##### Method:  
    
    /POST

##### Request Body
    {
        "refresh": "refresh_token_string"
    } 

##### Response
    {
        "status": "success"
    }
