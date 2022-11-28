from fLoxToken import Token
from fLoxTokenTypes import TokenType
import fLox

keywords={
    'and':TokenType.AND,
    'class':TokenType.CLASS,
    'else':TokenType.ELSE,
    'false':TokenType.FALSE,
    'for':TokenType.FOR,
    'fun':TokenType.FUN,
    'if':TokenType.IF,
    'nil':TokenType.NIL,
    'or':TokenType.OR,
    'print':TokenType.PRINT,
    'return':TokenType.RETURN,
    'super':TokenType.SUPER,
    'this':TokenType.THIS,
    'true':TokenType.TRUE,
    'var':TokenType.VAR,
    'while':TokenType.WHILE
}

class Scanner(object):
    def __init__(self, source:str):
        super().__init__()
        self.source=source
        self.tokens=list()
        self.start=0
        self.current=0
        self.line=1

    def scanToken(self):
        c=self.advance()
        if c=='(':
            self.addToken(TokenType.LEFT_PAREN)
        elif c==')':
            self.addToken(TokenType.RIGHT_PAREN)
        elif c=='{':
            self.addToken(TokenType.LEFT_BRACE)
        elif c=='}':
            self.addToken(TokenType.RIGHT_BRACE)
        elif c==',':
            self.addToken(TokenType.COMMA)
        elif c=='.':
            self.addToken(TokenType.DOT)
        elif c=='-':
            self.addToken(TokenType.MINUS)
        elif c=='+':
            self.addToken(TokenType.PLUS)
        elif c==';':
            self.addToken(TokenType.SEMICOLON)
        elif c=='*':
            self.addToken(TokenType.STAR)
        
        elif c=="!":
            if self.match('='):
                self.addToken(TokenType.BANG_EQUAL)
            else:
                self.addToken(TokenType.BANG)
        elif c=='=':
            if self.match('='):
                self.addToken(TokenType.LESS_EQUAL)
            else:
                self.addToken(TokenType.EQUAL)
        elif c=='<':
            if self.match('='):
                self.addToken(TokenType.LESS_EQUAL)
            else:
                self.addToken(TokenType.LESS)
        elif c=='>':
            if self.match('='):
                self.addToken(TokenType.GREATER_EQUAL)
            else:
                self.addToken(TokenType.GREATER)
        elif c=='/':
            if self.match('/'): 
                while self.peek()!='\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType.SLASH)
        elif c in [' ','\r','\t']:
            pass
        elif c=='\n':
            self.line+=1
            pass
        
        
        elif c=='"':
            self.string() 
        
        else:
            if self.isDigit(c):
                self.number()
            elif self.isAlpha(c):
                self.identifier()
            else:
                fLox.FLOX.error(self.line,"Unexpecterd Character.")
                
   
    def match(self,expected:str)->bool:
        if self.isAtEnd():
            return False
        if self.source[self.current]!=expected:
            return False
        self.current+=1
        return True

    def isAtEnd(self)->bool:
        return self.current>=len(self.source)

    def advance(self)->str:
        self.current+=1
        return self.source[self.current-1]

    
    def peek(self)->str:
        if self.isAtEnd():
            return '\0'
        else:
            return self.source[self.current]


    def peekNext(self)->str:
        if self.current+1>=len(self.source):
            return '\0'
        return self.source[self.current+1]

    def string(self):
        while self.peek()!='"' and not self.isAtEnd():
            if self.peek()=='\n':
                self.line+=1
            self.advance()
        
        if self.isAtEnd():
             fLox.FLOX.error(self.line,"Unterminated string.")
             return
        self.advance()
        value=self.source[self.start+1:self.current-1] 
        self.addToken(TokenType.STRING,value)

    def isDigit(self,c:str)->bool:
        return c>='0' and c<='9'

    def isAlpha(self,c:str)->bool:
        return (c>='a' and c<='z') or (c>='A' and c<='Z') or c=='_'

    def isAlphaNumeric(self,c:str)->bool:
        return self.isAlpha(c) or self.isDigit(c)

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek()=='.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        self.addToken(TokenType.NUMBER,float(self.source[self.start:self.current]))
    

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text=self.source[self.start:self.current]
        type=keywords.get(text)
        if type is None:
            type=TokenType.IDENTIFIER
        self.addToken(type)

    def scanTokens(self)->list:
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return self.tokens

    
    def addToken(self,type:TokenType,literal=None):
        text=self.source[self.start:self.current]
        self.tokens.append(Token(type,text,literal,self.line))
