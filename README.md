# photoshop-layers-exporter
Photoshop Layers Exporter

A library for exporting layers from a PSD file. The exported layers will be saved as PNGs.


# How to use

`python src/main_export.py --path /data/psd_files --output /output/assets`

The `--path` argument can be a folder or PSD file. If it's a folder, the exporter will export layers from all the PSD files in that folder (1 level deep only).

The `--output` argument is where the PNGs will be saved. Any existing files will be overwritten.