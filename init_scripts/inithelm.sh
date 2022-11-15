#!/bin/sh
helm install doubleauth-db ../databases/doubleauth_db/mysql/
helm install group-db ../databases/groups_db/mysql/
helm install login-db ../databases/login_db/mysql/
helm install private-db ../databases/private_db/mysql/
helm install shared-db ../databases/shared_db/mysql/
helm install rabbitmq ../rabbitmq/rabbitmq/