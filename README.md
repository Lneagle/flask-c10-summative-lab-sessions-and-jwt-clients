# MyJournal
A simple app for keeping notes or journal entries

## Installation
**Use pipenv to install required packages**
```bash
pipenv install
pipenv shell
```
**Change into the `client-with-jwt` directory and use `npm` to install and run the frontend code:**
```bash
cd client-with-jwt
npm install
npm start
```

**Exit the `client-with-jwt` directory, then change into the `server` directory and configure the `FLASK_APP` and `FLASK_RUN_PORT` environment variables:**
```bash
cd ..
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```
Note: the frontend configuration specifies port 5555 for the backend.  If you are running the server on another port, you will need to update "proxy" in client-with-jwt/package.json.

**Initialize the database**
```bash
flask db init
flask db migrate -m 'message about your migration here'
flask db upgrade head
```

**Add a .env file to your root directory with your JWT secret key:**
```python
JWT_SECRET="your-secret-key-here"
```

**Run `python app.py` from the `server` directory**

## Usage
The following endpoints are available:
* POST /login
  * Log into the app
* POST /signup
  * Create a new account
* GET /me
  * Verifies authorization
* GET /posts
  * Lists all posts created by the current user
* GET /posts?page=1&per_page=5
  * Posts are paginated (5 per page by default).  Use querystrings to retrieve a different number or page of posts.
* POST /posts
  * Create a new post
* GET /posts/<id>
  * Get an individual post
* PATCH /posts/<id>
  * Update a post
* DELETE /posts/<id>
  * Delete a post
 
## Notes
The frontend is not yet complete; currently, you can sign up or log in.
