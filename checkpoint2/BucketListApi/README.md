# Bucket List API 
If you haven't heard of the term `"Bucket List"`, it's a list of all the things you would want to do before you die.
###Overview
`Bucket List API` is a work in progress but fundementals are currently in place, it can let you do the following:

1. Add
2. View
3. Modify
4. Delete

Responses appear in this format
```
"items": [
        {
            "date_created": "Sat, 12 Dec 2015 15:35:43 -0000",
            "date_modified": "Sat, 12 Dec 2015 15:35:43 -0000",
            "done": false,
            "id": "1",
            "name": "Finish CheckPoint 1"
        },
        {
            "date_created": "Sat, 12 Dec 2015 15:37:19 -0000",
            "date_modified": "Sat, 12 Dec 2015 15:37:19 -0000",
            "done": false,
            "id": "2",
            "name": "Finish CheckPoint 2"
        }
 ]
```


###Installation
1. ######Requirements
 Ensure that python is installed on your machine, if not follow the link [Installing python](https://www.python.org/downloads/).
 * Python 2.7+
 * Flask
 * Flask-API
 * Among others as listed in `requirements.txt`
 
2. ######Installing virtualenvwrapper
 A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them.
 To install virtualenvwrapper follow the link [installing virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
3. ######Cloning the repo

 To clone the repo type the following command in terminal:
 
 ```
 $ git clone 
 ```
 
 To install all app requirements type these command in your terminal one after the other:
 
 ```
 $ cd BucketListApi
 $ pip install -r requirements.txt
 ```
 
4. ######Setting up enviroment variables
 To set up enviroment variables follow the [Setting env variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps), so as they can be used with your app.
 Ensure your create `APP_SETTINGS` and `DATABASE_URL` in your env variables.

5. ######Managing Database set up

To get started install Postgres on your local computer if you don’t have it already. if you haven't follow this [Setting up postgresql](http://www.postgresql.org/download/) and choose your appropriate OS.
Run the following commands on the terminal to set up tables and manage upgrades to tables if you change your models.

 * In order to run our migrations initialize Alembic, this command will create a migrations `directory`:

 ```
 $ python manage.py db init
 ```

 * To create your first migration running the `migrate` command:

 ```
 $ python manage.py db migrate
 ```

 * To apply upgrades to your database use the db `upgrade` command:

 ```
 $ python manage.py db upgrade
 ```

 Your database is now ready to use with the app.

###Running the API

To run the `API` type the following command in your terminal:

```
$ python routes.py
```

And the response on the terminal will look like:

```
UserWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True to suppress this warning.
 * Debugger is active!
 * Debugger pin code: 219-232-067
```

The default url is `http://127.0.0.1:5000`. Once the server runs you can make requests to the routes by using curl in another terminal window. Requests are in the following format:

1. User Sign Up

 ```
  $ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"pac","password":"1234"}' http://127.0.0.1:5000/signup
 ```

2. Login [method = 'POST']

 ```
  $ curl -u username:password -i -X POST http://127.0.0.1:5000/login
 ```

3. Bucketlists [method = 'GET']

 ```
  $ curl -u username:password -i -X GET http://127.0.0.1:5000/bucketlists
 ```

4. Create Bucketlist [method = 'POST']

 ```
  $ curl -u username:password -i -X POST -H "Content-Type: application/json" -d '{"bucket_list_name":"Bucket List 1"}' http://127.0.0.1:5000/bucketlists
 ```

5. Update Bucket List [method = 'PUT']

 ```
  $ curl -u username:password -i -X PUT -H "Content-Type: application/json" -d '{"bucket_list_name":"New Bucket List 1"}' http://127.0.0.1:5000/bucketlists
 ```

6. Delete Bucket List [method = 'DELETE']

 ```
  $ curl -u username:password -i -X DELETE -H "Content-Type: application/json"  http://127.0.0.1:5000/bucketlists
 ```

7. Bucketlists Items [method = 'GET']

 ```
  $ curl -u username:password -i -X GET -H "Content-Type: application/json"  http://127.0.0.1:5000/bucketlists/1/items
 ```

8. Create Bucketlist Items [method = 'POST']

 ```
  $ curl -u username:password -i -X POST -H "Content-Type: application/json" -d '{"item_name":"Touch the skype"}' http://127.0.0.1:5000/bucketlists/1/items
 ```

9. Update Bucket List Item [method = 'PUT']

 ```
  $ curl -u username:password -i -X PUT -H "Content-Type: application/json" -d '{"item_name":"Update value"}' http://127.0.0.1:5000/bucketlists/1/items
 ```

10. Delete Bucket List Item [method = 'DELETE']

 ```
  $ curl -u username:password -i -X DELETE -H "Content-Type: application/json" http://127.0.0.1:5000/bucketlists/1/items
 ```



###Running tests

To run tests type the following command in terminal:

```
$ python -m unittest discover
```

And your response should contain below message:

```
............................
----------------------------------------------------------------------
    Ran 28 tests in 0.387s
    OK
```








