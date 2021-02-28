lexer grammar MyLex;

Int
    : 'int'
    ;

Return
    : 'return'
    ;


Lparen : '(' ;
Rparen : ')' ;
Lbrace : '{' ;
Rbrace : '}' ;
Semicolon : ';' ;

Punctuator
    : Lparen
    | Rparen
    | Lbrace
    | Rbrace
    | Semicolon
    ;

Plus : '+' ;
Minus : '-' ;
Asterisk : '*' ;
Slash : '/' ;
Percent : '%' ;
Exclamation : '!' ;
Tilde : '~' ;
Ampersand : '&' ;
Langle : '<' ;
Rangle : '>' ;
Langle_eq : '<=' ;
Rangle_eq : '>=' ;
Double_eq : '==' ;
Exclam_eq : '!=' ;
Equal : '=' ;
Double_amp : '&&' ;
Double_bar : '||' ;

Operator
    : Plus
    | Minus
    | Asterisk
    | Slash
    | Percent
    | Exclamation
    | Tilde
    | Ampersand
    | Langle
    | Rangle
    | Langle_eq
    | Rangle_eq
    | Double_eq
    | Exclam_eq
    | Equal
    | Double_amp
    | Double_bar
    ;

Integer
    : Digit+
    ;

Whitespace
    : [ \t\n\r]+ -> skip
    ;

Ident
    : IdentLead WordChar*
    ;

fragment IdentLead: [a-zA-Z_];
fragment WordChar: [0-9a-zA-Z_];
fragment Digit: [0-9];
