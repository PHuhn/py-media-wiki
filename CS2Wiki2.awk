BEGIN { nmSp=""; sFlg=0; state=""; mstate="";
# state: d=doc, a=assembly, m=members
# mstate: s=summary, p=param, r=returns
}
{
 if( state == "d" ) {
  docState( $0 );
 } else {
  if( state == "a" ) {
   assemblyState( $0 );
  } else {
   if( state == "m" ) {
    membersState( $0 );
   }
  }
 }
 if( $1 == "<doc>" ) {
  state = "d";
 }
}
END { 
}
#
function docState( dStr ) {
 if( $1 == "<assembly>" ) {
  state = "a";
 }
}
#
function assemblyState( aStr ) {
 # <assembly>
 #  <name>NSG.Library.Logger</name>
 # </assembly>
 if( $1 == "<members>" ) {
  state = "m";
 } else {
  if( substr($1,1,6) == "<name>" ) {
   asm = getBetweenTags( $0, "name" );
   nmSp = asm;
   printf( "= Assembly: %s =\n", asm );
  }
 }
}
#
function membersState( aStr ) {
 # mstate: s=summary, p=param, r=returns, c=code
 if( substr($1,1,7) == "<member" ) {
  sFlg=0;
  met =  getBetweenQuotes( $2, 1 );
  if( substr(met,1,2) == "T:" ) {
   mstate = "typ";
   typeName( met );
  }
  if( substr(met,1,2) == "M:" ) {
   mstate = "mem";
   methodName( met );
  }
  if( substr(met,1,2) == "P:" ) {
   propertyName( met );
  }
 } else {
  if( ($1 == "</member>" || $1 == "</param>" || $1 == "</returns>") && NF ==1 ) {
   return;
  }
  if( $1 == "<summary>" ) {
   sFlg=1;
   return;
  } else {
   if( $1 == "</summary>" ) {
    sFlg=0;
    return;
   } else {
    if( sFlg == 1 ) {
     sub(/^            /, ""); # rtrim
     print $0;
     return;
    }
   }
   setState( );
   if( mstate == "par" ) {
    paramState( $0 );
   } else {
    if( mstate == "ret" ) {
     returnsState( $0 );
    }
   }
  }
 }
}
#
function typeName( tstr ) {
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
 if( mstate != "prop" ) {
  printf( "=== Properties ===\n" );
  mstate = "prop";
 }
 len = split( pstr, typ, "." );
 printf( "==== %s ====\n", typ[len] );
}
#
function methodName( mStr ) {
 # <member name="M:NSG.Foo.Bar(System.String)">
 if( nmSp != "" ) {
  mStr = substr( mStr,4 + length( nmSp ) );
 } else {
  mStr = substr( mStr,3 );
 }
 # horizontal rule
 printf( "\n\n----\n\n\n=== %s ===\n", mStr );
}
#
function paramState( pStr ) {
 # <param name="fullFilePathAndName">full path and file name</param>
 if( ( substr($1,1,2) == "</" ) && NF == 1 ) {
  return;
 }
 if( $1 == "<param" ) {
  pNam = getBetweenQuotes( $0, 1 );
  printf( "===== %s =====\n", pNam );
  parStr = getBetweenTags( $0, "param" );
 } else {
  parStr = $0;
  sub(/^            /, "", parStr); # rtrim
 }
 print parStr;
}
#
function returnsState( rStr ) {
 # <returns>string of prefix followed by GUID and extent</returns>
 if( ( $1 == "<returns>" || $1 == "</returns>" ) && NF == 1 ) {
  return;
 }
 if( ( substr($1,1,2) == "</" ) && NF == 1 ) {
  return;
 }
 if( substr($1,1,9) == "<returns>" ) {
  retStr = getBetweenTags( $0, "returns" );
 } else {
  retStr = $0;
 }
 print retStr;
}
#
function setState( ) {
 if( $1 == "<param" ) {
  if( mstate != "par" ) {
   printf( "\n==== Parameters ====\n" );
   mstate = "par";
  }
 } else {
  if( substr( $1, 1, 9) == "<returns>" ) {
   if( mstate != "ret" ) {
    printf( "\n==== Return Value ====\n" );
    mstate = "ret";
   }
  }
 }
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
