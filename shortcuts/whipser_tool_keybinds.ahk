#Requires AutoHotkey v2.0
#Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir A_WorkingDir  ; Ensures a consistent starting directory.
#SingleInstance

DetectHiddenWindows 1
SetTitleMatchMode 2

+^!y::{
if (InStr(A_Clipboard, "https://")) {
	Run A_WorkingDir . "\handle_youtube.py - Shortcut.lnk"
} else {
	Tooltip "No URL found in clipboard"
	Sleep 3000
	Tooltip
}
}
