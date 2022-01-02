from .base import *  # noqa F403

env_name = config('ENV', default='LOCAL')  # noqa F405

if env_name == 'PRODUCTION':
    from .production import *  # noqa F403
if env_name == 'LOCAL':
    from .local import *  # noqa F403

if TESTING:  # noqa F405
    from .test import *  # noqa F403
