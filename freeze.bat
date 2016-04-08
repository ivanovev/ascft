@echo off
Setlocal EnableDelayedExpansion
set name=ascft
set srcdir=C:\Share\start
set srctgz="%srcdir%\%name%.tgz"
set srctar=%name%.tar
set s7z="C:\Program Files\7-Zip\7z.exe"
set cxfreeze="C:\Python34\Scripts\cxfreeze.bat"

rem rmdir /S /Q freeze
rem del "%srcdir%\*.7z"

rem %s7z% x "%srctgz%" -ofreeze
rem cd freeze
rem %s7z% x "%srctar%"

cmd /C %cxfreeze% ascft.py --target-dir=ascft
copy ascft.bat ascft/ascft.bat
del /F "%srcdir%\ascft.7z"
cd ascft
%s7z% a "%srcdir%\ascft.7z" *
cd ..
pause
