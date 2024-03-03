import follow_set 
import first_set 

class Error:
    def __init__ (self, error_type, error_message, lexer_output):
        self.error_type = error_type
        self.error_message = error_message
        self.line_number = 0
        self.lexeme = ""    
        self.start_position = 1
        #self.end_position = end_position

        for lexeme, token, line_number in lexer_output:
            self.line_number = line_number 
            self.lexeme = lexeme
            self.token = lexeme
        
        print("From lexer: ", lexer_output)
    
    def __str__(self):
        notif = f"[{self.error_type}] Syntax Error on line {self.line_number}"

        notif += f":\n\t{self.error_message}"

        
        #TODO: add indicator for the error position

        return notif
    

class SyntaxAnalyzer:
    def __init__(self, lexer_output):
        self.lexer_output = lexer_output
        self.tokens = []
        self.i = 0
        
        for lexeme, token, line_number in lexer_output:
            self.tokens.append(token)        
        self.tokens.append('EOF')
        
        self.prev_token = self.tokens[self.i-1]
        self.current_token = self.tokens[self.i]
        self.next_token = self.tokens[self.i+1]
        self.analyzed = []
        self.synErrors = []
        self.break_flag = 0

        self.line_number = 0
        self.lexeme = ""
        
        self.reserved_words = ['bool_po','char_po','default_po','float_po','gawin_po', 
                  'habang_po','ibalik_po','int_po','ilabas_po', 'kundi_po','kung_po',
                  'magpasok_po','mali_po','okaya_po','sakali_po',
                  'str_po','totoo_po','tigil_po','lagi_po','_ni_','tuloy_po',
                  'wala_po', 'mamili_po','ulit_po','estruktura_po']
    
    def advance(self):
        if self.current_token == 'EOF':
            return

        self.analyzed.append(self.current_token)
        self.i += 1

        if self.i < len(self.tokens):
            self.current_token = self.tokens[self.i]
            self.next_token = self.tokens[self.i+1] if self.i+1 < len(self.tokens) else 'EOF'
        else:
            self.current_token = 'EOF'
    
    def follow(self,production):
        return follow_set.follow_set[production]

    def first(self, production):
        return first_set.first_set[production]
    
    def analyze(self):
        while self.current_token != 'EOF' and self.synErrors == [] and self.break_flag == 0:
            self.start_program()
            print("break flag: ", self.break_flag)
            
        
        print("------Finished program analysis-------")

    def start_program(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first('program'):
                self.program()
            elif self.current_token == 'simula_po':
                self.simula_po()
            else: #if self.current_token not in ['int_po','float_po','bool_po','char_po','str_po', 'lagi_po', 'estruktura_po', '#']:
                #self.error_missing_simula_po()
                
                self.self_invalid_global_dec()
            


    def simula_po(self):
        if self.i < len(self.tokens):
            self.advance()
            print("nag simula_po")
            self.declaration()
            print("nag declaration")
            self.statement()
            print("nag statement")
            if self.current_token == 'wakas_po':
                self.advance()
                self.check_next()
                self.func_definition()
            else:
                self.error_missing_wakas_po()

    
    def program(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first('global_dec'):
                self.global_dec()
                if self.current_token == 'simula_po':
                    self.simula_po()                    
                else:
                    self.error_missing_simula_po() #working
            
                

    
    def check_next(self):
        if self.current_token not in ['#', 'EOF']:
            self.error_after_wakas_po()
        else:
            return
      
                        
    def global_dec(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("declaration"):
                self.declaration()
                self.global_dec()
            elif self.current_token in self.first("struct_dec"):
                self.struct_dec()
                self.global_dec()
            elif self.current_token in self.follow("global_dec"):
                return
            
    
    def declaration(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("var_dec"):
                self.var_dec()
                self.declaration()
            elif self.current_token in self.first("kons_dec"):
                self.kons_dec()  
                self.declaration()
            elif self.current_token in self.first("func_dec"):
                self.func_dec()
                self.declaration()
            elif self.current_token in self.follow("declaration") or 'id' in self.current_token:
                print("nagreturn?")
                return
            
            #else:
            #    self.error_invalid_declaration()

    def var_dec(self): 
        if self.i < len(self.tokens):
            if self.next_token in self.reserved_words:
                print("HEREEEEEEEEE")
                self.error_reserved_word_in_dec()

            if self.current_token == 'int_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.int_value()
                    self.int_value_tail()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        print("dito nagterminate")
                        self.error_missing_terminator() 
                else:
                    self.error_missing_id_in_dec() 
            elif self.current_token == 'float_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.float_value()
                    self.float_value_tail()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        self.error_missing_terminator()
                else:
                    self.error_missing_id_in_dec()
            elif self.current_token == 'bool_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.bool_value()
                    self.bool_value_tail()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        self.error_missing_terminator()
                else:
                    self.error_missing_id_in_dec()
            elif self.current_token == 'char_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.char_value()
                    self.char_value_tail()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        self.error_missing_terminator()
                else:
                    self.error_missing_id_in_dec()
            elif self.current_token == 'str_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.str_value()
                    self.str_value_tail()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        self.error_missing_terminator()
                else:
                    self.error_missing_id_in_dec()
            
               
                
            #else:

                
            
            
            
    

    def int_value(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in ['=', '[']:
                if self.current_token == '=':
                    self.advance()
                    self.int_value_prod()
                elif self.current_token == '[':
                    self.int_array_dec()
            else:
                self.error_missing_assignment()
            
            

    def int_value_prod(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("int_value_prod") or 'id' in self.current_token or self.current_token in ['++', '--']:
                if self.current_token in self.first("arithmetic") or 'id' in self.current_token or self.current_token in ['++', '--']: #TODO: add first set of arithmetic_int
                    self.arithmetic_int()
                elif self.current_token == 'strlen_po':
                    self.strlen_exp()
            else:
                #self.error_expecting_value()
                self.error_invalid_value_int_dec() #working
               
                

            
    def int_value_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("int_value_tail"):
                if self.current_token == ',':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.int_value()
                        self.int_value_tail()
                    else:
                        self.error_missing_id_in_dec()
                
            elif self.current_token in self.follow("int_value_tail"):
                return
            else:
                print("int_value_tail")
                self.error_missing_sep_ter() 

    def arithmetic_int(self): 
        if self.i < len(self.tokens):
            self.math_val_int()
            self.arithmetic_int_tail()
            

    def math_val_int(self): 
        if self.i < len(self.tokens):
            if self.current_token == '(':
                self.advance()
                self.arithmetic_int()
                if self.current_token == ')':
                    self.advance()
                else:
                    self.error_unclosed_parenthesis()
                    
            elif self.current_token == '-':
                self.advance()
                self.math_val_int()
            elif self.current_token in ['++', '--', 'intlit'] or 'id' in self.current_token: #TODO: add first set ni unary
                self.unary()
            else:
                self.error_invalid_value_int_dec() #working

    def unary(self):
        if self.i < len(self.tokens):
            print("inside unary ", self.current_token)
            if self.current_token in ['++', '--']:
                self.unary_op()
                self.unary_val()
            else:
                self.unary_val()
                self.unary_post_op()


    def unary_op(self):
        if self.i < len(self.tokens):
            if self.current_token in ['++', '--']:
                self.advance()

    def unary_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'intlit': #OK
                print("inside unary val", self.current_token)
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()

    def unary_post_op(self):
        if self.i < len(self.tokens):
            if self.current_token in ['++', '--']: #OK
                self.unary_op()
            elif self.current_token in [';', ',', ')', ']', '+', '-', '*', '/']:
                return
            


    def arithmetic_int_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("arithmetic_tail"):
                self.arithmetic_op()
                self.math_val_int()
                self.arithmetic_int_tail()
            elif self.current_token in [',', ';', ')', ']']:
                return


    def arithmetic_op(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("arithmetic_op"):
                self.advance()
            else:
                self.missing_arithmetic_op() #working
            
                

    def id_prod_func(self): #OK
        if self.i < len(self.tokens):
            if 'id' in self.current_token:
                self.advance()
                self.id_tail_func()

    def id_tail_func(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in ['[', '_ni_']: #first set ni id_tail
                self.id_tail()
            elif self.current_token == '(': #first set ni func_call
                self.func_call()
            elif self.current_token in self.follow("id_tail"): #change to follow set ni 'id_tail_func'
                return

    def id_prod(self): #OK
        if self.i < len(self.tokens):
            if 'id' in self.current_token:
                self.advance()
                self.id_tail()

    def id_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.array_access()
            elif self.current_token == '_ni_':
                self.struct_access()
            elif self.current_token in [',', ';', '}', '=', '+=', '-=', '*=', '/=' ]: #follow set of id_tail
                return

    def array_access(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.index()
                if self.current_token == ']':
                    self.advance()
                    self.index_tail()
                else:
                    self.error_unclosed_square_bracket()

    def index(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("index") or self.current_token in ['++', '--'] or 'id' in self.current_token:
                self.arithmetic_int()
            else:
                self.error_invalid_array_index()

    def index_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.index()
                if self.current_token == ']':
                    self.advance()
                else:
                    self.error_unclosed_square_bracket()
            elif self.current_token in self.follow("index_tail"):
                return

    def struct_access(self): #TODO: test after updating lexical
        if self.i < len(self.tokens):
            if self.current_token == '_ni_':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                else:
                    self.error_missing_id_in_struct_access()

    def func_call(self):
        if self.i < len(self.tokens):
            if self.current_token == '(':
                self.advance()
                self.arguments()
                if self.current_token == ')':
                    self.advance()
                #else:
                    #self.error_unclosed_parenthesis()
                    #print("FUNC CAAAALLLL")

    def arguments(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("arguments") or 'id' in self.current_token or self.current_token in ['!', '++', '--', 'strlen', '(', '-', 'intlit', 'floatlit']:
                self.arguments_val()
                self.args_tail()
            elif self.current_token in self.follow("arguments"):
                return

    def arguments_val(self):
        if self.i < len(self.tokens):
            if self.current_token in ['charlit', 'boollit']: #OK
                self.advance()
            elif self.current_token in self.first("expression") or 'id' in self.current_token:
                self.expression()
            
            else:
                self.error_expecting_value() #working

    def args_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("args_tail"):
                if self.current_token == ',':
                    self.advance()
                    self.arguments_val()
                    self.args_tail()
                
            elif self.current_token in self.follow("args_tail") or 'id' in self.current_token or self.current_token in ['+', '-', '*', '/', ')']: #TODO: fix follow set of args_tail
                return
            #else:  NOTE: removed
                #self.error_missing_separator() #working
                

    def other_values(self):
        if self.i < len(self.tokens):
            if self.current_token in ['charlit', 'boollit']:
                self.advance()


    def expression(self): #75
        if self.i < len(self.tokens):
            print("inside expression")
            if self.current_token in ['(', '!', '-', 'floatlit', '++', '--', 'intlit'] or 'id' in self.current_token: #first set of rel_arith_logic_expr
                self.rel_arith_logic_expr()
            
            elif self.current_token in self.first("string_cont") or 'id' in self.current_token:
                self.string_cont()

            elif self.current_token == 'strlen_po':
                self.strlen_exp()
            
            elif self.current_token in self.follow("expression"):
                return
            
            else:
                self.error_invalid_expr() #TODO
            
            
            
    def rel_arith_logic_expr(self):
        if self.i < len(self.tokens):
            self.logical_val()
            self.logical_tail()
    
    def logical_val(self):
        if self.i < len(self.tokens):
            """if self.current_token == '(':
                print("parenthesis in logical val")
                self.advance()
                self.rel_arith_logic_expr()
                if self.current_token == ')':
                    print("closing parenthesis in logical val")
                    self.advance()
                else:
                    self.error_unclosed_parenthesis()"""
            """if self.current_token == '!':
                self.advance()
                self.logical_val()"""
            if self.current_token in [ '(', '-', 'floatlit', '++', '--', 'intlit', '!'] or 'id' in self.current_token: #first set ni arithmetic
                self.relational_arithmetic()
    
  
           
    def logical_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("logical_tail"):
                self.logical_op()
                self.rel_arith_logic_expr()
            elif self.current_token in self.follow("logical_tail"):
                return
            

    def logical_op(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("logical_op"):
                self.advance()
            
    def relational_arithmetic(self):
        if self.i < len(self.tokens):
            print("inside relational_arithmetic")
            if self.current_token in [ '(', '-', 'floatlit', '++', '--', 'intlit', '!'] or 'id' in self.current_token:
                self.arithmetic()
                self.relational_tail()
            if self.current_token == 'boollit':
                self.advance()
            if self.current_token in ['charlit', 'stringlit']:
                self.error_invalid_operand_in_rel()
            #else:
            #    print("missing operand")
            #    self.error_missing_operand()
            """elif self.current_token == '!':
                self.advance()
                self.logical_val()"""
            

    def relational_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("relational_tail"):
                self.relational_op()
                self.relational_arithmetic()
            elif self.current_token in self.first("logical_tail"):
                self.logical_op()
                self.rel_arith_logic_expr()
            elif self.current_token in self.follow("relational_tail"):
                return
            #else:
            #    self.error_invalid_relational_op() #TODO: check error message

            
    def relational_op(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("relational_op"):
                self.advance()
            
            

    def arithmetic(self):
         if self.i < len(self.tokens):
            print("inside arithmetic ", self.current_token)
            self.math_val()
            self.arithmetic_tail()

    def math_val(self):
        if self.i < len(self.tokens):
            if self.current_token == '(':
                self.advance()
                self.arithmetic()
                if self.current_token == ')':
                    self.advance()
                else:
                    self.error_unclosed_parenthesis()
            elif self.current_token == '-':
                self.advance()
                self.math_val()
            elif self.current_token == 'floatlit':
                self.advance()
            elif self.current_token in ['++', '--', 'intlit'] or 'id' in self.current_token:
                self.unary() 
            elif self.current_token == '!':
                self.advance()
                self.logical_val()
            else:
                self.error_invalid_value_arithmetic()

    def arithmetic_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("arithmetic_tail"):
                print("arithmetic_tail", self.current_token)
                self.arithmetic_op()
                self.math_val()
                self.arithmetic_tail()
            elif self.current_token in self.first("relational_tail"):
                self.relational_op()
                self.relational_arithmetic()
            elif self.current_token in self.first("logical_tail"):
                self.logical_op()
                self.rel_arith_logic_expr()

            elif self.current_token in [',', ';', ')', ']']:
                return


    def string_cont(self):
        if self.i < len(self.tokens):
            self.string_cont_val()
            self.string_cont_tail()

    def string_cont_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'stringlit':
                self.advance()
            elif 'id' in self.current_token:
                self.advance()
            else:
                self.error_invalid_value_strcont()
    
    def string_cont_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == '+':
                self.advance()
                self.string_cont_val()
                self.string_cont_tail()
            elif self.current_token in [',', ')']: #change to follow set ni string_cont_tail
                return
            #else:
                
            

    
    def strlen_exp(self):
        if self.i < len(self.tokens):
            if self.current_token == 'strlen_po':
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.strlen_item_val()
                    if self.current_token == ')':
                        self.advance()
                    else:
                        self.error_unclosed_parenthesis()
                else:
                    self.error_missing_paren_strlen()
                
    def strlen_item_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("strlen_item_val") or 'id' in self.current_token:                    
                self.strlen_val()
                self.strlen_val_tail()
            else:
                self.error_invalid_value_strlen()
    
    def strlen_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'stringlit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod()
    
    def strlen_val_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == '+': #OK
                self.advance()
                if self.current_token == 'intlit': #NOTE: double check
                    self.advance()
                else:
                    self.error_expecting_int()
                
            elif self.current_token in ')':
                return
    
    def int_array_dec(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.int_array_dec2()
                else:
                    self.error_unclosed_square_bracket() #working
    
    def array_size(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == 'intlit':
                self.advance()
            elif 'id' in self.current_token:
                self.advance()
            else:
                self.error_array_size() #working

    def int_array_dec2(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.int_array_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace() #working
                else:
                    self.error_missing_curly_brace_array() #working
            elif self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.int_array_2d_val()
                else:
                    self.error_unclosed_square_bracket() #working
            else:
                self.error_invalid_array_dec() #working
    
    def int_array_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.error_unexpected_curly_brace()
            self.int_array_item_val()
            self.int_array_dec2_tail() 

    def int_array_item_val(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == 'intlit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()
            else:
                self.error_invalid_data_type_int_dec() #working

    def int_array_dec2_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.int_array_item_val()
                self.int_array_dec2_tail()
            elif self.current_token in self.follow("int_array_dec2_tail"):
                return
            else:
                self.error_missing_sep_curl() #working

    def int_array_2d_val(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.int_array_2d_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace() #working
                else:
                    self.error_missing_curly_brace_array() #working
    
    def int_array_2d_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.int_array_item()
                if self.current_token == '}':
                    self.advance()
                    self.int_array_item_tail()
                else:
                    self.error_unclosed_curly_brace() #working
            else:
                self.error_missing_curly_brace_array() #working

    def int_array_item_tail(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.int_array_2d_item()
            elif self.current_token in self.follow("int_array_item_tail"):
                return
            else:
                self.error_missing_separator() #working


################ START OF FLOAT CFG ############################# START OF FLOAT CFG ############################# START OF FLOAT CFG ############################# START OF FLOAT CFG #############################

    def float_value(self):
        if self.i < len(self.tokens):
            if self.current_token in ['=', '[']:
                if self.current_token == '=':
                    self.advance()
                    self.float_value_prod()
                elif self.current_token == '[':
                    self.float_array_dec()
            else:
                self.error_missing_assignment()
            
            
    def float_value_prod(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("float_value_prod") or 'id' in self.current_token or self.current_token in ['++', '--']:
                self.arithmetic()
            else:
                self.error_invalid_value_float_dec() #working
    
    def float_value_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("float_value_tail"):
                if self.current_token == ',':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.float_value()
                        self.float_value_tail()
                    else:
                        self.error_missing_id_in_dec()
                #else:
                #    self.error_missing_sep_ter() #TODO: double check
            elif self.current_token in self.follow("float_value_tail"):
                return
            else:
                self.error_missing_sep_ter() #TODO: double check

    def float_array_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.float_array_dec2()
                else:
                    self.error_unclosed_square_bracket()
    
    def float_array_dec2(self):
         if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.float_array_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
            elif self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.float_array_2d_val()
                else:
                    self.error_unclosed_square_bracket() #working
            else:
                self.error_invalid_array_dec() #working

    def float_array_item(self):
        if self.i < len(self.tokens):
            self.float_array_item_val() 
            self.float_array_dec2_tail()

    def float_array_item_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'floatlit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()
            else:
                self.error_invalid_data_type_float_dec()
    
    def float_array_dec2_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.float_array_item_val()
                self.float_array_dec2_tail()
            elif self.current_token in self.follow("float_array_dec2_tail"):
                return 
            else:
                self.error_missing_sep_curl() #working
    
    def float_array_2d_val(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.float_array_2d_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
    
    def float_array_2d_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.float_array_item()
                if self.current_token == '}':
                    self.advance()
                    self.float_array_item_tail()
                else:
                    self.error_unclosed_curly_brace()
            else:
                self.error_missing_curly_brace_array()

    def float_array_item_tail(self): #OK ---tag
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.float_array_item()
                    if self.current_token == '}':
                        self.advance()
                        self.float_array_item_tail()
                    else:
                        self.error_unclosed_curly_brace()
            elif self.current_token in self.follow("float_array_item_tail"):
                return
            else:
                self.error_missing_separator() #working

################ END OF FLOAT CFG ############################# END OF FLOAT CFG ############################# END OF FLOAT CFG ############################# END OF FLOAT CFG #############################


################ START OF BOOL CFG ############################# START OF BOOL CFG ############################# START OF BOOL CFG ############################# START OF BOOL CFG #############################

    def bool_value(self):
        if self.i < len(self.tokens):
            if self.current_token in ['=', '[']:
                if self.current_token == '=':
                    self.advance()
                    self.bool_value_prod()
                elif self.current_token == '[':
                    self.bool_array_dec()
            else:
                self.error_missing_assignment()
            
            
    def bool_value_prod(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == 'boollit' or 'id' in self.current_token:
                if self.current_token == 'boollit':
                    self.advance()
                elif 'id' in self.current_token:
                    self.id_prod()
                #elif self.current_token in self.first("arithmetic") or 'id' in self.current_token or self.current_token in ['++', '--']:
                    #self.rel_arith_logic_expr()
            else:
                self.error_invalid_value_bool_dec() #working
    
    def bool_value_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("bool_value_tail"):
                if self.current_token == ',':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.bool_value()
                        self.bool_value_tail()
                    else:
                        self.error_missing_id_in_dec()
                #else:
                #    self.error_missing_sep_ter() #TODO: double check
            elif self.current_token in self.follow("bool_value_tail"):
                return
            else:
                self.error_missing_sep_ter() #TODO: double check

    def bool_array_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.bool_array_dec2()
                else:
                    self.error_unclosed_square_bracket()
    
    def bool_array_dec2(self):
         if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.bool_array_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
            elif self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.bool_array_2d_val()
                else:
                    self.error_unclosed_square_bracket() #working
            else:
                self.error_invalid_array_dec() #working

    def bool_array_item(self):
        if self.i < len(self.tokens):
            self.bool_array_item_val() 
            self.bool_array_dec2_tail()

    def bool_array_item_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'boollit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()
            else:
                self.error_invalid_data_type_bool_dec()
    
    def bool_array_dec2_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.bool_array_item_val()
                self.bool_array_dec2_tail()
            elif self.current_token in self.follow("bool_array_dec2_tail"):
                return 
            else:
                self.error_missing_sep_curl() #working
    
    def bool_array_2d_val(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.bool_array_2d_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
    
    def bool_array_2d_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.bool_array_item()
                if self.current_token == '}':
                    self.advance()
                    self.bool_array_item_tail()
                else:
                    self.error_unclosed_curly_brace()
            else:
                self.error_missing_curly_brace_array()

    def bool_array_item_tail(self): #OK ---tag
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.bool_array_item()
                    if self.current_token == '}':
                        self.advance()
                        self.bool_array_item_tail()
                    else:
                        self.error_unclosed_curly_brace()
            elif self.current_token in self.follow("bool_array_item_tail"):
                return
            else:
                self.error_missing_separator() #working

################ END OF BOOL CFG ############################# END OF BOOL CFG ############################# END OF BOOL CFG ############################# END OF BOOL CFG #############################

################ START OF CHAR CFG ############################# START OF CHAR CFG ############################# START OF CHAR CFG ############################# START OF CHAR CFG #############################


    def char_value(self):
        if self.i < len(self.tokens):
            if self.current_token in ['=', '[']:
                if self.current_token == '=':
                    self.advance()
                    self.char_value_prod()
                elif self.current_token == '[':
                    self.char_array_dec()
            else:
                self.error_missing_assignment()
            
            
    def char_value_prod(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("char_value_prod") or 'id' in self.current_token:
                if self.current_token == 'charlit':
                    self.advance()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_invalid_value_char_dec() #working
    
    def char_value_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("char_value_tail"):
                if self.current_token == ',':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.char_value()
                        self.char_value_tail()
                    else:
                        self.error_missing_id_in_dec()
                #else:
                #    self.error_missing_sep_ter() #TODO: double check
            elif self.current_token in self.follow("char_value_tail"):
                return
            else:
                self.error_missing_sep_ter() #TODO: double check

    def char_array_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.char_array_dec2()
                else:
                    self.error_unclosed_square_bracket()
    
    def char_array_dec2(self):
         if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.char_array_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
            elif self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.char_array_2d_val()
                else:
                    self.error_unclosed_square_bracket() #working
            else:
                self.error_invalid_array_dec() #working

    def char_array_item(self):
        if self.i < len(self.tokens):
            self.char_array_item_val() 
            self.char_array_dec2_tail()

    def char_array_item_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'charlit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()
            else:
                self.error_invalid_data_type_char_dec()
    
    def char_array_dec2_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.char_array_item_val()
                self.char_array_dec2_tail()
            elif self.current_token in self.follow("char_array_dec2_tail"):
                return 
            else:
                self.error_missing_sep_curl() #working
    
    def char_array_2d_val(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.char_array_2d_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
    
    def char_array_2d_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.char_array_item()
                if self.current_token == '}':
                    self.advance()
                    self.char_array_item_tail()
                else:
                    self.error_unclosed_curly_brace()
            else:
                self.error_missing_curly_brace_array()

    def char_array_item_tail(self): #OK ---tag
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.char_array_item()
                    if self.current_token == '}':
                        self.advance()
                        self.char_array_item_tail()
                    else:
                        self.error_unclosed_curly_brace()
            elif self.current_token in self.follow("char_array_item_tail"):
                return
            else:
                self.error_missing_separator() #working


################ START OF CHAR CFG ############################# START OF CHAR CFG ############################# START OF CHAR CFG ############################# START OF CHAR CFG #############################


################ START OF STRING CFG ############################# START OF STRING CFG ############################# START OF STRING CFG ############################# START OF STRING CFG #############################

    def str_value(self):
        if self.i < len(self.tokens):
            if self.current_token in ['=', '[']:
                if self.current_token == '=':
                    self.advance()
                    self.str_value_prod()
                elif self.current_token == '[':
                    self.str_array_dec()
            else:
                self.error_missing_assignment()
            
            
    def str_value_prod(self): #OK
        if self.i < len(self.tokens):
            if self.current_token in self.first("str_value_prod") or 'id' in self.current_token:
                if self.current_token == 'stringlit':
                    self.string_cont()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_invalid_value_str_dec() #working
    
    def str_value_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("str_value_tail"):
                if self.current_token == ',':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.str_value()
                        self.str_value_tail()
                    else:
                        self.error_missing_id_in_dec()
                #else:
                #    self.error_missing_sep_ter() #TODO: double check
            elif self.current_token in self.follow("str_value_tail"):
                return
            else:
                self.error_missing_sep_ter() #TODO: double check

    def str_array_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.str_array_dec2()
                else:
                    self.error_unclosed_square_bracket()
    
    def str_array_dec2(self):
         if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.str_array_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
            elif self.current_token == '[':
                self.advance()
                self.array_size()
                if self.current_token == ']':
                    self.advance()
                    self.str_array_2d_val()
                else:
                    self.error_unclosed_square_bracket() #working
            else:
                self.error_invalid_array_dec() #working

    def str_array_item(self):
        if self.i < len(self.tokens):
            self.str_array_item_val() 
            self.str_array_dec2_tail()

    def str_array_item_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'stringlit':
                self.advance()
            elif 'id' in self.current_token:
                self.id_prod_func()
            else:
                self.error_invalid_data_type_str_dec()
    
    def str_array_dec2_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.str_array_item_val()
                self.str_array_dec2_tail()
            elif self.current_token in self.follow("str_array_dec2_tail"):
                return 
            else:
                self.error_missing_sep_curl() #working
    
    def str_array_2d_val(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.str_array_2d_item()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:
                    self.error_missing_curly_brace_array()
    
    def str_array_2d_item(self): #OK
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.str_array_item()
                if self.current_token == '}':
                    self.advance()
                    self.str_array_item_tail()
                else:
                    self.error_unclosed_curly_brace()
            else:
                self.error_missing_curly_brace_array()

    def str_array_item_tail(self): #OK ---tag
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.str_array_item()
                    if self.current_token == '}':
                        self.advance()
                        self.str_array_item_tail()
                    else:
                        self.error_unclosed_curly_brace()
            elif self.current_token in self.follow("str_array_item_tail"):
                return
            else:
                self.error_missing_separator() #working




################ END OF STRING CFG ############################# END OF STRING CFG ############################# END OF STRING CFG ############################# END OF STRING CFG #############################


###################### KONS_DEC CFG ############################# KONS_DEC CFG ############################# KONS_DEC CFG ############################# KONS_DEC CFG #############################

    def kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == 'lagi_po':
                self.advance()
                self.kons_dec_data_type() 
                if self.current_token == ';':
                    self.advance()
                else:
                    self.error_missing_terminator()

    def kons_dec_data_type(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("kons_dec_data_type"):
                if self.current_token == 'int_po':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.int_kons_dec()
                    else:
                        self.error_missing_id_in_dec()
                elif self.current_token == 'float_po':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.float_kons_dec()
                    else:
                        self.error_missing_id_in_dec()
                elif self.current_token == 'bool_po':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.bool_kons_dec()
                    else:
                        self.error_missing_id_in_dec()
                elif self.current_token == 'char_po':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.char_kons_dec()
                    else:
                        self.error_missing_id_in_dec()
                elif self.current_token == 'str_po':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        self.str_kons_dec()
                    else:
                        self.error_missing_id_in_dec()
            else:
                self.error_expected_data_type()
    
    #INT KONS DEC

    def int_kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("int_kons_dec"):
                if self.current_token == '=':
                    self.advance()
                    self.int_kons_dec_val() 
                elif self.current_token == '[':
                    self.int_array_dec()
            else:
                self.error_expecting_value_kons_dec() #working 

    def int_kons_dec_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("int_kons_dec_val") or 'id' in self.current_token:
                if self.current_token == 'intlit':
                    self.advance()
                    self.int_kons_tail()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_expecting_value_kons_dec()
    
    def int_kons_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.int_kons_dec()
            elif self.current_token in self.follow("int_kons_tail"):
                return
            else:
                self.error_missing_sep_ter()

    #FLOAT KONS DEC
    def float_kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("float_kons_dec"):
                if self.current_token == '=':
                    self.advance()
                    self.float_kons_dec_val() 
                elif self.current_token == '[':
                    self.float_array_dec()
            else:
                self.error_expecting_value_kons_dec() #working 

    def float_kons_dec_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("float_kons_dec_val") or 'id' in self.current_token:
                if self.current_token == 'floatlit':
                    self.advance()
                    self.float_kons_tail()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_expecting_value_kons_dec()
    
    def float_kons_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.float_kons_dec()
            elif self.current_token in self.follow("float_kons_tail"):
                return
            else:
                self.error_missing_sep_ter()


    #BOOL KONS DEC
    def bool_kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("bool_kons_dec"):
                if self.current_token == '=':
                    self.advance()
                    self.bool_kons_dec_val() 
                elif self.current_token == '[':
                    self.bool_array_dec()
            else:
                self.error_expecting_value_kons_dec() #working 

    def bool_kons_dec_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("bool_kons_dec_val") or 'id' in self.current_token:
                if self.current_token == 'boollit':
                    self.advance()
                    self.bool_kons_tail()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_expecting_value_kons_dec()
    
    def bool_kons_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.bool_kons_dec()
            elif self.current_token in self.follow("bool_kons_tail"):
                return
            else:
                self.error_missing_sep_ter()    
            
    #CHAR KONS DEC
    def char_kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("char_kons_dec"):
                if self.current_token == '=':
                    self.advance()
                    self.char_kons_dec_val() 
                elif self.current_token == '[':
                    self.char_array_dec()
            else:
                self.error_expecting_value_kons_dec() #working 

    def char_kons_dec_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("char_kons_dec_val") or 'id' in self.current_token:
                if self.current_token == 'charlit':
                    self.advance()
                    self.char_kons_tail()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_expecting_value_kons_dec()
    
    def char_kons_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.char_kons_dec()
            elif self.current_token in self.follow("char_kons_tail"):
                return
            else:
                self.error_missing_sep_ter()
    
    #STR KONS DEC
    def str_kons_dec(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("str_kons_dec"):
                if self.current_token == '=':
                    self.advance()
                    self.str_kons_dec_val() 
                elif self.current_token == '[':
                    self.str_array_dec()
            else:
                self.error_expecting_value_kons_dec() #working 

    def str_kons_dec_val(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("str_kons_dec_val") or 'id' in self.current_token:
                if self.current_token == 'stringlit':
                    self.advance()
                    self.str_kons_tail()
                elif 'id' in self.current_token:
                    self.id_prod_func()
            else:
                self.error_expecting_value_kons_dec()
    
    def str_kons_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    self.str_kons_dec()
            elif self.current_token in self.follow("str_kons_tail"):
                return
            else:
                self.error_missing_sep_ter()


################ START OF FUNC DEC CFG ############################# START OF FUNC DEC CFG ############################# START OF FUNC DEC CFG ############################# START OF FUNC DEC CFG #############################
# TESTED. OK
    def func_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == '#':
                self.advance()
                self.func_type()
                if 'id' in self.current_token:
                    self.advance()
                    if self.current_token == '(':
                        self.advance()
                        self.parameter()
                        if self.current_token == ')':
                            self.advance()
                            if self.current_token == ';':
                                self.advance()
                            else:
                                self.error_missing_terminator()
                        else:
                            self.error_unclosed_parenthesis()
                    else:
                        self.error_missing_paren_func()
                else:
                    self.error_missing_id_in_func()

    def func_type(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("func_type"):
                if self.current_token == 'wala_po':
                    self.advance()
                elif self.current_token in self.first("data_type"):
                    self.data_type()
            else:
                self.error_missing_data_type_func()

    def data_type(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("data_type"):
                self.advance()


    def parameter(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("data_type"):
                self.data_type()
                if 'id' in self.current_token:
                    self.advance()
                    self.parameter_tail()
                else:
                    self.error_missing_id_in_parameter()
            elif self.current_token in self.follow("parameter"):
                return

    def parameter_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("parameter_tail"):
                if self.current_token == ',':
                    self.advance()
                    self.parameter()
            elif self.current_token in self.follow("parameter_tail"):
                return
            else:
                self.error_missing_sep_par()

################ END OF FUNC DEC CFG ############################# END OF FUNC DEC CFG ############################# END OF FUNC DEC CFG ############################# END OF FUNC DEC CFG #############################


################ START OF STRUCT DEC CFG ############################# START OF STRUCT DEC CFG ############################# START OF STRUCT DEC CFG ############################# START OF STRUCT DEC CFG #############################
#TESTED. OK

    def struct_dec(self):
        if self.i < len(self.tokens):
            if self.current_token == 'estruktura_po':
                self.advance()
                if 'id' in self.current_token:
                    self.advance()
                    if self.current_token == '{':
                        self.advance()
                        self.struct_body()
                        if self.current_token == '}':
                            self.advance()
                            if self.current_token == ';':
                                self.advance()
                            else:
                                self.error_missing_terminator_struct()
                        else:
                            self.error_unclosed_curly_brace()
                    else:
                        self.error_missing_curly_brace_struct()
                else:
                    self.error_missing_id_in_struct_dec()
    
    def struct_body(self):
        if self.i < len(self.tokens):
            if self.current_token not in ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po']:
                self.error_invalid_struct_body()
            self.var_dec()
            self.var_dec_tail()
    
    def var_dec_tail(self):
        if self.i < len(self.tokens):
            if self.current_token not in ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po']:
                self.error_invalid_struct_body()

            if self.current_token in self.first("var_dec"):
                self.struct_body()
            elif self.current_token =='}': #follow set ni var_dec_tail
                return



################ END OF STRUCT DEC CFG ############################# END OF STRUCT DEC CFG ############################# END OF STRUCT DEC CFG ############################# END OF STRUCT DEC CFG #############################


################ START OF STATEMENT CFG ############################# START OF STATEMENT CFG ############################# START OF STATEMENT CFG ############################# START OF STATEMENT CFG #############################


    def statement(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("statement") or 'id' in self.current_token or self.current_token in ['ibalik_po', 'tigil_po', 'tuloy_po', '++', '--']:
                if 'id' in self.current_token:
                    #print("pumunta kay id_prod_statements")
                    self.id_prod_statements() #DONE
                    self.statement()
                elif self.current_token in ['++', '--']:
                    self.unary_pre_statement()
                    self.statement()
                elif self.current_token == 'ilabas_po':
                    #print("pumunta kay output_statement")
                    self.output_statement() #DONE
                    self.statement()
                elif self.current_token in self.first("conditional_statement") or self.current_token in ['okaya_po', 'kundi_po']:
                    #print("pumunta kay conditional_statement")
                    if self.current_token in ['okaya_po', 'kundi_po']:
                        self.error_missing_kung_po()
                    self.conditional_statement() 
                    self.statement()
                elif self.current_token in self.first("for_statement"):
                    #print("pumunta kay for_statement")
                    self.for_statement() 
                    self.statement()
                elif self.current_token in self.first("do-while_statement"):
                    #print("pumunta kay do-while_statement")
                    self.dowhile_statement() 
                    self.statement()
                elif self.current_token in self.first("while_statement"):
                    #print("pumunta kay while_statement")
                    self.while_statement() 
                    self.statement()
                elif self.current_token == 'ibalik_po':
                    self.ibalikpo_statement()
                    self.statement()
                elif self.current_token in ['tigil_po', 'tuloy_po']:
                    self.control_statement() 
                    self.statement()
                
            elif self.current_token in self.follow("statement"):
                print("nagreturn from statement?")
                return
            #elif self.current_token in ['okaya_po', 'kundi_po']:
            #    self.error_missing_kung_po()
            #else:
                print("AAAAAAAAAAAAAAAA")
                #self.error_invalid_statement()
            


    ####################### ID PROD STATEMENTS #######################

    def id_prod_statements(self):
        if self.i < len(self.tokens):
            self.advance()
            self.id_prod_statement_tail()
            if self.current_token == ';':
                self.advance()
            else:
                #print("missing terminator sa id_prod_statements")
                self.error_missing_terminator()

    def id_prod_statement_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in ['[', '_ni_']: #first set of id_tail
                self.id_tail()
                self.assignment_statement()
            elif self.current_token =='(': #first set of func_call
                self.func_call()
            elif 'id' in self.current_token:
                self.advance()
            elif self.current_token in ['++', '--']:
                self.unary_op()
            elif self.current_token in ['=', '+=', '-=', '*=', '/=', '%=']: #first set of assignment_statement
                #print("pumunta kay assignment_statement")
                self.assignment_statement()
            else:
                self.error_invalid_id_only()
            
    def assignment_statement(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("assign_op"):
                self.assign_op()
                self.assignment_val()
            elif self.current_token == '=':
                self.advance()
                self.assignment_val_input()
    
    def assign_op(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("assign_op"):
                self.advance()

    def assign_op_eq(self):
        if self.i < len(self.tokens):
            if self.current_token == '=':
                self.advance()
            if self.current_token in self.first("assign_op"):
                self.assign_op()

    def assignment_val(self):
        if self.i < len(self.tokens):
            if self.current_token in ['charlit', 'boollit']:
                self.other_values()
            elif self.current_token in ['(', '!', '-', 'floatlit', '++', '--', 'intlit', 'stringlit', 'strlen_po'] or 'id' in self.current_token: #first set of expression
                self.expression()
            else:
                self.error_missing_value_assign()
    
    def assignment_val_input(self):
        if self.i < len(self.tokens):
            if self.current_token in ['charlit', 'boollit', '(', '!', '-', 'floatlit', '++', '--', 'intlit', 'stringlit', 'strlen_po'] or 'id' in self.current_token: #first set of assignment_val
                print("assignment_val")
                self.assignment_val()
            elif self.current_token == 'magpasok_po':
                self.input_statement_val()
            else:
                self.error_missing_value_assign()

    def input_statement_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'magpasok_po':
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.prompt()
                    if self.current_token == ')':
                        self.advance()
                    else:
                        self.error_unclosed_parenthesis()
                else:
                    self.error_missing_paren_input()
    
    def prompt(self): 
        if self.i < len(self.tokens):
            if self.current_token == 'stringlit':
                self.advance()
            elif self.current_token in self.follow("prompt"):
                return
    
    ####################### END OF ID PROD STATEMENTS #######################
    
    def unary_pre_statement(self):
        if self.i < len(self.tokens):
            if self.current_token in ['++', '--']:
                self.unary_op()
                if 'id' in self.current_token:
                    self.advance()
                    if self.current_token == ';':
                        self.advance()
                    else:
                        self.error_missing_terminator()
                else:
                    self.error_missing_id_in_unary()



            

    def output_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == 'ilabas_po':
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.output_val()
                    if self.current_token == ')':
                        self.advance()
                        if self.current_token == ';':
                            self.advance()
                    else:
                        self.error_unclosed_parenthesis()
                else: 
                    self.error_missing_paren_output()
            else:
                self.error_invalid_declaration()
    
    def output_val(self):
        if self.i < len(self.tokens):
            if 'id' in self.current_token:
                self.advance()
            elif self.current_token in ['charlit', 'boollit']:
                self.other_values()
            elif self.current_token in ['(', '!', '-', 'floatlit', '++', '--', 'intlit', 'stringlit', 'strlen_po'] or 'id' in self.current_token:
                self.expression()
            elif self.current_token in self.follow("output_val"):
                return
            #else: #TODO: add error
            #    print("ERROR: Invalid output value")

    def conditional_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == "kung_po":
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.condition()
                    if self.current_token == ')':
                        self.advance()
                        if self.current_token == '{':
                            self.advance()
                            self.statement()
                            self.okayapo_statement()
                            self.kundipo_statement()
                            if self.current_token == '}':
                                self.advance()
                                self.okayapo_statement()
                                self.kundipo_statement()
                            else:
                                self.error_unclosed_curly_brace()
                        else: 
                            self.error_missing_curly_brace_conditional()
                    else:
                        self.error_unclosed_parenthesis()
                else: 
                    self.error_missing_paren_conditional()

            if self.current_token == "mamili_po":
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    if 'id' in self.current_token:
                        self.advance()
                        if self.current_token == ')':
                            self.advance()
                            if self.current_token == '{':
                                self.advance()
                                self.switch_body()
                                if self.current_token == '}':
                                    self.advance()
                                else:
                                    self.error_unclosed_curly_brace()
                            else:
                                self.error_missing_curly_brace_conditional()
                        else:
                            self.error_unclosed_parenthesis()
                    else:
                        self.error_missing_id_in_switch()



            #else: #TODO: add error
            #    print("ERROR: Invalid conditional statement")
    
    def okayapo_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == "okaya_po":
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.condition()
                    if self.current_token == ')':
                        self.advance()
                        if self.current_token == '{':
                            self.advance()
                            self.statement()
                            if self.current_token == '}':
                                self.advance()
                                self.okayapo_statement()
                            else:
                                self.error_unclosed_curly_brace()
                        else:#TODO: add error
                            self.error_missing_paren_conditional()
                    else:
                        self.error_unclosed_curly_brace()
                else: #TODO: add error
                    self.error_missing_curly_brace_conditional()
                    
            
            elif self.current_token in self.follow("okayapo_statement"):
                return
        
    
    def kundipo_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == "kundi_po":
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.statement()
                    if self.current_token == '}':
                        self.advance()
                    else:
                        self.error_unclosed_curly_brace()
                else:#TODO: add error
                    self.error_missing_curly_brace_conditional()
            elif self.current_token in self.follow("kundipo_statement"):
                return

    def switch_body(self):
        if self.i < len(self.tokens):
            self.case()
            self.default()
            if self.current_token == 'default_po':
                self.error_multiple_default()
            
    def case(self):
        if self.i < len(self.tokens):
            if self.current_token == "sakali_po":
                self.advance()
                self.switch_val()
                if self.current_token == ':':
                    self.advance()
                    self.statement()
                    self.case_tail()
                    
                else: 
                    self.error_missing_colon()
            #else: #TODO: add error
            #    print("ERROR: Invalid case")
                    

    def switch_val(self):
        if self.i < len(self.tokens):
            if self.current_token == 'intlit':
                self.advance()
            elif self.current_token == 'charlit':
                self.advance()
            else: #TODO: add error
                #print("ERROR: Invalid switch value")
                self.error_invalid_switch_val()

    def tigil_po(self):
        if self.i < len(self.tokens):
            if self.current_token == 'tigil_po':
                self.advance()



    def case_tail(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("case_tail"):
                self.case()
                self.case_tail()
            elif self.current_token in self.follow("case_tail"):
                return
    
    def default(self):
        if self.i < len(self.tokens):
            if self.current_token == "default_po":
                self.advance()
                if self.current_token == ':':
                    self.advance()
                    self.statement()
                else:#TODO: add error
                    self.error_missing_colon()
            elif self.current_token in self.follow("default"):
                return
            
    def for_statement(self):
         if self.i < len(self.tokens):
            if self.current_token == "ulit_po":
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.initialization()
                    if self.current_token == ';':
                        self.advance()
                        self.for_condt()
                        if self.current_token == ';':
                            self.advance()
                            self.update()#4
                            if self.current_token == ')':
                                self.advance()
                                if self.current_token == '{':
                                    self.advance()
                                    self.statement()
                                    if self.current_token == '}':
                                        self.advance()
                                    else:
                                        self.error_unclosed_curly_brace()
                                else: #TODO: add errpr
                                    #print("ERROR: Expected '{'")
                                    self.error_missing_curly_brace_for()
                            else:
                                self.error_unclosed_parenthesis()
                        else:
                            self.error_missing_terminator()
                    else:
                        self.error_missing_terminator()
                else:#TODO: add error
                    #print("ERROR: Expected '('")
                    self.error_missing_paren_for()  
            else:
                self.error_invalid_declaration()
    
    def initialization(self):
        if self.i < len(self.tokens):
            if 'id' in self.current_token:
                self.advance()
                if self.current_token == '=':
                    self.advance()
                    if self.current_token == 'intlit':
                        self.advance()
                    elif 'id' in self.current_token:
                        self.id_prod()
                    else:
                        self.error_expecting_int_or_id()
                else: 
                    self.error_expecting_eq()
            else: #TODO: add error
                #print("ERROR: Expected Identifier")
                self.error_missing_id_init()
    
    def for_condt(self):
        if self.i < len(self.tokens):
            if self.current_token in ['(', '!', '-', 'floatlit', '++', '--', 'intlit'] or 'id' in self.current_token:
                self.condition()
            #else: #TODO: add error
            #    print("ERROR: Invalid condition")

    def update(self):
        if self.i < len(self.tokens):
            if self.current_token in self.first("unary") or self.next_token in self.first("unary"):
                self.unary()
            elif 'id' in self.current_token:
                self.advance()
                self.assign_op()
                self.update_val()
            #else: #TODO: add error
            #    print("ERROR: Invalid update")
    
    def update_val(self):
        if self.i < len(self.tokens):
            if 'id' in self.current_token :
                self.id_prod()
            elif self.current_token == 'intlit':
                self.advance()
            else: #TODO: add error
                print("ERROR: Invalid update value")

    def dowhile_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == 'gawin_po':
                self.advance()
                if self.current_token == '{':
                    self.advance()
                    self.statement()
                    if self.current_token == '}':
                        self.advance()
                        if self.current_token == "habang_po":
                            self.advance()
                            if self.current_token == '(':
                                self.advance()
                                self.condition()
                                if self.current_token == ')':
                                    self.advance()
                                    if self.current_token ==';':
                                        self.advance()
                                    else:
                                        self.error_missing_terminator()
                                else:
                                    self.error_unclosed_parenthesis()
                            else: #TODO: add error
                                #print("ERROR: Expected '('")
                                self.error_missing_paren_do_while()
                        else: #TODO: add error
                            #print("ERROR: Expected 'habang_po'")
                            self.error_missing_habang_po()
                    else:
                        self.error_unclosed_curly_brace()
                else: #TODO: add error
                    #print("ERROR: Expected '{'")
                    self.error_missing_curly_brace_do_while()
            #else: #TODO: add error
                #print("ERROR: Invalid do-while statement")


    #################### WHILE STATEMENT ###########################

    def while_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == 'habang_po':
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.condition()
                    if self.current_token == ')':
                        self.advance()
                        if self.current_token == '{':
                            self.advance()
                            self.statement()
                            if self.current_token == '}':
                                self.advance()
                            else:
                                self.error_unclosed_curly_brace()
                        else:
                            self.error_missing_curly_brace_while()
                    else:
                        self.error_unclosed_parenthesis()
                else:
                    self.error_missing_paren_while()
                        
                
    def condition(self):
        if self.i < len(self.tokens):
            self.rel_arith_logic_expr()


    def control_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == 'tigil_po':
                self.tigil_po()
                if self.current_token == ';':
                    self.advance()
                else:
                    self.error_missing_terminator()
            elif self.current_token == 'tuloy_po':
                self.advance()
                if self.current_token == ';':
                    self.advance()
                else:
                    self.error_missing_terminator()
            
################ END OF STATEMENT CFG ############################# END OF STATEMENT CFG ############################# END OF STATEMENT CFG ############################# END OF STATEMENT CFG #############################


    def func_definition(self):
        if self.i < len(self.tokens):
            if self.current_token == '#':
                self.advance()
                self.func_type()
                if 'id' in self.current_token:
                    self.advance()
                    if self.current_token == '(':
                        self.advance()
                        self.parameter()
                        if self.current_token == ')':
                            self.advance()
                            self.func_body()
                            self.func_definition_tail()
                        else:
                            self.error_unclosed_parenthesis()
                    else:
                        self.error_missing_paren_func_def()
                else:
                    self.error_missing_id_in_func_def()

    def func_body(self):
        if self.i < len(self.tokens):
            if self.current_token == '{':
                self.advance()
                self.statement()
                self.ibalikpo_statement() #must be included in statements
                if self.current_token == '}':
                    self.advance()
                else:
                    self.error_unclosed_curly_brace()
            else:
                self.error_missing_curly_brace_func_def()
                

    def ibalikpo_statement(self):
        if self.i < len(self.tokens):
            if self.current_token == 'ibalik_po':
                self.advance()
                if self.current_token == '(':
                    self.advance()
                    self.ibalikpo_val()
                    self.ibalik_po_tail()
                    if self.current_token == ')':
                        self.advance()
                        if self.current_token == ';':
                            self.advance()
                        else:
                            self.error_missing_terminator()
                    else:
                        self.error_unclosed_parenthesis()
                else:
                    self.error_missing_paren_ibp()

    def ibalikpo_val(self):
        if self.i < len(self.tokens):
            if self.current_token in ['charlit', 'boollit']:
                self.other_values()
            elif self.current_token in ['(', '!', '-', 'floatlit', '++', '--', 'intlit', 'stringlit', 'strlen_po'] or 'id' in self.current_token: #first set of expression
                self.expression()

    def ibalik_po_tail(self):
        if self.i < len(self.tokens):
            if self.current_token == ',':
                self.advance()
                self.ibalikpo_val()
                self.ibalik_po_tail()
            elif self.current_token == ')':
                return
    
    def func_definition_tail (self):
        if self.i < len(self.tokens):
            if self.current_token == '#':
                self.func_definition()
            else:
                return
            


    ##ERRORS
    def error_missing_simula_po (self):
        self.synErrors.append(Error("MISSING 'simula_po'", 
                                    f"Missing 'simula_po' declaration.", self.lexer_output))
    
    def error_missing_wakas_po (self):
        self.synErrors.append(Error("MISSING 'wakas_po'", 
                                    f"Missing 'wakas_po' declaration.", self.lexer_output))
    
    def error_after_wakas_po(self):
        self.synErrors.append(Error("INVALID STATEMENT", 
                                    f"Only function definition is allowed after 'wakas_po' statement. Any other statement is prohibited.", self.lexer_output))

    def self_invalid_global_dec(self):
        self.synErrors.append(Error("INVALID GLOBAL DECLARATION", 
                                    f"'{self.current_token}' is not a valid word for global declaration.", self.lexer_output))

    def error_invalid_declaration(self):
        self.synErrors.append(Error("INVALID DECLARATION", 
                                    f"Invalid declaration inside 'simula_po'.", self.lexer_output))

    def error_missing_terminator(self):
        self.synErrors.append(Error("MISSING TERMINATOR", 
                                    f"Expected ';' to terminate the statement, got '{self.current_token}'.", self.lexer_output))

    def error_expecting_value(self):
        self.synErrors.append(Error("MISSING VALUE", 
                                    f"Expecting a value for declaration.", self.lexer_output))
    
    def error_missing_id_in_dec(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in declaration, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_separator (self):
        self.synErrors.append(Error("MISSING SEPARATOR", 
                                    f"Expected ',' but got '{self.current_token}'.", self.lexer_output))
        
    
    def error_invalid_value_int_dec(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for int_po declaration. Expecting 'int_po' type.", self.lexer_output))
    
    def error_expected_initializer(self):
        self.synErrors.append(Error("MISSING INITIALIZER", 
                                    f"Expected initializer before '{self.current_token}' token", self.lexer_output))

    def error_unclosed_parenthesis (self):
        self.synErrors.append(Error("UNCLOSED PARENTHESIS", 
                                    f"Expected ')' to close the parenthesis, got '{self.current_token}'.", self.lexer_output))
        
    def missing_arithmetic_op(self):
        self.synErrors.append(Error("MISSING ARITHMETIC OPERATOR", 
                                    f"Expected arithmetic operator but got '{self.current_token}'.", self.lexer_output))
        
    def error_unclosed_square_bracket(self):
        self.synErrors.append(Error("UNCLOSED SQUARE BRACKET", 
                                    f"Expected ']' to close the square bracket, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_array_index(self):
        self.synErrors.append(Error("ARRAY INDEX ERROR", 
                                    f"Invalid array index. Expected 'int_po' type for array index", self.lexer_output))
    
    def error_missing_id_in_struct_access(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in accessing struct member, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_value_arithmetic(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for arithmetic expression. Expecting 'int_po' or 'float_po' type." , self.lexer_output))
    
    def error_missing_paren_strlen(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for strlen_po function, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_value_strlen(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for strlen_po function. Expecting 'str_po' type." , self.lexer_output))

    def error_expecting_int(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Expecting 'int_po' value.", self.lexer_output))

    def error_array_size(self):
        self.synErrors.append(Error("ARRAY SIZE ERROR", 
                                    f"Invalid array size. Expected 'int_po' type for array size.", self.lexer_output))
    
    def error_unclosed_curly_brace(self):
        self.synErrors.append(Error("UNCLOSED CURLY BRACE", 
                                    f"Expected '}}' to close the curly brace, got '{self.current_token}'.", self.lexer_output))

    def error_missing_curly_brace_array(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' to declare array members, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_array_dec(self):
        self.synErrors.append(Error("INVALID ARRAY DECLARATION", 
                                    f"Invalid array declaration. Expected array members", self.lexer_output))
    
    def error_invalid_data_type_int_dec(self):
        self.synErrors.append(Error("INVALID DATA TYPE", 
                                    f"Invalid data type for int_po declaration. Expecting 'int_po' type.", self.lexer_output))
    
    def error_unexpected_curly_brace(self):
        self.synErrors.append(Error("UNEXPECTED CURLY BRACE", 
                                    f"Unexpected '{{' in 1D array declaration.", self.lexer_output))
    
    def error_missing_paren_logical(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for logical expression, got '{self.current_token}'.", self.lexer_output)) 
    
    def error_expected_data_type(self):
        self.synErrors.append(Error("MISSING DATA TYPE", 
                                    f"Expected data type for 'lagi_po' declaration.", self.lexer_output))
    
    def error_invalid_logical_op(self):
        self.synErrors.append(Error("INVALID LOGICAL OPERATOR", 
                                    f"Invalid logical operator.", self.lexer_output))

    def error_invalid_relational_op(self):
        self.synErrors.append(Error("INVALID RELATIONAL OPERATOR", 
                                    f"Invalid relational operator.", self.lexer_output))
        
    def error_missing_sep_ter(self):
        self.synErrors.append(Error("MISSING SEPARATOR/TERMINATOR", 
                                    f"Expected ',' or ';' before {self.current_token}.", self.lexer_output))

    def error_expecting_value_kons_dec(self):
        self.synErrors.append(Error("MISSING VALUE", 
                                    f"Expecting value for 'lagi_po' declaration.", self.lexer_output))

    def error_missing_sep_curl(self):
        self.synErrors.append(Error("MISSING SEPARATOR/CURLY BRACE", 
                                    f"Expected ',' or '}}' before {self.current_token}.", self.lexer_output))
        
    def error_missing_sep_arr(self):
        self.synErrors.append(Error("MISSING SEPARATOR", 
                                    f"Expected ',' to separate array members.", self.lexer_output))

    def error_invalid_value_strcont(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for string concatenation. Expecting 'str_po' type.", self.lexer_output))
    
    def error_invalid_value_float_dec(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for float_po declaration. Expecting 'float_po' type.", self.lexer_output))

    def error_invalid_data_type_float_dec(self):
        self.synErrors.append(Error("INVALID DATA TYPE", 
                                    f"Invalid data type for float_po declaration. Expecting 'float_po' type.", self.lexer_output))
        
    def error_invalid_value_bool_dec(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for bool_po declaration. Expecting 'bool_po' type.", self.lexer_output))
    
    def error_invalid_data_type_bool_dec(self):
        self.synErrors.append(Error("INVALID DATA TYPE", 
                                    f"Invalid data type for bool_po declaration. Expecting 'bool_po' type.", self.lexer_output))
    
    def error_invalid_value_char_dec(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for char_po declaration. Expecting 'char_po' type.", self.lexer_output))
    
    def error_invalid_data_type_char_dec(self):
        self.synErrors.append(Error("INVALID DATA TYPE", 
                                    f"Invalid data type for char_po declaration. Expecting 'char_po' type.", self.lexer_output))
    
    def error_invalid_value_str_dec(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for str_po declaration. Expecting 'str_po' type.", self.lexer_output))
    
    def error_invalid_data_type_str_dec(self):
        self.synErrors.append(Error("INVALID DATA TYPE", 
                                    f"Invalid data type for str_po declaration. Expecting 'str_po' type.", self.lexer_output))
    

    def error_missing_paren_func(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for function declaration, got '{self.current_token}'.", self.lexer_output))

    def error_missing_id_in_func(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in function declaration, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_data_type_func(self):
        self.synErrors.append(Error("MISSING DATA TYPE", 
                                    f"Expected data type in function declaration.", self.lexer_output))

    def error_missing_id_in_parameter(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in parameter of a function, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_sep_par(self):
        self.synErrors.append(Error("MISSING SEPARATOR/PARENTHESIS", 
                                    f"Expected ',' or ')' before {self.current_token}", self.lexer_output))
    
    def error_missing_curly_brace_struct(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' to declare 'estruktura_po' members, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_id_in_struct_dec(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in 'estruktura_po' declaration, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_terminator_struct(self):
        self.synErrors.append(Error("MISSING TERMINATOR", 
                                    f"Expected ';' to terminate 'estruktura_po' declaration, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_statement(self):
        self.synErrors.append(Error("INVALID STATEMENT", 
                                    f"Invalid statement inside 'simula_po, got '{self.current_token}'", self.lexer_output))
    
    def error_invalid_id_only(self):
        self.synErrors.append(Error("INVALID STATEMENT", 
                                    f"Identifier is not a valid statement. Expecting other tokens", self.lexer_output))
    
    def error_missing_value_assign(self):
        self.synErrors.append(Error("MISSING VALUE", 
                                    f"Expecting value for assignment statement.", self.lexer_output))
    
    def error_missing_paren_input(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for input statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_curly_brace_while(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' to declare while statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_while(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for while statement condition, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_func_def(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for function definition, got '{self.current_token}'.", self.lexer_output))

    def error_missing_id_in_func_def(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in function definition, got '{self.current_token}'.", self.lexer_output))
    
    def error_unclosed_curly_brace_func_def(self):
        self.synErrors.append(Error("UNCLOSED CURLY BRACE", 
                                    f"Expected '}}' to close the function definition, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_curly_brace_func_def(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' for function definition, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_ibp(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for 'ibalik_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_output(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for output statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_curly_brace_conditional(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' for conditional statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_conditional(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for conditional statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_id_in_switch(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier in 'mamili_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_expected_tigil_po(self):
        self.synErrors.append(Error("MISSING 'tigil_po'", 
                                    f"Expected 'tigil_po' keyword in switch-case.", self.lexer_output))
    
    def error_missing_colon(self):
        self.synErrors.append(Error("MISSING COLON", 
                                    f"Expected ':' in switch-case statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_invalid_switch_val(self):
        self.synErrors.append(Error("INVALID SWITCH VALUE", 
                                    f"Invalid value for switch-case statement.", self.lexer_output))
    
    def error_missing_curly_brace_for(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' for 'ulit_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_for(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for 'ulit_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_expecting_eq(self):
        self.synErrors.append(Error("MISSING EQUAL SIGN", 
                                    f"Expected '=' for ulit_po' initialization, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_id_init(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier for 'ulit_po' initialization, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_paren_do_while(self):
        self.synErrors.append(Error("MISSING PARENTHESIS", 
                                    f"Expected '(' for 'gawin_po-habang_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_habang_po(self):
        self.synErrors.append(Error("MISSING 'habang_po'", 
                                    f"Expected 'habang_po' for 'gawin_po-habang_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_curly_brace_do_while(self):
        self.synErrors.append(Error("MISSING CURLY BRACE", 
                                    f"Expected '{{' for 'gawin_po-habang_po' statement, got '{self.current_token}'.", self.lexer_output))
    
    def error_missing_data_type_func_def(self):
        self.synErrors.append(Error("MISSING DATA TYPE", 
                                    f"Expected data type for function definition.", self.lexer_output))
    
    def error_reserved_word_in_dec(self):
        self.synErrors.append(Error("INVALID IDENTIFIER", 
                                    f"The reserved word '{self.next_token}' cannot be used as an identifier.", self.lexer_output))
        
    def error_missing_assignment(self):
        self.synErrors.append(Error("MISSING INITIALIZATION", 
                                    f"Invalid variable declaration. Expected initialization value before '{self.current_token}' token", self.lexer_output))
    
    def error_missing_kung_po(self):
        self.synErrors.append(Error("MISSING 'kung_po'", 
                                    f"Expected 'kung_po' before '{self.current_token}' statement.", self.lexer_output))

    def error_expecting_int_or_id(self):
        self.synErrors.append(Error("INVALID VALUE", 
                                    f"Invalid value for initialization. Expecting 'int_po' type or identifier, got '{self.current_token}'", self.lexer_output))
    
    def error_multiple_default(self):
        self.synErrors.append(Error("MULTIPLE 'default_po'", 
                                    f"Only one 'default_po' case is allowed in one 'mamili_po' statement.", self.lexer_output))
    
    def error_invalid_struct_body(self):
        self.synErrors.append(Error("INVALID STRUCTURE DECLARATION", 
                                    f"Expected data type in declaring 'estruktura_po' members, got '{self.current_token}'", self.lexer_output))
    
    def error_invalid_operand_in_rel(self):
        self.synErrors.append(Error("INVALID OPERAND", 
                                    f"'{self.current_token}' is not a valid operand in relational expression.", self.lexer_output))
    
    def error_missing_operand(self):
        self.synErrors.append(Error("MISSING OPERAND", 
                                    f"Missing operand before '{self.current_token}' token", self.lexer_output))
    
    def error_missing_id_in_unary(self):
        self.synErrors.append(Error("MISSING IDENTIFIER", 
                                    f"Expected identifier for unary operation, got '{self.current_token}'", self.lexer_output))