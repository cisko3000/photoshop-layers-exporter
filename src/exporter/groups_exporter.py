import os
from dataclasses import dataclass
from exporter.base import PhotoshopExporterBase


class GroupsExporter(PhotoshopExporterBase):
    bases = [
        'cat', 'dog', 'elf', 'human', 'robot', 'vampire', 'alien',
    ]

    def __init__(self, *args, output_path=None, **kwargs):
        """
        Init.
        """
        super().__init__(*args, **kwargs)
        self._output_path = output_path

    @dataclass
    class Exportable(PhotoshopExporterBase.Exportable):
        kind: str
        part: str

        @property
        def output_file_name(self):
            return f'{self.kind}-{self.part}.png'

    def output_path(self):
        if not os.path.isdir(self._output_path):
            raise ValueError(f'Not a directory: {self._output_path}')
        if not os.path.exists(self._output_path):
            raise ValueError(f'Path does not exist: {self._output_path}')
        return self._output_path

    @property
    def exportables(self):
        for layer in self.layers:
            if layer.kind != 'group':
                continue
            if layer.name in self.bases:
                yield from (self.Exportable(kind=layer.name, part=i.name, layer=i) for i in layer)
            elif layer.name.startswith('orphan-'):
                yield from (self.Exportable(kind=i.name, part=layer.name.split('-')[1], layer=i) for i in layer)
            else:
                pass
                # logging.info(f'Omitting: {layer.name}.')