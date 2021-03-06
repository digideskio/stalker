# -*- coding: utf-8 -*-
# Stalker a Production Asset Management System
# Copyright (C) 2009-2016 Erkan Ozgur Yilmaz
#
# This file is part of Stalker.
#
# Stalker is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
#
# Stalker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with Stalker.  If not, see <http://www.gnu.org/licenses/>

import unittest
from stalker import ClientUser


class ClientUserTestCase(unittest.TestCase):
    """tests for ClientUser class
    """

    def test_role_argument_is_not_a_role_instance(self):
        """testing if a TypeError will be raised when the role argument is not
        a Role instance
        """
        from stalker import Client, User

        with self.assertRaises(TypeError) as cm:
            client_user = ClientUser(
                client=Client(name='Test Client'),
                user=User(
                    name='Test User',
                    login='tuser',
                    email='u@u.com',
                    password='secret'
                ),
                role='not a role instance'
            )

        self.assertEqual(
            str(cm.exception),
            'ClientUser.role should be a stalker.models.auth.Role instance, '
            'not str'
        )
