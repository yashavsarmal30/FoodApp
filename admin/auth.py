import os
from typing import Optional, Dict
import hashlib

class AdminAuth:
    def __init__(self):
        self.admin_credentials = {
            'username': 'admin',
            'password': self._hash_password('admin')
        }

    def _hash_password(self, password: str) -> str:
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate admin user"""
        return (username == self.admin_credentials['username'] and 
                self._hash_password(password) == self.admin_credentials['password'])

    def change_password(self, current_password: str, new_password: str) -> bool:
        """Change admin password"""
        if self._hash_password(current_password) == self.admin_credentials['password']:
            self.admin_credentials['password'] = self._hash_password(new_password)
            return True
        return False

# Create a singleton instance
admin_auth = AdminAuth() 