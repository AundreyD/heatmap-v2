cd map
yarn build
cd ..
cd server
pip install requirements.txt
web: gunicorn wsgi:app