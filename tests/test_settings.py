#!/usr/bin/env python
# encoding: utf-8
import unittest

from . import config
from workin.conf.settings_manager import Settings


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.settings = Settings()
        self.settings.configure()

    def test_settings(self):
        self.assertEqual(self.settings.debug, True)
        self.assertEqual(self.settings['debug'], True)
        self.settings.ATTR_A = 1
        self.assertEqual(self.settings.attr_a, 1)
        self.assertEqual(self.settings['attr_a'], 1)

        self.settings.configure(config, override=True)
        self.assertEqual(self.settings.debug, False)
        self.assertEqual(self.settings['debug'], False)
        self.assertEqual(self.settings.attr_a, 1)


if __name__ == '__main__':
    unittest.main()
