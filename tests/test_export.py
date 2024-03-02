import os
import pytest

from exporter.base import PhotoshopExporterBase


@pytest.fixture
def input_path():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'input',
        'test_file.psd',
    )


@pytest.fixture
def output_path():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'output',
    )


@pytest.fixture
def expected_output_file_names():
    return [
        f'Layer {i}.png' for i in range(1, 5)
    ]


@pytest.fixture
def output_path_cleanup(output_path, expected_output_file_names):
    yield
    for output_file in expected_output_file_names:
        try:
            os.remove(output_file)
        except Exception:
            pass

class TestExport:

    def test_export_layers(self, input_path, output_path, expected_output_file_names):
        exporter = PhotoshopExporterBase(input_path, output_path=output_path)
        exporter.export()
        files = set(f for f in os.listdir(output_path) if '.png' in f)
        assert files == set(expected_output_file_names)
