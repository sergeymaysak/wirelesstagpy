#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Model class for push notification config for wirelesstags platform.

Copyrights: (c) 2018 Sergiy Maysak, see LICENSE file for details
Creation Date: 3/20/2018
"""


class NotificationConfig:
    """Model representing push notification configuration for single tag."""

    @classmethod
    def make_post_local(cls, name, url, content):
        """Create local push notification using POST http verb."""
        return cls(name, {'url': url, 'verb': 'POST',
                          'content': content,
                          'disabled': False, 'nat': True})

    def __init__(self, name, spec):
        """Init with name of event and dictionary."""
        self.name = name
        self.spec = spec

    @property
    def url(self):
        """URL to receive notification."""
        return self.spec["url"]

    @property
    def verb(self):
        """HTTP verb: GET, POST etc."""
        return self.spec["verb"]

    @property
    def is_enabled(self):
        """Is notification enabled or not."""
        return not self.spec["disabled"]

    @property
    def is_local(self):
        """Is notification local."""
        return self.spec["nat"]

    @property
    def content(self):
        """Notification tempplate to be sent."""
        return self.spec["content"]

    def __repr__(self):
        """Return string representation."""
        return '{} spec: {}'.format(self.name, self.spec)
