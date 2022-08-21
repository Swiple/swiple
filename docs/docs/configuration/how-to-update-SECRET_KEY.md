---
sidebar_position: 3
---

# How to Update SECRET_KEY

Run the following snippet to create a Fernet Key and set `SECRET_KEY` to it.
```python
from cryptography.fernet import Fernet

fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # your fernet_key, keep it in a secure place!
```

:::note Note
At this time, changing `SECRET_KEY` after data sources have been added will cause connections to them to fail. Secret rotation is on the roadmap.
:::