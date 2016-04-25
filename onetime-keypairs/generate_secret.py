#!/usr/bin/env python

import uuid

with open('/var/secret', 'w') as f:
    f.write('SECRET=%s\n' % uuid.uuid4())
