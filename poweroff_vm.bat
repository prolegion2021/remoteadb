@echo off
SetLocal EnableExtensions EnableDelayedExpansion
Echo Received name: %*
"C:\Program Files\Genymobile\Genymotion\gmtool.exe" admin stop "%*"
exit
