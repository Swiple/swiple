---
sidebar_position: 1
---

# Overriding Env Variables

All overridable environment variables exist in [backend/app/settings.py](https://github.com/Swiple/swiple/blob/main/backend/app/settings.py) 
and can be overridden in [docker/.env](https://github.com/Swiple/swiple/blob/main/docker/.env) and [docker/.env-non-dev](https://github.com/Swiple/swiple/blob/main/docker/.env-non-dev)

For example, to override `ADMIN_EMAIL` update [docker/.env](https://github.com/Swiple/swiple/blob/main/docker/.env) with:
```bash
ADMIN_EMAIL=joesoap@example.com
```

For env variables that expect dictionary types, you can use a `__` for nested values. For example, to override `SCHEDULER_REDIS_KWARGS`, `HOST`:
```bash
SCHEDULER_REDIS_KWARGS__HOST=redis

# This is equivalent to
SCHEDULER_REDIS_KWARGS='{"HOST": "redis"}'
```
