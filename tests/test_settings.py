#!/usr/bin/env python
# encoding: utf-8

import unittest


class SettingsTest(unittest.TestCase):

    def test_settings(self):
        from workin.conf import settings
        self.assertEqual(settings.DEBUG, True)
        self.assertEqual(settings['DEBUG'], True)
        settings.ATTR_A = 1
        self.assertEqual(settings.ATTR_A, 1)
        self.assertEqual(settings['ATTR_A'], 1)

        import config
        settings.configure(config)
        self.assertEqual(settings.DEBUG, False)
        self.assertEqual(settings['debug'], False)
        self.assertEqual(settings.ATTR_A, 1)


if __name__ == '__main__':
    unittest.main()
