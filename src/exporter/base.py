import os
import logging
import typing

from dataclasses import dataclass
from psd_tools import PSDImage
from PIL import Image
from cached_property import cached_property


class PhotoshopExporterBase:
    """
    Exports layers from all photoshop files in some folder.
    """

    def __init__(self, input_path,  *,  output_path=None, verbose=None, **kwargs):
        """
        Init.
        """
        self.input_path = input_path
        self._output_path = output_path

    @dataclass
    class Exportable:
        layer: typing.Any

        @property
        def output_file_name(self):
            return f'{self.layer.name}.png'

    @cached_property
    def output_path(self):
        """
        Output path.

        The export path.
        """
        if self._output_path is not None:
            return self._output_path
        if os.path.isdir(self.input_path):
            return os.path.join(self.input_path, 'exports')
        return os.path.join(os.path.dirname(self.input_path), 'exports')

    @cached_property
    def psd_files(self):
        """
        PSD files.

        The files that are found by the exporter.
        """
        paths = []
        logging.info(f'Scanning {self.input_path}')
        if os.path.isfile(self.input_path):
            paths = [self.input_path]
        elif os.path.isdir(self.input_path):
            filesInDir = [
                os.path.join(self.input_path, f) for f in os.listdir(self.input_path)
                if os.path.isfile(os.path.join(self.input_path, f))
            ]
            paths = [f for f in filesInDir if f.endswith('.psd')]
        logging.info(f'Found {len(paths)} files:%s')
        logging.info('\n\t'.join(paths))
        return paths

    @cached_property
    def image_size(self):
        psd = PSDImage.open(self.psd_files[0])
        image = psd.composite()
        size = image.size
        # psd.close()
        return size

    def export(self):
        """
        Export all the discovered layers to the output path.
        """
        if len(self.psd_files) == 0:
            logging.error(f"Couldn't find any PSD files in {self.input_path}.")
            return

        for x in self.exportables:
            save_path = os.path.join(self.output_path, x.output_file_name)
            save_path = os.path.normpath(save_path)
            original_pil = x.layer.topil()
            if original_pil is None:
                continue
            save_image = Image.new(original_pil.mode, self.image_size, "#00000000")
            save_image.paste(original_pil, x.layer.bbox)
            # save_image.paste(original_pil, x.layer.viewbox)
            save_image.save(save_path)
            logging.info("Layer saved as %s", x.output_file_name)
        print(f'Saved to {self.output_path}.')

    @property
    def layers(self):
        for psd_file_path in self.psd_files:
            yield from (PSDImage.open(psd_file_path))

    @property
    def exportables(self):
        yield from (self.Exportable(layer=layer) for layer in self.layers)
