@echo off
:: �G���[�������ɏ������~
setlocal enabledelayedexpansion
set ERRORLEVEL=0

:: �����`�F�b�N
if "%~1"=="" (
    echo �G���[: dir_name ���w�肵�Ă��������B
    exit /b 1
)
if "%~2"=="" (
    echo �G���[: file_name ���w�肵�Ă��������B
    exit /b 1
)

:: ������ϐ��ɑ��
set "dir_name=%~1"
set "file_name=%~2"

:: �p�b�P�[�W�R�}���h�̎��s
pyxel package "%dir_name%" "%dir_name%\%file_name%.py"
if not !ERRORLEVEL!==0 (
    echo �G���[: pyxel package �R�}���h�����s���܂����B
    exit /b 1
)

:: app2html �R�}���h�̎��s
pyxel app2html "%dir_name%.pyxapp"
if not !ERRORLEVEL!==0 (
    echo �G���[: pyxel app2html �R�}���h�����s���܂����B
    exit /b 1
)

:: �t�@�C���̃��l�[��
if exist "index.html" (
    del "index.html"
)
rename "%dir_name%.html" "index.html"
if not !ERRORLEVEL!==0 (
    echo �G���[: rename �Ɏ��s���܂����B
    exit /b 1
)

:: �e���v���[�g�𔽉f
python reflect_template.py

:: �������b�Z�[�W
echo �������������܂����B
exit /b 0
