---
sidebar_position: 6
title: How to override environment variables
---

# Overriding Environment Variables

All overridable environment variables exist in [backend/app/settings.py](https://github.com/Swiple/swiple/blob/main/backend/app/settings.py) 
and can be overridden in [docker/.env](https://github.com/Swiple/swiple/blob/main/docker/.env) and [docker/.env-non-dev](https://github.com/Swiple/swiple/blob/main/docker/.env-non-dev)

For example, to override `ADMIN_EMAIL` update [docker/.env](https://github.com/Swiple/swiple/blob/main/docker/.env) with:
```bash
ADMIN_EMAIL=joesoap@example.com
```

For environment variables that expect dictionary types, you can wrap it in ticks or use a `__` to represent a nested value. For example:
```bash
SCHEDULER_REDIS_KWARGS='{"HOST": "redis"}'

# both are equivalent
SCHEDULER_REDIS_KWARGS__HOST=redis
```
