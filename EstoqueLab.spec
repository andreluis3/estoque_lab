# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main_original.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Todos os assets da interface
        ('inventario/ui/assets/*', 'inventario/ui/assets'),

        # Banco
        ('inventario/database/estoque.db', 'inventario/database'),

        # Configuração
        ('inventario/config/config.json', 'inventario/config'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='EstoqueLab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

    # Ícone do arquivo EXE
    icon='inventario/ui/assets/logo.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='EstoqueLab 1.0',
)