# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/ui/components', 'src/ui/components'),
        ('src/ui', 'src/ui'),
        ('src/simulador', 'src/simulador'),
        ('src/data', 'src/data'),
        ('src/utils', 'src/utils'),
    ],
    hiddenimports=[
        'src.ui.main_window',
        'src.ui.components.file_loader',
        'src.ui.components.policy_selector',
        'src.ui.components.parameter_input',
        'src.ui.components.simulation_controls',
        'src.ui.components.results_tab',
        'src.ui.components.gantt_tab',
        'src.ui.components.stats_tab',
        'customtkinter',
        'matplotlib',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Simulador_Planificacion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
