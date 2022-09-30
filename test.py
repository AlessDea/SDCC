import secrets  # https://docs.python.org/3/library/secrets.html
import bcrypt


# con questo secrets.token_hex() si può prendere un salt

def fun():
    p = secrets.token_hex(10)
    print(p)


if __name__ == '__main__':
    # fun()
    password = "porcamadonna"

    bytes = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()
    print(salt)

    # Hashing the password
    hash = bcrypt.hashpw(bytes, salt)

    print(hash)
    print(len(hash.decode()))
