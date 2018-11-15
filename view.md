# View As

## Questions

9.1. An access token is a encrypted string which identifies either a user, app, or page and is obtained at login.  The access token is used any time an API is called to read, write, or modify a user's data.

9.2. When using the "view as" feature in Facebook, hackers were able to look at the video uploader.  That video uploader was then producing the access token of the user who the hackers were viewing the page as.

9.3. By forcing the users to log out, Facebook could create a new access token for the user when they logged back in.  The hackers' stolen access code would then be useless.

9.4. Flask's session cookies differ from access tokens in that cookies are stored both on the client side as well as in a database on the server.  In contrast, access tokens are exclusively stored client side and not in the database, which has the advantage of not having to update the databses every time a user logs out.

## Debrief

a. These links: https://arstechnica.com/information-technology/2018/09/50-million-facebook-accounts-breached-by-an-access-token-harvesting-attack/ and https://dzone.com/articles/cookies-vs-tokens-the-definitive-guide

b. 35 minutes
