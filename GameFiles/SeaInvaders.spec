# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os, pygame_gui
pygame_data_loc = os.path.join(os.path.dirname(pygame_gui.__file__), 'data')
a = Analysis(['SeaInvaders.py'],
             pathex=['/Users/laurens/Coding/Python_Projects/SeaInvaders/GameFiles'],
             binaries=[],
             datas=[('data/*', 'data'), ('Images/*', 'Images'), (pygame_data_loc, "pygame_gui/data")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='SeaInvaders',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
app = BUNDLE(exe,
             name='SeaInvaders.app',
             icon=None,
             bundle_identifier=None)
