rm db.sqlite3
rm -rf ./artseenapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations artseenapi
python3 manage.py migrate artseenapi
python3 manage.py loaddata users
python3 manage.py loaddata cities
python3 manage.py loaddata galleries
python3 manage.py loaddata artists
python3 manage.py loaddata tokens
python3 manage.py loaddata arttypes
python3 manage.py loaddata mediums
python3 manage.py loaddata subtypes
python3 manage.py loaddata artsubrelationships
python3 manage.py loaddata surfaces
python3 manage.py loaddata artists
python3 manage.py loaddata pieces
python3 manage.py loaddata piecesubtypes