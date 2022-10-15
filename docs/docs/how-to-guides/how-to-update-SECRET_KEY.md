---
sidebar_position: 5
title: How to generate a SECRET_KEY
---

# How to Update SECRET_KEY

Run the following snippet to create a Fernet Key and set `SECRET_KEY` to it.

```sh
poetry run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

:::note Note
At this time, changing `SECRET_KEY` after data sources have been added will cause connections to them to fail. Secret rotation is on the roadmap.
:::