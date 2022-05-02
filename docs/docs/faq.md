---
sidebar_position: 4
---

# FAQ  💬

### Q: `Failed to authenticate` when signing in .

This happens when the `/login` request succeeds but the `Set-Cookie` in the response does not. 

#### Solution 1

When running locally, make sure you are using [http://127.0.0.1:3000/login](http://127.0.0.1:3000/login) **NOT** [http://localhost:3000/login](http://localhost:3000/login) 

Browsers require at least 2 dots in the url when setting the cookie; hence why the cookie is not being set for `localhost`.

#### Solution 2 (OAuth)

Redirect URL's do not match.