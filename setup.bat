@echo off
echo Configurando ambiente virtual...

REM Criar ambiente virtual se não existir
if not exist .venv (
    echo Criando ambiente virtual...
    python -m venv .venv
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call .venv\Scripts\activate

REM Instalar dependências
echo Instalando dependências...
pip install -r requirements.txt

echo.
echo Ambiente configurado com sucesso!
echo.
echo Para usar o programa:
echo 1. Execute: .venv\Scripts\activate
echo 2. Execute: python main.py
echo 3. Para sair: deactivate
echo.
pause