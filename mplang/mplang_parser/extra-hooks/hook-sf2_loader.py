from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('sf2_loader')
others = [
    ('sf2_loader\\read_sf2\\__init__.py', 'sf2_loader\\read_sf2'),
    ('sf2_loader\\read_sf2\\fluidsynth.py', 'sf2_loader\\read_sf2'),
    ('sf2_loader\\read_sf2\\read_sf2.py', 'sf2_loader\\read_sf2'),
    ('sf2_loader\\read_sf2_32bit\\__init__.py', 'sf2_loader\\read_sf2_32bit'),
    ('sf2_loader\\read_sf2_32bit\\fluidsynth.py',
     'sf2_loader\\read_sf2_32bit'),
    ('sf2_loader\\read_sf2_32bit\\read_sf2.py', 'sf2_loader\\read_sf2_32bit')
]
datas += others
