# -*- mode: python -*-

import os

MODULE = 'examples\\get_pitch.py'
FFMPEG_BIN = 'ffmpeg.exe'
FFMPEG_DIR = 'C:\\ffmpeg\\bin\\'
KERAS_MODEL = 'keras\\keras_tf_1025_240_120_12_fft_0.model'
block_cipher = None


a = Analysis([MODULE],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[],
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
          a.binaries + [(FFMPEG_BIN,os.path.join(FFMPEG_DIR,FFMPEG_BIN), 'BINARY')],
          a.zipfiles,
          a.datas + [(KERAS_MODEL, 'KERAS')],
          [],
          name='ultrastar_pitch',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True)
