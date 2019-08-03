set mypath=%~dp0
set reqFile=%mypath%requirements.txt
pip install --upgrade -r %reqFile%

pause