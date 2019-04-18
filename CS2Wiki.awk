BEGIN { nmSp=""; aFlg=0; sFlg=0; propFlg=0; pFlg=0; rFlg=0;
}
{
 if( ($1 == "</member>" || $1 == "</param>" ) && NF ==1 ) {
  next;
 }
 if( aFlg == 1 ) {
  if( $1 == "</assembly>" ) {
   aFlg = 0;
  } else {
   assemblyName( $0 );
  }
 }
 if( $1 == "<assembly>" ) {
  aFlg = 1;
 }
 if( $1 == "<member" ) {
  sFlg=0; pFlg=0; rFlg = 0;
  met = getBetweenQuotes( $2, 1 );
  if( substr(met,1,2) == "T:" ) {
   typeName( met );
  }
  if( substr(met,1,2) == "M:" ) {
   methodName( met );
  }
  if( substr(met,1,2) == "P:" ) {
   propertyName( met );
  }
 } else {
  if( $1 == "<summary>" ) { sFlg=1;
  } else {
   if( $1 == "</summary>" ) { sFlg=0;
   } else {
    if( sFlg == 1 ) {
     sub(/^            /, ""); # rtrim
     print $0;
    }
    if( substr($1,1,9) == "<returns>" || rFlg == 1 ) {
     returnsName( $0 );
    }
    if( $1 == "<param" || pFlg == 1 ) {
     paramName( $0 );
    }
   }
  }
 }
}
END { 
}
#
function assemblyName( aStr ) {
 # <assembly>
 #  <name>NSG.Library.Logger</name>
 # </assembly>
 if( substr($1,1,6) == "<name>" ) {
  asm = getBetweenTags( $0, "name" );
  nmSp = asm;
  printf( "= Assembly: %s =\n", asm );
 }
}
#
function typeName( tstr ) {
 propFlg = 0;
 pFlg = 0; # turn off param
 len = split( tstr, typ, "." );
 if ( typ[len] == "NamespaceDoc" ) {
  nmSp = substr( tstr,3 );
  gsub( /.NamespaceDoc/, "", nmSp );
  printf( "= Namespace: %s =\n", nmSp );
 } else {
  printf( "== Class: %s ==\n", typ[len] );
 }
}
#
function propertyName( pstr ) {
 # <member name="P:NSG.Library.Logger.ILogData.Id">
 #  <summary>
 #   The id/key of the log record.
 #  </summary>
 # </member>
 pFlg = 0; # turn off param
 if( propFlg == 0 ) {
  printf( "=== Properties ===\n" );
  propFlg = 1;
 }
 len = split( pstr, typ, "." );
 printf( "==== %s ====\n", typ[len] );
}
#
function methodName( mStr ) {
 # <member name="M:NSG.Foo.Bar(System.String)">
 propFlg = 0;
 pFlg = 0; # turn off param
 mStr = substr( mStr,4 + length( nmSp ) );
 # horizontal rule
 printf( "\n\n----\n\n\n=== %s ===\n", mStr );
}
#
function paramName( pStr ) {
 # <param name="fullFilePathAndName">full path and file name</param>
 propFlg = 0;
 if( pFlg == 0 ) {
  printf( "\n==== Parameters ====\n" );
  pFlg = 1;
 }
 if( $1 == "<param" ) {
  pNam = getBetweenQuotes( $0, 1 );
  printf( "===== %s =====\n", pNam );
  parStr = getBetweenTags( $0, "param" );
 } else {
  sub(/^            /, ""); # rtrim
  parStr = $0;
 }
 idx = index( parStr, "</param>" );
 if( idx > 0 ) {
  parStr = substr( parStr, 1, idx-1 );
 }
 print parStr;
}
#
function returnsName( rStr ) {
 # <returns>string of prefix followed by GUID and extent</returns>
 if( rFlg == 0 ) {
  printf( "\n==== Return Value ====\n" );
  pFlg = 0; # turn off param
  rFlg = 1; # turn on return
 }
 if( $1 == "<returns>" && NF == 1 ) {
  rFlg=1;
  return;
 }
 if( $1 == "</returns>" ) {
  rFlg=0;
  return;
 }
 if( substr($1,1,9) == "<returns>" ) {
  retStr = getBetweenTags( $0, "returns" );
 } else {
  retStr = $0;
 }
 idx = index( retStr, "</returns>" );
 if( idx > 0 ) {
  rFlg=0;
  retStr = substr( retStr, 1, idx-1 );
 }
 print retStr;
}
# - utilities ------
# Between tags
function getBetweenTags( inp, tagName ) {
 betwn = inp;
 sub(/^ +/, "", betwn); # rtrim
 tag = "<" tagName;
 if( substr(betwn,1,length(tag)) == tag ) {
  pos = index( inp, ">" );
  if( pos > 0 ) {
   betwn = substr( inp, pos +1 );
  }
 }
 # end tag
 tag = "</" tagName ">";
 pos = index( betwn, tag );
 if( pos > 0 ) {
  betwn = substr( betwn, 1, pos -1 );
 }
 return betwn;
}
# Between double quotes
function getBetweenQuotes( inp, cnt ) {
 betwn = "";
 idx = cnt * 2;
 len = split( inp, qts, "\"" );
 if( len >= idx ) {
  betwn = qts[ idx ];
 }
 return betwn;
}
# --- end-of-file ---
