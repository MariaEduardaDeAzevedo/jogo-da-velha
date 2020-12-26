from cx_Freeze import setup, Executable
 
setup(name='jogo-da-velha',
    version='1.0',
    description='Jogue Jogo da Velha com o seu computador!',
    options={'build_exe': {'packages': ['pygame']}},
    executables = [Executable(
                   script='main.py',
                   base=None,
                   icon='assets/icon.ico'
                   )
            ]
)