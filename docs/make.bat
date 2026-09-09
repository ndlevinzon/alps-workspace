@ECHO OFF
REM Windows Sphinx build driver (same targets as Makefile).

set SPHINXBUILD=sphinx-build
set SOURCEDIR=.
set BUILDDIR=_build

if "%1"=="" goto help
if "%1"=="apidoc" goto apidoc
if "%1"=="help" goto help

if "%1"=="html" (
    python gen_api.py
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:apidoc
python gen_api.py
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
