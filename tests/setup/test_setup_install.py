from redturtle.linkmap import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if redturtle.linkmap is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from redturtle.linkmap.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "1000"

    def test_controlpanel_registered(self, portal):
        actions = portal.portal_actions.controlpanel.listActions()
        action_ids = {action.id for action in actions}
        assert "RedturtleLinkMapSettings" in action_ids
