# Ophardt File Export Reader

Allows python to interact with [Ophardt](https://fencing.ophardt.online/de/home) file exports

## Usage

```python
from ophardtImport import OphardtImporter
import zipfile

o = OphardtImporter(zipfile.ZipFile('export.zip'))
data = o.get_data()

print(data['fencers'])
```

## File structure

The export is one zip file with the following structure:

```
\
├── {Export ID}.pdf => no used (notice about the tournament)
├── UE{Export ID}.csv => contains information about the tournaments
├── XML => xml formated information about the tournaments
│   ├── XMLstd{Tournament ID}.xml => one file per tournament
│   └── national
│       └── XMLnat{Tournament ID}.xml => one file per tournament
├── csv => csv formated information about the tournaments
│   └── OH{Tournament ID}.csv => one file per tournament
└── pictures => pictures of the participants
    └── F{Fencer ID}.jpg => jpg 480x640px
```

## Credits
GPLv3 Markdown Version from [TheFox](https://github.com/TheFox/GPLv3.md)