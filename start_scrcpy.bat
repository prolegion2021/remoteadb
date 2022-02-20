@echo off
SetLocal EnableExtensions EnableDelayedExpansion
Echo Received name: %*
"C:\Python\sc_cmd\prog\scrcpy.exe" -s %* -Sw --max-fps 15
exit
