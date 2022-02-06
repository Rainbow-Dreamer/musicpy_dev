from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('sf2_loader')
others = [
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2\\__init__.py',
     'sf2_loader\\read_sf2'),
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2\\fluidsynth.py',
     'sf2_loader\\read_sf2'),
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2\\read_sf2.py',
     'sf2_loader\\read_sf2'),
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2_32bit\\__init__.py',
     'sf2_loader\\read_sf2_32bit'),
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2_32bit\\fluidsynth.py',
     'sf2_loader\\read_sf2_32bit'),
    ('C:\\Users\\andy\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages\\sf2_loader\\read_sf2_32bit\\read_sf2.py',
     'sf2_loader\\read_sf2_32bit')
]
datas += others
