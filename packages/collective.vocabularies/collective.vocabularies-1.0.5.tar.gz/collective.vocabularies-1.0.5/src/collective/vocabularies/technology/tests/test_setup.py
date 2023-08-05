# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.vocabularies.technology.testing import COLLECTIVE_VOCABULARIES_TECHNOLOGY_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.vocabularies.technology is properly installed."""

    layer = COLLECTIVE_VOCABULARIES_TECHNOLOGY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.vocabularies.technology is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.vocabularies.technology'))

    def test_browserlayer(self):
        """Test that ICollectiveVocabulariesTechnologyLayer is registered."""
        from collective.vocabularies.technology.interfaces import (
            ICollectiveVocabulariesTechnologyLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveVocabulariesTechnologyLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_VOCABULARIES_TECHNOLOGY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.vocabularies.technology'])

    def test_product_uninstalled(self):
        """Test if collective.vocabularies.technology is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.vocabularies.technology'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveVocabulariesTechnologyLayer is removed."""
        from collective.vocabularies.technology.interfaces import ICollectiveVocabulariesTechnologyLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveVocabulariesTechnologyLayer, utils.registered_layers())
