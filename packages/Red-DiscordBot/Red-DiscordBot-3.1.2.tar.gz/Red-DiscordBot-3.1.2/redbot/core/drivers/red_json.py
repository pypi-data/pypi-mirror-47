from pathlib import Path
from typing import Tuple
import copy
import weakref
import logging

from ..json_io import JsonIO

from .red_base import BaseDriver, IdentifierData

__all__ = ["JSON"]


_shared_datastore = {}
_driver_counts = {}
_finalizers = []

log = logging.getLogger("redbot.json_driver")


def finalize_driver(cog_name):
    if cog_name not in _driver_counts:
        return

    _driver_counts[cog_name] -= 1

    if _driver_counts[cog_name] == 0:
        if cog_name in _shared_datastore:
            del _shared_datastore[cog_name]

    for f in _finalizers:
        if not f.alive:
            _finalizers.remove(f)


class JSON(BaseDriver):
    """
    Subclass of :py:class:`.red_base.BaseDriver`.

    .. py:attribute:: file_name

        The name of the file in which to store JSON data.

    .. py:attribute:: data_path

        The path in which to store the file indicated by :py:attr:`file_name`.
    """

    def __init__(
        self,
        cog_name,
        identifier,
        *,
        data_path_override: Path = None,
        file_name_override: str = "settings.json"
    ):
        super().__init__(cog_name, identifier)
        self.file_name = file_name_override
        if data_path_override:
            self.data_path = data_path_override
        else:
            self.data_path = Path.cwd() / "cogs" / ".data" / self.cog_name

        self.data_path.mkdir(parents=True, exist_ok=True)

        self.data_path = self.data_path / self.file_name

        self.jsonIO = JsonIO(self.data_path)

        self._load_data()

    async def has_valid_connection(self) -> bool:
        return True

    @property
    def data(self):
        return _shared_datastore.get(self.cog_name)

    @data.setter
    def data(self, value):
        _shared_datastore[self.cog_name] = value

    def _load_data(self):
        if self.cog_name not in _driver_counts:
            _driver_counts[self.cog_name] = 0
        _driver_counts[self.cog_name] += 1

        _finalizers.append(weakref.finalize(self, finalize_driver, self.cog_name))

        if self.data is not None:
            return

        try:
            self.data = self.jsonIO._load_json()
        except FileNotFoundError:
            self.data = {}
            self.jsonIO._save_json(self.data)

    def migrate_identifier(self, raw_identifier: int):
        if self.unique_cog_identifier in self.data:
            # Data has already been migrated
            return
        poss_identifiers = [str(raw_identifier), str(hash(raw_identifier))]
        for ident in poss_identifiers:
            if ident in self.data:
                self.data[self.unique_cog_identifier] = self.data[ident]
                del self.data[ident]
                self.jsonIO._save_json(self.data)
                break

    async def get(self, identifier_data: IdentifierData):
        partial = self.data
        full_identifiers = identifier_data.to_tuple()
        for i in full_identifiers:
            partial = partial[i]
        return copy.deepcopy(partial)

    async def set(self, identifier_data: IdentifierData, value=None):
        partial = self.data
        full_identifiers = identifier_data.to_tuple()
        for i in full_identifiers[:-1]:
            if i not in partial:
                partial[i] = {}
            partial = partial[i]

        partial[full_identifiers[-1]] = copy.deepcopy(value)
        await self.jsonIO._threadsafe_save_json(self.data)

    async def clear(self, identifier_data: IdentifierData):
        partial = self.data
        full_identifiers = identifier_data.to_tuple()
        try:
            for i in full_identifiers[:-1]:
                partial = partial[i]
            del partial[full_identifiers[-1]]
        except KeyError:
            pass
        else:
            await self.jsonIO._threadsafe_save_json(self.data)

    async def import_data(self, cog_data, custom_group_data):
        def update_write_data(identifier_data: IdentifierData, data):
            partial = self.data
            idents = identifier_data.to_tuple()
            for ident in idents[:-1]:
                if ident not in partial:
                    partial[ident] = {}
                partial = partial[ident]
            partial[idents[-1]] = data

        for category, all_data in cog_data:
            splitted_pkey = self._split_primary_key(category, custom_group_data, all_data)
            for pkey, data in splitted_pkey:
                ident_data = IdentifierData(
                    self.unique_cog_identifier,
                    category,
                    pkey,
                    (),
                    custom_group_data.get(category, {}),
                    is_custom=category in custom_group_data,
                )
                update_write_data(ident_data, data)
        await self.jsonIO._threadsafe_save_json(self.data)

    def get_config_details(self):
        return
