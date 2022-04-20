from ply import lex

tokens = ["TERM","NORMAL","PROD","FUNC","CODE","COMMENT","END"]

states = [("prod","exclusive"),("prodfunc","exclusive"),("func","exclusive"),("code","exclusive"),("comment","exclusive")]

def t_NORMAL(t):
	r"\w+"
	print("default normal")

def t_prod_NORMAL(t):
	r"\w+"
	print("prod normal")

def t_prodfunc_NORMAL(t):
	r".+\n"
	t.lexer.begin("prod")

def t_func_NORMAL(t):
	r".+"

def t_func_END(t):
	r"^\n"
	t.lexer.begin("INITIAL")

def t_PROD(t):
	r":"
	t.lexer.begin("prod")

def t_prod_PROD(t):
	r"|"

def t_prod_TERM(t):
	r'".*"'
	print("prod term")

def t_prod_FUNC(t):
	r"#"
	t.lexer.begin("func_prod")

def t_CODE(t):
	r"##"
	t.lexer.begin("code")

def t_code_NORMAL(t):
	r".+"
	print("code normal")

def t_code_END(t):
	r"^\n"

def t_COMMENT(t):
	r"'''"
	t.lexer.begin("comment")

t_comment_NORMAL = r".+"

def t_comment_END(t):
	r"'''"
	t.lexer.begin("INITIAL")