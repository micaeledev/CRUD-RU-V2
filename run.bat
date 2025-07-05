@echo off
echo Iniciando programa...

REM Verificar se o ambiente virtual existe
if not exist .venv (
    echo Ambiente virtual não encontrado! Execute setup.bat primeiro.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Executar programa
python main.py

REM Pausar para ver mensagens de erro se houver
pause