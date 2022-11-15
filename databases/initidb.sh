#!/bin/sh
helm install doubleauth-db ./doubleauth_db/mysql/
helm install group-db ./groups_db/mysql/
helm install login-db ./login_db/mysql/
helm install private-db ./private_db/mysql/
helm install shared-db ./shared_db/mysql/