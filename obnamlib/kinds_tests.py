# Copyright (C) 2008  Lars Wirzenius <liw@liw.fi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import unittest

import obnamlib


class KindsTests(unittest.TestCase):

    def test_is_empty_initially(self):
        kinds = obnamlib.Kinds()
        self.assertEqual(kinds.pairs(), [])

    def test_adds_one_kind_correctl(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        self.assertEqual(kinds.pairs(), [(1, "foo")])

    def test_refuses_to_add_duplicate(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        self.assertRaises(KeyError, kinds.add, 1, "foo")

    def test_refuses_to_add_duplicate_code_with_different_name(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        self.assertRaises(KeyError, kinds.add, 1, "bar")

    def test_refuses_to_add_duplicate_name_with_different_code(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        self.assertRaises(KeyError, kinds.add, 2, "foo")

    def test_adds_mapping_in_both_directions(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        self.assertEqual(kinds.nameof(1), "foo")
        self.assertEqual(kinds.codeof("foo"), 1)

    def test_raises_error_for_unknown_code(self):
        kinds = obnamlib.Kinds()
        self.assertRaises(KeyError, kinds.nameof, 1)

    def test_raises_error_for_unknown_name(self):
        kinds = obnamlib.Kinds()
        self.assertRaises(KeyError, kinds.codeof, "foo")

    def test_adds_identifiers_to_module_namespace(self):
        kinds = obnamlib.Kinds()
        kinds.add(1, "foo")
        kinds.add_identifiers(obnamlib)
        self.assertEqual(obnamlib.foo, 1)