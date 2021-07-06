rem @echo off
setlocal EnableDelayedExpansion

rem Get Python major and minor version
for /f %%i in ('python -c "import sys; print(sys.version_info.major)"') do set python_version_major=%%i
for /f %%i in ('python -c "import sys; print(sys.version_info.minor)"') do set python_version_minor=%%i

rem Concatenate major and minor versions
set python_version="%python_version_major%%python_version_minor%"

rem Platform
set platform="win"

rem Directory at which wheel files are located
set root_dir=%CD%\dist

rem flag if any of the wheels are installed
set wheel_installed=false

rem Iterate through all wheel files in /dist/* directory.
for /R %root_dir% %%i in (*.whl) do (
    
    rem Check if wheel filename matches python version
    	echo %%i | findstr /C:"%python_version%">nul && (
	    	set python_version_matched=true
	) || (
		set python_version_matched=false
	)

	rem Check if wheel filename matches platform
    	echo %%i | findstr /C:"%platform%">nul && (
	    	set platform_matched=true
	) || (
		set platform_matched=false
	)

	rem Install wheel if python version and platform matched
	if "!wheel_installed!"=="false" (
		if "!python_version_matched!"=="true" (
			if "!platform_matched!"=="true" (

				echo Try installing %%i for python version %python_version%
                rem python -m pip install --upgrade pip
                python -m pip install --force-reinstall %%i --verbose

				rem Check last error
				if errorlevel==0 (
					set wheel_installed=true
					echo Wheel installed successfully.
					goto :break
				)
			)
		)
	)
)

rem Check if any of the wheels in \dist\* could be installed
:break
if "!wheel_installed!"=="false" (
	echo No wheel could be installed.
	exit /b 1
)
