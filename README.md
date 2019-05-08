# py-media-wiki
## Overview
Convert .Net XML comment files to mediawika documentations as follows:
- A python script to convert 95% to mediawiki (cs2media_wiki.py),
- An AWK script to convert 70% to mediawiki(CS2Wiki.awk).

### cs2media_wiki.py
To execute from the command line, converting Library.xml as follows:
```
    python cs2media_wiki.py Library.xml > library.md.txt
```
Make sure the text is flush left except for code.  Code is indented two spaces. This script processes the comments as an XML document.

#### Note
The python code was created in Visual Studio.

### CS2Wiki.awk
To execute from the batch file, converting Library.xml as follows:
```
    CS2Wiki Library
```
Make sure the text is flush left except for code.  Code is indented two spaces.This script processes the comments as a text document.

### Wiki
These Wiki pages were initialy created by the CS2Wiki.awk scripts with the library's XML file, and again regenerated with cs2media_wiki.py. The cs2media_wiki.py script got me 95% of the way to creating the MediaWiki file.  Make sure the text is flush left except for code (which should be indented 2 spaces). In one, I replaced all &#96;&#96;1 and {&#96;&#96;0} with &#38;lt;T&#38;gt;

Check these Wiki pages for examples:

- [NSG.Library.Helpers](https://github.com/PHuhn/NSG.Library/wiki/NSG.Library.Helpers),
- [NSG.Library.Logger](https://github.com/PHuhn/NSG.Library/wiki/NSG.Library.Logger),
- [NSG.Library.EMail](https://github.com/PHuhn/NSG.Library/wiki/NSG.Library.EMail),
- [NSG.PrimeNG](https://github.com/PHuhn/NSG.PrimeNG/wiki).

