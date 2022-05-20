import ply.yacc as yacc
import ply.lex as lex


t_literais = ":|#"

terminais = ['terminal','n_terminal','identificador','linha_identada','num','linha']

terminal = r'"(?:(?:(?!(?<!\)").))"'

n_terminal = r"\w+"

identificador = r"\w+"

num = r"\d+"

linha = r".(\n|$)" novo estado

linha_identada = r"^\t.(\n|$)"

def p_total(p):
        "total : entrada"

def p_total(p):
        "total : total entrada"

def p_entrada(p):
        "entrada : producao "

def p_entrada_1(p):
        "entrada : acao_semantica"

def p_entrada_2(p):
        "entrada : codigo"
        lexer.code += p[1]

def p_entrada_3(p):
        "entrada : comentario"

def p_producao(p):
        "producao : identificador ':' simbolos"

def p_producao_1(p):
        "producao : identificador ':' simbolos '#' linha"

def p_producao_2(p):
        "producao : '|' simbolos"

def p_producao_3(p):
        "producao : '|' simbolos '#' linha"

def p_simbolos(p):
        "simbolos : simbolo"
        p[0] = [p[1]]
        
def p_simbolos_1(p):
        "simbolos : simbolos simbolo"
        p[0] = p[1] + [p[2]]

def p_simbolo(p):
        "simbolo : terminal"
        p[0] = p[1]

def p_simbolo_1(p):
        "simbolo : n_terminal "
        p[0] = p[1]

def p_codigo(p):
        "codigo : ## string"
        p[0] = p[2]

def p_acao_semantica(p):
        "acao_semantica : '#' identificador ':' string"
        if p[2] in t.lexer.act_sem:
                t.lexer.act_sem[t.lexer.aux.group(1)][0] = p[4]
                
        else:
                print("Não existe o " + p[2] + " na gramática")
                t.lexer.error = True


def p_acao_semantica_1(p):
        "acao_semantica : '#' identificador '*' num ':' string"
        if p[2] in t.lexer.act_sem:
                if int(p[4]) < len(t.lexer.act_sem[p[2]]):
                        t.lexer.act_sem[p[2]][p[4]] = p[6]
                else:
                        print("Produção não existe:{}*{}".format(p[2],p[4]))
        else:
                print("Não existe o " + p[2] + " na gramática")
                t.lexer.error = True

def p_string(p):
        "string : linha string_aux"
        p[0] = p[1] + p[2]

def p_string_aux(p):
        "string_aux : linha_identada"
        p[0] = p[1]

def p_string_aux_1(p):
        "string_aux : string_aux linha_identada"
        p[0] = p[1] + p[2]


def t_ANY_error(t):
        #print("Erro:",t)
        t.lexer.skip(1)

def parser_file(file):

        parser = yacc.yacc()

        lexer = lex.lex()
        lexer.prod_name = ""
        lexer.prod_atual = []
        lexer.prods = {}
        lexer.term = [""]
        lexer.axioma = ""
        lexer.act_sem = {}
        lexer.code = ""
        lexer.end_comment = 0
        lexer.error = False

        try:
                fd = open(file,"r")
                for line in fd:
                        lexer.input(line)
                        for token in lexer:
                                pass
                                #print(token)
        except:
                print("Ficheiro não foi encontrado")
                lexer.error = True

        return (lexer.term,lexer.prods,lexer.axioma,lexer.act_sem,lexer.code,lexer.error)