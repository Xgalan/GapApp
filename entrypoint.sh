#!/bin/bash
# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python ./gap/manage.py makemigrations
python ./gap/manage.py migrate
python ./gap/manage.py collectstatic --no-input

# load users from dumped existing data
USERS="users.json"
if [ -f $USERS ]; then
    python ./gap/manage.py loaddata $USERS
fi


# load fixtures, see content of loaddata.example
# ./gap/loaddata.example

# for creating first superuser you could use:
# cat ./gap/createsuperuser.example | python ./gap/manage.py shell
# cat ./gap/createuser.example | python ./gap/manage.py shell

exec "$@"