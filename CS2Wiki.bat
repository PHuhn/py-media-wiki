@REM
@REM NSG.Library.Helpers
 @IF "X%1" == "X" GOTO END
 @SET xml=%1\bin\debug\%1
 @SET out=%xml%_wiki.txt
 @IF EXIST %out% DEL %out%
 gawk -f CS2Wiki.awk %xml%.xml > %out%
 TYPE %out%
:END

