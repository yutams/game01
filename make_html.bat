@echo off
:: エラー発生時に処理を停止
setlocal enabledelayedexpansion
set ERRORLEVEL=0

:: 引数チェック
if "%~1"=="" (
    echo エラー: dir_name を指定してください。
    exit /b 1
)
if "%~2"=="" (
    echo エラー: file_name を指定してください。
    exit /b 1
)

:: 引数を変数に代入
set "dir_name=%~1"
set "file_name=%~2"

:: パッケージコマンドの実行
pyxel package "%dir_name%" "%dir_name%\%file_name%.py"
if not !ERRORLEVEL!==0 (
    echo エラー: pyxel package コマンドが失敗しました。
    exit /b 1
)

:: app2html コマンドの実行
pyxel app2html "%dir_name%.pyxapp"
if not !ERRORLEVEL!==0 (
    echo エラー: pyxel app2html コマンドが失敗しました。
    exit /b 1
)

:: ファイルのリネーム
if exist "index.html" (
    del "index.html"
)
rename "%dir_name%.html" "index.html"
if not !ERRORLEVEL!==0 (
    echo エラー: rename に失敗しました。
    exit /b 1
)

:: テンプレートを反映
python reflect_template.py

:: 完了メッセージ
echo 処理が完了しました。
exit /b 0
