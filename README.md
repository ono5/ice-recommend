# ice-recommend

https://icecream-recommend.herokuapp.com/

## Setup
### Install
```
python3 -m virtualenv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### activate

```
source env/bin/activate
```

### Heroku 準備

```
heroku login

heroku create icecream-recommend

heroku stack

# 20に設定(python 3.7を動かしたい)
heroku stack:set heroku-20
```

## Data import

```
$ sqlite3 appserver.sql
sqlite> .mode csv
sqlite> .import datasets/item_head.csv icecream
sqlite> select * from icecream;

sqlite> .import datasets/user_head.csv user
sqlite> .import datasets/rating_head.csv rate
```

## CSS
```
		<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css')}}" />
```
