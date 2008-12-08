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


import obnamlib


class BackupCommand(object):

    """A sub-command for the command line interface to back up some data."""

    PART_SIZE = 256 * 1024

    def backup_new_file(self, relative_path):
        """Back up a completely new file."""
        content = self.store.new_object(kind=obnamlib.FILECONTENTS)
        f = self.fs.open(relative_path, "r")
        while True:
            data = f.read(self.PART_SIZE)
            if not data:
                break
            part = self.store.new_object(kind=obnamlib.FILEPART)
            part.data = data
            self.store.put_object(part)
            content.add(part.id)
        f.close()
        self.store.put_object(content)
        return content

    def backup_new_files_as_groups(self, relative_paths):
        """Back a set of new files as a new FILEGROUP."""
        fg = self.store.new_object(kind=obnamlib.FILEGROUP)
        for path in relative_paths:
            fc = self.backup_new_file(path)
            file_component = obnamlib.Component(kind=obnamlib.FILE)
            file_component.children += [
                obnamlib.Component(kind=obnamlib.FILENAME, string=path),
                obnamlib.Component(kind=obnamlib.CONTREF, string=fc.id),
                ]
            fg.components.append(file_component)
        self.store.put_object(fg)
        return [fg]

    def backup_dir(self, relative_path, subdirs, filenames):
        """Back up a single directory, non-recursively.

        subdirs is a list of obnamlib.Dir objects for the direct
        subdirectories of the target directory. They must have been
        backed up already.

        """

        dir = self.store.new_object(obnamlib.DIR)
        dir.name = relative_path
        dir.dirrefs = [x.id for x in subdirs]
        if filenames:
            dir.fgrefs = [x.id 
                          for x in self.backup_new_files_as_groups(filenames)]
        else:
            dir.fgrefs = []
        self.store.put_object(dir)
        return dir

    def __call__(self, config, args): # pragma: no cover
        # This is here just so I can play around with things on the
        # command line. It will be replaced with the real stuff later.
        store_url = args[0]
        roots = args[1:]

        self.store = obnamlib.Store(store_url, "w")
        self.fs = obnamlib.LocalFS(".")

        self.backup_new_files_as_group(roots)
        self.store.commit()

        print "backup"
