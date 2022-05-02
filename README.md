# res publica

A political simulator game that puts you in the shoes of the Bulgarian Prime Minister. 

## Building

Install pygame and pygame_gui:

`pip install numpy`\
`pip install pygame`\
`pip install pygame_gui -U`

Then run `src/main.py` with Python :)

## Deploying

To deploy the game to a single exe file you need
`pip install pyinstaller`

Then run `pyinstaller --onefile src/main.py`. Copy `data` dir to `dist` and open `dist/main.exe`.

