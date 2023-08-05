# coding: utf-8
# Modified Work: Copyright (c) 2018, 2019, Oracle and/or its affiliates. All rights reserved.
# Copyright 2008-2016 Andrey Petrov and contributors

import collections
from ..packages import six
from ..packages.six.moves import queue

if six.PY2:
    # Queue is imported for side effects on MS Windows. See issue #229.
    import Queue as _unused_module_Queue  # noqa: F401


class LifoQueue(queue.Queue):
    def _init(self, _):
        self.queue = collections.deque()

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()
