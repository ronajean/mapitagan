import string

class CodeTokenizer:
    def __init__(self):
        self.reg_def = {
            'sero_digyit': ['-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            'Letra': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ''],
            'letra': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'],
            'numero': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
            'negatibo':  ['-9', '-8', '-7', '-6', '-5', '-4', '-3', '-2', '-1']
        }

        self.reserved_words = ['bool_po','char_po','default_po','float_po','gawin_po', 
                  'habang_po','ibalik_po','int_po','ilabas_po', 'kundi_po','kung_po',
                  'magpasok_po','mali_po','okaya_po','sakali_po','simula_po',
                  'str_po','totoo_po','tigil_po','lagi_po','_ni_','tuloy_po',
                  'wala_po','wakas_po','mamili_po','ulit_po','estruktura_po','strlen_po']
 

    def validate_char_literal(self,lexeme):
        # Remove trailing whitespace before validating char literals
        lexeme = lexeme.strip()
        # Validate char literals
        if lexeme.startswith("'") and lexeme.endswith("'") and len(lexeme) == 3 and lexeme[1].isprintable():
            return lexeme
        elif ')' in lexeme or ';' in lexeme or '\n' in lexeme:
            return None  # Return None for invalid char literals
        else:
            return None

    def validate_string_literal(self,lexeme): #bawal kunin next line
        # Remove trailing whitespace before validating string literals
        lexeme = lexeme.strip()
        # Validate string literals
        if lexeme.startswith('"') and lexeme.endswith('"') and '\n' not in lexeme and lexeme.count('\\"') % 2 == 0:
            new_lexeme = lexeme.replace(r"\n", "\n").replace(r"\t", "\t")
            print("hi")
            return new_lexeme
        elif ')' in lexeme or ';' in lexeme or '\n' in lexeme:
            return None
    
 
    def tokenize_code(self, input_code):
        tokens = []
        errors=[]
        i = 0
        illegal_chars = '©☺☻♥♦♣♠•◘○◙♂♀♪♫☼►◄↕‼¶§▬↨↑↓→←∟↔▲^~▼©?@$¥€•'
        identifier_dict = {}
        identifier_counter = 1
        code_length = len(input_code)
        line_number = 1

        while i < code_length:
            current_char = input_code[i]
            if current_char == '\n':
                line_number += 1
                i += 1
                continue 

            if current_char.islower(): #identifiers
                j = i
                lexeme = input_code[i:j]
                if input_code[j] not in [' ','\n',';','(',')','[',']','{','}',',','+','-','*','/','%','=','>','<','!','|','&',':']:
                    while (j < code_length and len(lexeme) <= 31):
                        if input_code[j:j+4] == '_ni_':  # Check for '_ni_'
                            if lexeme:  # If there's a lexeme before '_ni_', add it as a token
                                tokens.append([lexeme, f"id{identifier_counter}", line_number])
                                identifier_counter += 1
                                lexeme = ''
                            tokens.append(['_ni_', '_ni_', line_number])
                            j += 4  # Skip past '_ni_'
                        elif (input_code[j].islower() or input_code[j].isdigit()) and input_code[j].isalnum() or input_code[j] == '_':
                            lexeme += input_code[j]
                            j += 1
                        else:
                            break
                    if lexeme not in self.reserved_words:
                        if j < len(input_code) and input_code[j] in [' ', '+', '-', '*', '/', '%', '&', '|', '>', '<', '=', '}', '.', ',', ';', ']', '!', '(', ')', '[', '{']: #iddelim
                            if lexeme not in identifier_dict:
                                identifier_dict[lexeme] = f"id{identifier_counter}"
                                identifier_counter += 1
                            tokens.append([lexeme,str(identifier_dict[lexeme]), line_number])
                            lexeme = input_code[i:j]
                            i = j-1
                        elif j < len(input_code) and input_code[j] not in ['*',' ', ';', '=','(',')',',']:
                            inv = ''
                            inv = input_code[j]
                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                            lexeme = input_code[i:j]
                            i = j - 1
                        else:
                            pass
                    else:
                        pass
                else:
                    inv = ''
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                    lexeme = input_code[i:j]
                    i = j - 1
                    
            if current_char.isupper(): #illegal character
                j = i + 1
                lexeme = input_code[i:j]  # Initialize lexeme with current_char
                errors.append([f"Lexical Error:\t\tInvalid letter case", lexeme, line_number])
                i +=1 
                continue
            
            if current_char in illegal_chars:
                errors.append([f"Lexical Error:\t\tIllegal character ({current_char})", "", line_number])
                i += 1
                continue
            
            if current_char == '_': #_ni_
                j = i + 1
                if input_code[j] == 'n':
                    j += 1
                    if input_code[j] == 'i':
                        j += 1   
                        if input_code[j] == '_':
                            j += 1
                            lexeme = input_code[i:j]                                 
                            if j < len(input_code) and (input_code[j] in [' ','*'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']): # temporary delim
                                lexeme = input_code[i:j]    
                                tokens.append([lexeme, lexeme, line_number])
                                i = j - 1
                            else:
                                i = j
                                inv = ''
                                inv = input_code[j]
                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                i = j - 1
                        else:
                            lexeme = input_code[i:j]  # Initialize lexeme with current_char
                            while j < code_length and (input_code[j] not in [' ','n','i','_']):
                                lexeme += input_code[j]
                                j += 1        
                            if lexeme not in self.reserved_words and lexeme not in tokens:
                                errors.append([f"Lexical Error:\t\tInvalid starting character (_) for identifier", lexeme, line_number])
                                i = j 
                                continue
                            else:
                                pass
                    else:
                        lexeme = input_code[i:j]  # Initialize lexeme with current_char
                        while j < code_length and (input_code[j] not in [' ','n','i','_']):
                            lexeme += input_code[j]
                            j += 1
                        
                        if lexeme not in self.reserved_words and lexeme not in tokens:
                            errors.append([f"Lexical Error:\t\tInvalid starting character (_) for identifier", lexeme, line_number])
                            i = j 
                            continue
                        else:
                            pass
                else:
                    lexeme = input_code[i:j]  # Initialize lexeme with current_char
                    while j < code_length and (input_code[j] not in [' ','n','i','_']):
                        lexeme += input_code[j]
                        j += 1
                    
                    if lexeme not in self.reserved_words and lexeme not in tokens:
                        errors.append([f"Lexical Error:\t\tInvalid starting character (_) for identifier", lexeme, line_number])
                        i = j 
                        continue
                    else:
                        pass


            if current_char == 'b':  #bool_po
                j = i + 1
                if j < len(input_code) and input_code[j] == 'o':
                    j += 1
                    if j < len(input_code) and input_code[j] == 'o':
                        j += 1
                        if j < len(input_code) and input_code[j] == 'l':
                            j += 1
                            if j < len(input_code) and input_code[j] == '_':
                                j += 1
                                if j < len(input_code) and input_code[j] == 'p':
                                    j += 1
                                    if j < len(input_code) and input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j] 
                                        if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                            tokens.append([lexeme, lexeme,line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1

            elif current_char == 'c':  #char_po
                j = i + 1            
                if j < len(input_code) and input_code[j] == 'h':
                    j += 1                 
                    if input_code[j] == 'a':
                        j += 1                     
                        if input_code[j] == 'r':
                            j += 1                         
                            if input_code[j] == '_':
                                j += 1                             
                                if input_code[j] == 'p':
                                    j += 1                                 
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j] 
                                        if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                            lexeme = input_code[i:j] 
                                            tokens.append([lexeme, lexeme, line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1

            elif current_char == 'd':  #default_po:
                j = i + 1
                if input_code[j] == 'e':
                    j += 1
                    if input_code[j] == 'f':
                        j += 1
                        if input_code[j] == 'a':
                            j += 1
                            if input_code[j] == 'u':
                                j += 1
                                if input_code[j] == 'l':
                                    j += 1
                                    if input_code[j] == 't':
                                        j += 1
                                        if input_code[j] == '_':
                                            j += 1
                                            if input_code[j] == 'p':
                                                j += 1
                                                if input_code[j] == 'o':
                                                    j += 1
                                                    lexeme = input_code[i:j] 
                                                    if j < len(input_code) and input_code[j] in ['*',' ',':']: #delim22
                                                        lexeme = input_code[i:j]
                                                        tokens.append([lexeme, lexeme, line_number])
                                                        i = j - 1
                                                    else:
                                                        i = j
                                                        inv = ''
                                                        inv = input_code[j]
                                                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                        i = j - 1

            elif current_char == 'e': #estruktura_po
                j = i + 1 
                if input_code[j] == 's':
                    j += 1                 
                    if input_code[j] == 't':
                        j += 1                     
                        if input_code[j] == 'r':
                            j += 1                         
                            if input_code[j] == 'u':
                                j += 1                             
                                if input_code[j] == 'k':
                                    j += 1                                 
                                    if input_code[j] == 't':
                                        j += 1                                    
                                        if input_code[j] == 'u':
                                            j += 1
                                            if input_code[j] == 'r':
                                                j += 1
                                                if input_code[j] == 'a':
                                                    j += 1
                                                    if input_code[j] == '_':
                                                        j += 1
                                                        if input_code[j] == 'p':
                                                            j += 1
                                                            if input_code[j] == 'o':
                                                                j += 1
                                                                lexeme = input_code[i:j] 
                                                                if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                                                    lexeme = input_code[i:j]
                                                                    tokens.append([lexeme, lexeme, line_number])
                                                                    i = j - 1
                                                                else:
                                                                    i = j
                                                                    inv = ''
                                                                    inv = input_code[j]
                                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                                    i = j - 1

                                                

            elif current_char == 'f':  #float_po
                j = i + 1            
                if input_code[j] == 'l':
                    j += 1                 
                    if input_code[j] == 'o':
                        j += 1                     
                        if input_code[j] == 'a':
                            j += 1                         
                            if input_code[j] == 't':
                                j += 1                             
                                if input_code[j] == '_':
                                    j += 1                                 
                                    if input_code[j] == 'p':
                                        j += 1                                    
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmt
                                                lexeme = input_code[i:j] 
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1
                    
            elif current_char == 'g':  #gawin_po
                j = i + 1            
                if input_code[j] == 'a':
                    j += 1                 
                    if input_code[j] == 'w':
                        j += 1                     
                        if input_code[j] == 'i':
                            j += 1                         
                            if input_code[j] == 'n':
                                j += 1                             
                                if input_code[j] == '_':
                                    j += 1                                 
                                    if input_code[j] == 'p':
                                        j += 1                                    
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ', '\n', '{']: #delim2
                                                lexeme = input_code[i:j]
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1

            elif current_char == 'h':  #habang_po
                j = i + 1            
                if input_code[j] == 'a':
                    j += 1                 
                    if input_code[j] == 'b':
                        j += 1                     
                        if input_code[j] == 'a':
                            j += 1                         
                            if input_code[j] == 'n':
                                j += 1                             
                                if input_code[j] == 'g':
                                    j += 1                                 
                                    if input_code[j] == '_':
                                        j += 1                                    
                                        if input_code[j] == 'p':
                                            j += 1                                         
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]  
                                                if j < len(input_code) and input_code[j] in ['*',' ','(']: #delim3
                                                    lexeme = input_code[i:j]
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1

            elif current_char == 'i':  #ibalik_po
                j = i + 1            
                if input_code[j] == 'b':
                    j += 1                 
                    if input_code[j] == 'a':
                        j += 1                     
                        if input_code[j] == 'l':
                            j += 1                         
                            if input_code[j] == 'i':
                                j += 1                             
                                if input_code[j] == 'k':
                                    j += 1                                 
                                    if input_code[j] == '_':
                                        j += 1                                    
                                        if input_code[j] == 'p':
                                            j += 1                                         
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]  
                                                if j < len(input_code) and input_code[j] in ['*',' ', ';', '(']: #delim4
                                                    lexeme = input_code[i:j]
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1
                                                    
                elif input_code[j] == 'n': #int_po
                    j += 1                 
                    if input_code[j] == 't':
                        j += 1                     
                        if input_code[j] == '_':
                            j += 1                        
                            if input_code[j] == 'p':
                                j += 1                             
                                if input_code[j] == 'o':
                                    j += 1
                                    lexeme = input_code[i:j]  
                                    if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                        lexeme = input_code[i:j]
                                        tokens.append([lexeme, lexeme, line_number])
                                        i = j - 1
                                    else:
                                        i = j
                                        inv = ''
                                        inv = input_code[j]
                                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                        i = j - 1
                                     

                elif input_code[j] == 'l': #ilabas_po
                    j += 1                 
                    if input_code[j] == 'a':
                        j += 1                     
                        if input_code[j] == 'b':
                            j += 1                        
                            if input_code[j] == 'a':
                                j += 1                             
                                if input_code[j] == 's':
                                    j += 1                                
                                    if input_code[j] == '_':
                                        j += 1                                    
                                        if input_code[j] == 'p':
                                            j += 1                                        
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]    
                                                if j < len(input_code) and input_code[j] in ['*',' ', '(']: #delim3
                                                    lexeme = input_code[i:j] 
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1
                                                                                 
            elif current_char == 'k': #kundi_po or else
                j = i + 1                        
                if input_code[j] == 'u':
                    j += 1
                    if input_code[j] == 'n':
                        j += 1
                        if input_code[j] == 'd':
                            j += 1
                            if input_code[j] == 'i':
                                j += 1
                                if input_code[j] == '_':
                                    j += 1
                                    if input_code[j] == 'p':
                                        j += 1
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ', '\n', '{']: #delim2
                                                lexeme = input_code[i:j] 
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1

                        elif input_code[j] == 'g': #kung_po or if
                            j += 1
                            if input_code[j] == '_':
                                j += 1
                                if input_code[j] == 'p':
                                    j += 1
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j] 
                                        if j < len(input_code) and input_code[j] in ['*',' ', '(']: #delim3
                                            lexeme = input_code[i:j] 
                                            tokens.append([lexeme, lexeme, line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1

            elif current_char == 'l': #lagi_po
                j = i + 1
                if input_code[j] == 'a':
                    j += 1
                    if input_code[j] == 'g':
                        j += 1
                        if input_code[j] == 'i':
                            j += 1
                            if input_code[j] == '_':
                                j += 1
                                if input_code[j] == 'p':
                                    j += 1
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j] 
                                        if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                            lexeme = input_code[i:j] 
                                            tokens.append([lexeme, lexeme, line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1


            elif current_char == 'm':  #magpasok_po or input
                j = i + 1
                if input_code[j] == 'a':
                    j += 1
                    if input_code[j] == 'g':
                        j += 1
                        if input_code[j] == 'p':
                            j += 1
                            if input_code[j] == 'a':
                                j += 1
                                if input_code[j] == 's':
                                    j += 1
                                    if input_code[j] == 'o':
                                        j += 1
                                        if input_code[j] == 'k':
                                            j += 1
                                            if input_code[j] == '_':
                                                j += 1
                                                if input_code[j] == 'p':
                                                    j += 1
                                                    if input_code[j] == 'o':
                                                        j += 1
                                                        lexeme = input_code[i:j]  
                                                        if j < len(input_code) and input_code[j] in ['*',' ', '(']: #delim3
                                                            lexeme = input_code[i:j] 
                                                            tokens.append([lexeme, lexeme, line_number])
                                                            i = j - 1
                                                        else:
                                                            i = j
                                                            inv = ''
                                                            inv = input_code[j]
                                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                            i = j - 1
                    
                    elif input_code[j] == 'l': #mali_po
                        j += 1
                        if input_code[j] == 'i':
                            j += 1
                            if input_code[j] == '_':
                                j += 1
                                if input_code[j] == 'p':
                                    j += 1
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j]
                                        if j < len(input_code) and input_code[j] in [' ','*',')',';',',']: #delim5
                                            lexeme = input_code[i:j]
                                            tokens.append([lexeme, 'boollit', line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1

                    elif input_code[j] == 'm': #mamili_po
                        j += 1
                        if input_code[j] == 'i':
                            j += 1
                            if input_code[j] == 'l':
                                j += 1
                                if input_code[j] == 'i':
                                    j += 1
                                    if input_code[j] == '_':
                                        j += 1
                                        if input_code[j] == 'p':
                                            j += 1
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]  
                                                if j < len(input_code) and input_code[j] in ['*',' ', '(']: #delim3
                                                    lexeme = input_code[i:j] 
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1

            elif current_char == 'o':  #okaya_po or if else
                j = i + 1
                if input_code[j] == 'k':
                    j += 1
                    if input_code[j] == 'a':
                        j += 1
                        if input_code[j] == 'y':
                            j += 1
                            if input_code[j] == 'a':
                                j += 1
                                if input_code[j] == '_':
                                    j += 1
                                    if input_code[j] == 'p':
                                        j += 1
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ', '(']: #delim3
                                                lexeme = input_code[i:j]
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1


            elif current_char == 's':  #sakali_po or case
                j = i + 1
                if input_code[j] == 'a':
                    j += 1
                    if input_code[j] == 'k':
                        j += 1
                        if input_code[j] == 'a':
                            j += 1
                            if input_code[j] == 'l':
                                j += 1
                                if input_code[j] == 'i':
                                    j += 1
                                    if input_code[j] == '_':
                                        j += 1
                                        if input_code[j] == 'p':
                                            j += 1
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j] 
                                                if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                                    lexeme = input_code[i:j] 
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1

                elif input_code[j] == 'i':  #simula_po
                    j += 1                
                    if input_code[j] == 'm':
                        j += 1                     
                        if input_code[j] == 'u':
                            j += 1                         
                            if input_code[j] == 'l':
                                j += 1                             
                                if input_code[j] == 'a':
                                    j += 1                                 
                                    if input_code[j] == '_':
                                        j += 1                                     
                                        if input_code[j] == 'p':
                                            j += 1                                        
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]
                                                if j < len(input_code) and input_code[j] in ['*','\n']: #delim1
                                                    lexeme = input_code[i:j] 
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1
                                                          
                elif input_code[j] == 't':  #str_po
                    j += 1                
                    if input_code[j] == 'r':
                        j += 1                     
                        if input_code[j] == '_':
                            j += 1                         
                            if input_code[j] == 'p':
                                j += 1                             
                                if input_code[j] == 'o':
                                    j += 1
                                    lexeme = input_code[i:j]
                                    if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                        lexeme = input_code[i:j] 
                                        tokens.append([lexeme, lexeme, line_number])
                                        i = j - 1
                                    else:
                                        i = j
                                        inv = ''
                                        inv = input_code[j]
                                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                        i = j - 1
                        elif input_code[j] == 'l':  #strlen_po
                            j += 1                
                            if input_code[j] == 'e':
                                j += 1                     
                                if input_code[j] == 'n':
                                    j += 1                         
                                    if input_code[j] == '_':
                                        j += 1                             
                                        if input_code[j] == 'p':
                                            j += 1                                 
                                            if input_code[j] == 'o':
                                                j += 1
                                                lexeme = input_code[i:j]
                                                if j < len(input_code) and input_code[j] in ['*','(', ' ']: #delim3
                                                    lexeme = input_code[i:j] 
                                                    tokens.append([lexeme, lexeme, line_number])
                                                    i = j - 1
                                                else:
                                                    i = j
                                                    inv = ''
                                                    inv = input_code[j]
                                                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                    i = j - 1
                                                
            elif current_char == 't':  #tigil_po
                j = i + 1
                if input_code[j] == 'i':
                    j += 1
                    if input_code[j] == 'g':
                        j += 1
                        if input_code[j] == 'i':
                            j += 1
                            if input_code[j] == 'l':
                                j += 1
                                if input_code[j] == '_':
                                    j += 1
                                    if input_code[j] == 'p':
                                        j += 1
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ',';']: #delim23
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1

                elif input_code[j] == 'o':
                    j += 1                 
                    if input_code[j] == 't':
                        j += 1                     
                        if input_code[j] == 'o':
                            j += 1                         
                            if input_code[j] == 'o':
                                j += 1                             
                                if input_code[j] == '_':
                                    j += 1                                 
                                    if input_code[j] == 'p':
                                        j += 1                                    
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in [' ', '*', ')', ';',',']: #delim5
                                                lexeme = input_code[i:j] 
                                                tokens.append([lexeme, 'boollit', line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1                                

                elif input_code[j] == 'u': #tuloy_po
                    j += 1
                    if input_code[j] == 'l':
                        j += 1
                        if input_code[j] == 'o':
                            j += 1
                            if input_code[j] == 'y':
                                j += 1
                                if input_code[j] == '_':
                                    j += 1
                                    if input_code[j] == 'p':
                                        j += 1
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*',' ',';']: #delim23
                                                lexeme = input_code[i:j] 
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1

            elif current_char == 'u': #ulit_po
                j = i + 1
                if input_code[j] == 'l':
                    j += 1
                    if input_code[j] == 'i':
                        j += 1
                        if input_code[j] == 't':
                            j += 1
                            if input_code[j] == '_':
                                j += 1
                                if input_code[j] == 'p':
                                    j += 1
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j] 
                                        if j < len(input_code) and input_code[j] in ['*',' ','(']: #delim3
                                            lexeme = input_code[i:j]
                                            tokens.append([lexeme, lexeme, line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1
                
            elif current_char == 'w':  #wakas_po
                j = i + 1
                if input_code[j] == 'a':
                    j += 1
                    if input_code[j] == 'k':
                        j += 1
                        if input_code[j] == 'a':
                            j += 1
                            if input_code[j] == 's':
                                j += 1
                                if input_code[j] == '_':
                                    j += 1
                                    if input_code[j] == 'p':
                                        j += 1
                                        if input_code[j] == 'o':
                                            j += 1
                                            lexeme = input_code[i:j] 
                                            if j < len(input_code) and input_code[j] in ['*','\n']: #delim1
                                                lexeme = input_code[i:j] 
                                                tokens.append([lexeme, lexeme, line_number])
                                                i = j - 1
                                            else:
                                                i = j
                                                inv = ''
                                                inv = input_code[j]
                                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                                i = j - 1
                                    else:
                                        i = j
                                        inv = ''
                                        inv = input_code[j]
                                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                        i = j - 1
                              
                    elif input_code[j] == 'l':
                        j += 1                     
                        if input_code[j] == 'a':
                            j += 1                         
                            if input_code[j] == '_':
                                j += 1                             
                                if input_code[j] == 'p':
                                    j += 1                                 
                                    if input_code[j] == 'o':
                                        j += 1
                                        lexeme = input_code[i:j]                                 
                                        if j < len(input_code) and input_code[j] in ['*',' ']: #spacecmnt
                                            lexeme = input_code[i:j]    
                                            tokens.append([lexeme, lexeme, line_number])
                                            i = j - 1
                                        else:
                                            i = j
                                            inv = ''
                                            inv = input_code[j]
                                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                                            i = j - 1

            
            
           

            elif current_char == '+': 
                j = i + 1
                if (input_code[j] == '='): # +=
                    j+=1                              
                    lexeme = input_code[i:j]
                    if j < len(input_code) and (input_code[j] in [' ', '(', '-',';','*','"',"'"] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']): #delim8
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i=j-1
                    else:
                        inv = ''
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) #invalid delim for +=
                        i = j
                        i = j-1
                        
                elif input_code[j] == '+': # unary operator ++
                    j+=1                              
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',';',')',']'] or (input_code[j] in self.reg_def['numero']) or (input_code[j] in self.reg_def['letra']): #delim7
                        tokens.append([lexeme, lexeme, line_number])
                        i = j  
                        i = j-1
                    else:
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                        i = j  
                        i = j-1 #invalid delim for ++

                elif input_code[j] in [' ', '(','-','*','"',"'"] or (input_code[j] in self.reg_def['numero']) or (input_code[j] in self.reg_def['letra']):  #delim6
                    lexeme = input_code[i:j] # operator +
                    tokens.append([lexeme, lexeme, line_number])
                    i = j  
                    i = j-1

                else:
                    inv = ''
                    lexeme = input_code[i:j]
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) #invalid delim for +
                    i = j
                    i = j-1
            
    
            #Positive numbers
            elif current_char.isdigit():
                j = i
                lexeme = input_code[i:j]
                while (j < code_length and len(lexeme) <= 9) and input_code[j].isdigit():
                    lexeme += input_code[j]
                    j += 1

                if input_code[j]=='.':
                    decimal_part=''
                    lexeme += '.'
                    j += 1
                    while (j < code_length and len(decimal_part) < 5) and input_code[j].isdigit():
                        lexeme += input_code[j]
                        decimal_part += input_code[j]
                        j += 1
                    
                    #positive float literal
                    if len(decimal_part) <= 5: 
                        if j < len(input_code) and input_code[j] in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']: #numdelim
                            tokens.append([lexeme, "floatlit", line_number])
                            i = j
                            i = j - 1
                        elif j < len(input_code) and input_code[j] not in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']:
                            inv = ''
                            inv = input_code[j]
                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                            lexeme = input_code[i:j]
                            i = j - 1
                        else:
                            inv = input_code[j]
                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                            lexeme = input_code[i:j]
                            i = j - 1
                    else:
                        pass
                else: #positive int literal
                    if len(lexeme) <= 10: 
                        if j < len(input_code) and input_code[j] in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']: #numdelim
                            tokens.append([lexeme, "intlit", line_number])
                            i = j
                            i = j - 1
                        elif j < len(input_code) and input_code[j] not in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']:
                            inv = ''
                            inv = input_code[j]
                            errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                            lexeme = input_code[i:j]
                        i = j - 1
                    

            #negative symbol, negative int and float literal

            elif current_char == '-': 
                j = i + 1
                if input_code[j] == '=': # -=
                    j+=1                              
                    lexeme = input_code[i:j]
                    if j < len(input_code) and (input_code[j] in ['*',' ','(','+','"',"'"] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']): #delim8
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i=j-1
                    else:
                        inv = ''
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])  
                        i = j
                        i = j-1 #invalid delim for -=
                elif input_code[j] == '-': # unary operator --
                    j+=1                              
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',';',')',']'] or (input_code[j] in self.reg_def['numero']) or (input_code[j] in self.reg_def['letra']): #delim7
                        tokens.append([lexeme, lexeme, line_number])
                        i = j  
                        i = j-1
                    else:
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])
                        i = j  
                        i = j-1 #invalid delim for --
                
                elif input_code[j] in ['*',' ', '('] or (input_code[j] in self.reg_def['letra']):  #delim9 temporary
                    lexeme = input_code[i] 
                    if input_code[j] in ['*',' ', '('] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9 temporary
                        tokens.append([lexeme, lexeme, line_number])
                        i = j  
                        i = j-1      
                    else:
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1 
                
                elif input_code[j].isdigit():
                    lexeme = input_code[i:j]
                    while (j < code_length and len(lexeme) <= 10) and input_code[j].isdigit():
                        lexeme += input_code[j]
                        j+=1

                    if input_code[j]=='.': 
                        decimal_part=''
                        lexeme += '.'
                        j += 1
                        while (j < code_length and len(decimal_part) < 5) and input_code[j].isdigit():
                            lexeme += input_code[j]
                            decimal_part += input_code[j]
                            j += 1
                        
                        #negative float
                        if len(decimal_part) <= 5: 
                            if j < len(input_code) and input_code[j] in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']: #numdelim
                                tokens.append([lexeme, "floatlit", line_number])
                                i = j
                                i = j - 1
                            elif j < len(input_code) and input_code[j] not in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']:
                                inv = ''
                                inv = input_code[j]
                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                                lexeme = input_code[i:j]
                                i = j - 1
                            else:
                                inv = input_code[j]
                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                                lexeme = input_code[i:j]
                                i = j - 1
                        else:
                            pass
                    
                    #negative int
                    else:
                        if len(lexeme) <= 11: 
                            if j < len(input_code) and input_code[j] in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']: #numdelim
                                tokens.append([lexeme, "intlit", line_number])
                                i = j
                                i = j - 1
                            elif j < len(input_code) and input_code[j] not in ['*',';', '=', '/', '+', '-', '%', '>', '<', ']', ':', ')', '!', '}', ',',' ','|','&']:
                                inv = ''
                                inv = input_code[j]
                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token",lexeme,line_number])
                                lexeme = input_code[i:j]
                                i = j - 1
                        else:
                            pass
                
                                
            elif current_char == '*':
                j = i + 1
                lexeme = input_code[i:j]
                if j < code_length and (input_code[j] == '='):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for *=
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                elif j < code_length and (input_code[j] == '*'): #comment
                    j += 1
                    lexeme = input_code[i:j]
                    try:
                        while (j < code_length and input_code[j] != '*'):
                            lexeme += input_code[j]
                            j += 1
                            if input_code[j] == '\n':
                                line_number += 1
                                continue
                        if input_code[j] in ['*']:
                            j += 1
                            if input_code[j] in [' ','*','\n']:#spacenl
                                i = j - 1 
                            else:
                                inv = input_code[j]
                                errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for comment ",lexeme,line_number])
                                i = j
                        else: #invalid delim for comment **
                            inv = input_code[j]
                            errors.append([f"Lexical Error:\t\tInvalid comment ",lexeme,line_number])
                            i = j
                    except:
                        errors.append([f"Lexical Error:\t\tInvalid comment ",lexeme,line_number])
                        i = j
                elif input_code[j] in [' ', '(', '-','*'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                else: #invalid delim for *
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                    
            elif current_char == '/':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '(','-'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1 
                elif j < code_length and (input_code[j] == '='):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for /=
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else: #invalid delim for /
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                    
            elif current_char == '%':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '(', '-'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim9
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                else: #invalid delim for %
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                
            elif current_char == '<': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '(', '-', '\''] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim10
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                elif j < code_length and (input_code[j] == '='):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-', "'"] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim10
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for <=
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                
                else: #invalid delim for <
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                
            elif current_char == '>':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '(', '-', '\''] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']:#delim10
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                
                elif j < code_length and (input_code[j] == '='):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-', '\''] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']:#delim10
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for >=
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1

                else: #invalid delim for <
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                                    
            elif current_char == '=': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '(', '-','\'','"', '{'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim11
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                
                elif input_code[j] == '=':
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-','\'','"', '{'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim11
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for ==
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else: #invalid delim for =
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1    

            elif current_char == '!': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in self.reg_def['letra'] or (input_code[j] in ['*',' ','(']): #delim13
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                elif j < code_length and (input_code[j] == '='):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ', '(', '-','\'','"'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim12
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i=j-1
                    else: #invalid delim for !=
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else: #invalid delim for !
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                    
            elif current_char == '|': 
                j = i + 1
                lexeme = input_code[i:j]  
                if j < code_length and (input_code[j] == '|'):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ','(','-','=','!','[','\'','"'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim14
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for ||
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else: 
                    inv = input_code[j] 
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number])  
                    i = j 
                    i = j-1 

            elif current_char == '&':
                j = i + 1
                if j < code_length and (input_code[j] == '&'):
                    j += 1
                    lexeme = input_code[i:j]
                    if input_code[j] in ['*',' ','(','-','=','!','[','\'','"'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim14
                        tokens.append([lexeme, lexeme, line_number])
                        i = j
                        i = j-1
                    else: #invalid delim for &&
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else:
                    errors.append([f"Lexical Error:\t\tIllegal character ({current_char})", "", line_number])
                    i += 1


            elif current_char == ',':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', "'", '"', '-', '{','(','\n'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim11
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                else: #invalid delim for ,
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
            

            elif current_char == ';':
                j = i + 1
                lexeme = input_code[i:j]
                if j < len(input_code) and (input_code[j] in ['*',' ', '\n'] or input_code[j] in self.reg_def['letra']): #delim15
                    tokens.append([lexeme, lexeme, line_number])
                    i = j 
                    i = j-1
                else: #invalid delim for ,
                    inv = ''
                    if j < len(input_code):
                        inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            elif current_char == '(':
                j = i + 1
                lexeme = input_code[i:j]
                
                if input_code[j] in ['*',' ', '"', "'",'-','!','+','(',')','['] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim16
                    tokens.append([lexeme, lexeme, line_number])
                    i = j 
                    i = j-1
                else:
                    inv = ' '
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            elif current_char == '[':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ','(','-','=','!','[','\'','"'] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim14
                    tokens.append([lexeme, lexeme, line_number])
                    i = j 
                    i = j-1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                

            elif current_char == '{':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', '\n', '{','"','\'','}','-','+',] or input_code[j] in self.reg_def['numero'] or input_code[j] in self.reg_def['letra']: #delim17
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            elif current_char == ':': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in [' ','*','\n']: #spacecmnt
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j-1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            elif current_char == ')': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in [' ', ';', ')', ',', '*', '/', '+', '-', '%', '!', '=', '>', '<','&','|','\n']:  #delim18
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i=j-1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
            
            elif current_char == ']': 
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ', ';', ')', ',', ']','[','/', '+', '-', '%', '!', '=', '>', '<','&','|','\n']: #delim19
                    tokens.append([lexeme, lexeme, line_number])
                    i = j 
                    i=j-1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1
                    
            elif current_char == '}':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*',' ',';','}', '\n',','] or input_code[j] in self.reg_def['letra']: #delim20
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j - 1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            elif current_char == '#':
                j = i + 1
                lexeme = input_code[i:j]
                if input_code[j] in ['*'] or input_code[j] in self.reg_def['letra']: #delim21
                    tokens.append([lexeme, lexeme, line_number])
                    i = j
                    i = j - 1
                else:
                    inv = input_code[j]
                    errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                    i = j
                    i = j-1

            

            elif current_char == '"': #string literals
                j = i + 1
                while j < len(input_code) and input_code[j] != '"': 
                    if input_code[j] == '\\':
                        j += 2 
                    else:
                        j += 1 
                lexeme = input_code[i:j+1] 
                lexeme = lexeme.replace("\\n", "\n").replace("\\t", "\t").replace("\\'","\'").replace('\\"', '\"').replace("\\\\","\\")
                if j+1 < len(input_code) and input_code[j+1] in ['*',' ', ',', ';',')','}','&','|','+','=',':',']','!']: #strdelim
                    tokens.append([lexeme, "stringlit", line_number])
                    i = j
                else:
                    errors.append([f"Lexical Error:\t\tInvalid string literal: ",lexeme,line_number])
                    i = j 
 
            elif current_char == "'": #char literals
                j = i + 2
                while j < len(input_code) and input_code[j-1] != "'":
                    j+=1
                lexeme = input_code[i:j]
                char_lexeme = self.validate_char_literal(lexeme)
                if char_lexeme is not None:
                    if input_code[j] in ['*',' ', ',', ';',')','}','&','|','+','=',':',']','!','>','<']:  #chardelim                
                        tokens.append([lexeme, "charlit", line_number])
                        i = j
                        i = j - 1
                    else:
                        inv = ''
                        inv = input_code[j]
                        errors.append([f"Lexical Error:\t\tInvalid delimiter ({inv}) for token ",lexeme,line_number]) 
                        i = j
                        i = j-1
                else:
                    errors.append([f"Lexical Error:\t\tInvalid character literal: ",lexeme,line_number]) 
                    i = j
                    i = j-1 #invalid char lit
            

            i += 1
        return tokens, errors