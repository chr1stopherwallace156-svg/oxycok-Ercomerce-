"""OXYCOK-authored VPN session surface for authorized static rehearsal.

This is not NordVPN software. It exists so REA/mission providers can rehearse
a Nord VPN *domain* application against an owned target without inspecting
proprietary NordVPN binaries or bypassing product ownership checks.
"""


class SessionError(Exception):
    """Raised when a session transition is invalid."""


class VpnSession:
    """Bounded in-memory session model with kill-switch and identity checks."""

    def __init__(self, profile_id):
        if not isinstance(profile_id, str) or not profile_id.strip():
            raise SessionError("profile_id required")
        self.profile_id = profile_id.strip()
        self.connected = False
        self.endpoint = None
        self.kill_switch = False

    def connect(self, endpoint):
        if self.connected:
            raise SessionError("already connected")
        if not isinstance(endpoint, str) or not endpoint.strip():
            raise SessionError("endpoint required")
        self.endpoint = endpoint.strip()
        self.connected = True
        return {"status": "connected", "endpoint": self.endpoint}

    def disconnect(self):
        if not self.connected:
            raise SessionError("not connected")
        self.connected = False
        previous = self.endpoint
        self.endpoint = None
        return {"status": "disconnected", "previous_endpoint": previous}

    def set_kill_switch(self, enabled):
        if not isinstance(enabled, bool):
            raise SessionError("kill_switch must be bool")
        self.kill_switch = enabled
        return {"kill_switch": self.kill_switch}

    def status(self):
        return {
            "profile_id": self.profile_id,
            "connected": self.connected,
            "endpoint": self.endpoint,
            "kill_switch": self.kill_switch,
        }
