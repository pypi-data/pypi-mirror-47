#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Tests for pyvo.io.vosi
"""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import pyvo.io.uws as uws

from astropy.utils.data import get_pkg_data_filename


class TestJob(object):
    def test_job(self):
        job = uws.parse_job(get_pkg_data_filename(
            "data/job.xml"))

        assert job.jobid == '1337'
