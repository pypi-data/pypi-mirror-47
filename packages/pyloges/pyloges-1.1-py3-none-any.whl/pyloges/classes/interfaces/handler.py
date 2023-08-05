# Copyright (C) 2018 Nikita S., Koni Dev Team, All Rights Reserved
# https://github.com/Nekit10/pyloges
#
# This file is part of Pyloges.
#
# Pyloges is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyloges is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyloges.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod


class Handler(ABC):
    """
    Base class for handlers.

    Handler is a class, that process new logs
    """

    @abstractmethod
    def print_log(self, msg: str):
        """Logger pass message of log here"""
        pass

    @abstractmethod
    def save(self):
        """This method saves logs (e.g. to drive)"""
        pass
