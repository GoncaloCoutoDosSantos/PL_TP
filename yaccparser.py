import ply.yacc as yacc
from lexer import tokens

def p_axioma(p):
        "z : total"
        pass

def p_total(p):
        "total : entrada"
        print("total")
        pass

def p_total1(p):
        "total : total entrada"
        print("total1")
        pass

def p_entrada(p):
        "entrada : producao "
        print("entrada p")
        name,prod,ac_sem = p[1]
        if (p.parser.axioma == ""):
                p.parser.axioma = name
        if(name in p.parser.prods): 
                p.parser.prods[name].append(prod)
                p.parser.act_sem[name].append(ac_sem)
        else: 
                p.parser.prods[name] = [prod]
                p.parser.act_sem[name] = [ac_sem]

def p_entrada_1(p):
        "entrada : acao_semantica"
        print("entrada a")
        pass

def p_entrada_2(p):
        "entrada : codigo"
        print("entrada c")
        p.parser.code += p[1]

def p_producao(p):
        "producao : identificador DOTS simbolos"
        print("produçao 1")
        p[0] = (p[1],p[3],"")
        p.parser.prod_name = p[1]

def p_producao_1(p):
        "producao : identificador DOTS simbolos CARD LINHA"
        print("produçao 2")
        p[0] = (p[1],p[3],p[5])
        p.parser.prod_name = p[1]

def p_producao_2(p):
        "producao : BAR simbolos"
        print("produçao 3")
        if (p.parser.prod_name == ""): 
                p.parser.error = True
        p[0] = (p.parser.prod_name,p[2],"")

def p_producao_3(p):
        "producao : BAR simbolos CARD LINHA"
        print("produçao 4")
        if (p.parser.prod_name == ""): 
                p.parser.error = True
        p[0] = (p.parser.prod_name,p[2],p[4])

def p_simbolos(p):
        "simbolos : simbolo"
        print("simbolos")
        p[0] = [p[1]]
        
def p_simbolos_1(p):
        "simbolos : simbolos simbolo"
        print("simbolos 1")
        p[0] = p[1] + [p[2]]

def p_simbolo(p):
        "simbolo : TERMINAL"
        print("TERMINAL")
        if not(p[1] in p.parser.term) and p[1] != '""':
                p.parser.term.append(p[1])
        elif p[1] == '""':
                p[1] = None
        p[0] = p[1]

def p_simbolo_1(p):
        "simbolo : n_terminal"
        print("N TERMINAL")
        p[0] = p[1]

def p_codigo(p):
        "codigo : CODE string"
        print("Codigo")
        p[0] = p[2]

def p_acao_semantica(p):
        "acao_semantica : CARDI identificador BAR string"
        print("act_sem 1")
        if p[2] in p.parser.act_sem:
                p.parser.act_sem[p[2]][0] = p[4]
                
        else:
                print("Não existe o " + p[2] + " na gramática")
                p.parser.error = True


def p_acao_semantica_1(p):
        "acao_semantica : CARDI identificador AST NUM BAR string"
        print("act_sem 2")
        if p[2] in p.parser.act_sem:
                if int(p[4]) < len(p.parser.act_sem[p[2]]):
                        p.parser.act_sem[p[2]][p[4]] = p[6]
                else:
                        print("Produção não existe:{}*{}".format(p[2],p[4]))
        else:
                print("Não existe o " + p[2] + " na gramática")
                p.parser.error = True

def p_string(p):
        "string : LINHA string_aux"
        print("string")
        p[0] = p[1] + p[2]

def p_string_aux(p):
        "string_aux : LINHAIDENTADA"
        print("string aux 1")
        p[0] = p[1]

def p_string_aux_1(p):
        "string_aux : string_aux LINHAIDENTADA"
        print("string aux 2")
        p[0] = p[1] + p[2]

def p_identificador(p):
        "identificador : PAL"
        print("identificador")
        p[0] = p[1]

def p_n_terminal(p):
        "n_terminal : PAL"
        print("n terminal")
        p[0] = p[1]

def p_error(p):
        print ("Error:",p)
        #p.parser.error = True

def parser_file(file):

        parser = yacc.yacc()

        parser.error = False
        parser.act_sem = {}
        parser.prods = {}
        parser.code = ""
        parser.prod_name = ""
        parser.term = []
        parser.axioma = ""

        #try:
        fd = open(file,"r")
        for line in fd:
                print(line)
                parser.parse(line)
                if parser.error:
                        print("erro parser")
                        break
                        
        #except:
        #        print("Ficheiro não foi encontrado")
        #        parser.error = True

        return (parser.term,parser.prods,parser.axioma,parser.act_sem,parser.code,parser.error)