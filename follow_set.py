
follow_set = {
    'global_dec': ['simula_po'],
    'declaration': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', 'int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', '#', 'estruktura_po', 'simula_po'],
    'statement': ['wakas_po', '}', ';'],
    'func_definition': ['#'],
    'struct_dec': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', '#', 'estruktura_po', 'simula_po'],
    'var_dec': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', '#', 'id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', 'estruktura_po', 'simula_po', '}'],
    'kons_dec': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', '#', 'id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', 'estruktura_po', 'simula_po'],
    'func_dec': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', '#', 'id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', 'estruktura_po', 'simula_po'],
    'int_value': [',', ';'],
    'int_value_tail': [';'],
    'float_value': [',', ';'],
    'float_value_tail': [';'],
    'bool_value': [',', ';'],
    'bool_value_tail': [';'],
    'char_value': [',', ';'],
    'char_value_tail': [';'],
    'str_value': [',', ';'],
    'str_value_tail': [';'],
    'int_value_prod': [',', ';'],
    'int_array_dec': [';', ','],
    'id_prod': [',', ';', '}', ')', '+', '-', '*', '/', '%', ']', '=', '+=', '-=', '*=', '/='],
    'arithmetic': [',', ';', ']', ')', '+', '-', '*', '/', '%' ],
    'unary': [',', ';', ')'],
    'strlen_exp': [',', ';'],
    'array_size': [']'],
    'int_array_dec2': [',', ';'],
    'int_array_item': ['}'],
    'int_array_2d_val': [',', ';'],
    'int_array_dec2_tail': ['}'],
    'int_array_item_val': [',', ',', '}'],
    'int_array_2d_item': ['}'],
    'int_array_item_tail': ['}'],
    'id_tail': [',', ';', '}'],
    'array_access': [',', ';', '}', '++', '--'],
    'struct_access': [',', ';', '}', '++', '--'],
    'func_call': [',', ';', '}'],
    'index': [']'],
    'index_tail': [',', ';', '}'],
    'arguments': [')'],
    'arguments_val': [',', ',', ')'],
    'args_tail': [')'],
    'value': [',', ')', ';'],
    'expression': [',', ')', ';'],
    'math_val': ['+', '-', '*', '/', '%', ',', ';', ']', '==', '!=', '<=', '>=', '<', '>'],
    'arithmetic_tail': [',', ';', ']', ')'],
    'arithmetic_op': ['(', '-', 'intlit', 'floatlit', 'id'],
    'unary_op': ['intlit', 'id', ',', ';'],
    'unary_val': [',', ';', '++', '--'],
    'unary_id_tail': [',', ';', '++', '--'],
    'strlen_item_val': [')'],
    'strlen_val': ['+'],
    'strlen_val_tail': [')'],
    'value_tail': [',', ',', ')'],
    'relational': [',', ',', ')', ';'],
    'logical': [',', ',', ')', ';'],
    'string_cont': [',', ',', ')', ';'],
    'strlen_exp': [',', ',', ')'],
    'relational_tail': [',', ',', ')'],
    'relational_op': ['(', '-', 'intlit', 'floatlit', 'id'],
    'not': ['('],
    'logical_tail': [',', ',', ')'],
    'logical_op': ['!', '('],
    'string_cont_val': ['+', ',', ',', ')'],
    'float_value_prod': [',', ',', ';'],
    'float_array_dec': [',', ',', ';'],
    'float_array_dec2': [',', ',', ';'],
    'float_array_item': ['}'],
    'float_array_2d_val': [',', ',', ';'],
    'float_array_item_val': [',', ',', '}'],
    'float_array_dec2_tail': ['}'],
    'float_array_2d_item': ['}'],
    'float_array_item_tail': ['}'],
    'bool_value_prod': [',', ',', ';'],
    'bool_array_dec': [',', ',', ';'],
    'bool_array_dec2': [',', ',', ';'],
    'bool_array_item': ['}'],
    'bool_array_2d_val': [',', ',', ';'],
    'bool_array_item_val': [',', ',', '}'],
    'bool_array_dec2_tail': ['}'],
    'bool_array_2d_item': ['}'],
    'bool_array_item_tail': ['}'],
    'char_value_prod': [',', ',', ';'],
    'char_array_dec': [',', ',', ';'],
    'char_array_dec2': [',', ',', ';'],
    'char_array_item': ['}'],
    'char_array_2d_val': [',', ',', ';'],
    'char_array_item_val': [',', ',', '}'],
    'char_array_dec2_tail': ['}'],
    'char_array_2d_item': ['}'],
    'char_array_item_tail': ['}'],
    'str_value_prod': [',', ',', ';'],
    'str_array_dec': [',', ',', ';'],
    'str_array_dec2': [',', ',', ';'],
    'str_array_item': ['}'],
    'str_array_2d_val': [',', ',', ';'],
    'str_array_item_val': [',', ',', '}'],
    'str_array_dec2_tail': ['}'],
    'str_array_2d_item': ['}'],
    'str_array_item_tail': ['}'],
    'kons_dec_data_type': [';', '}'],
    'int_kons_dec': [';'],
    'float_kons_dec': [';'],
    'bool_kons_dec': [';'],
    'char_kons_dec': [';'],
    'str_kons_dec': [';'],
    'int_kons_dec_val': [';'],
    'int_kons_tail': [';'],
    'float_kons_dec_val': [';'],
    'float_kons_tail': [';'],
    'bool_kons_dec_val': [';'],
    'bool_kons_tail': [';'],
    'char_kons_dec_val': [';'],
    'char_kons_tail': [';'],
    'str_kons_dec_val': [';'],
    'str_kons_tail': [';'],
    'func_type': ['id'],
    'parameter': [')'],
    'data_type': ['id'],
    'parameter_tail': [')'],
    'struct_body': [';'],
    'input_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', ';'],
    'output_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', ';'],
    'assignment_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'conditional_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po', ';'],
    'for_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'do-while_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'while_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'func_call_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'prompt': [')'],
    'output_val': [')'],
    'assign_op_eq': ['id', 'intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', '!', '++', '--', 'strlen', ';'],
    'assignment_val': [';'],
    'assign_op': ['id', 'intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', '!', '++', '--', 'strlen', ';'],
    'conditional_val': [')'],
    'okayapo_statement': ['kundi_po', 'id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'kundipo_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'wakas_po'],
    'switch_body': ['}'],
    'case': ['default_po', '}', 'sakali_po'],
    'default': ['}'],
    'switch_val': [':'],
    'switch_statement': [';', '}'],
    'case_tail': ['default_po', '}'],
    'initialization': [';'],
    'for_condt': [';'],
    'update': [')'],
    'update_val': [')'],
    'ibalikpo_statement': ['}'],
    'func_definition_tail': ['}'],
    'ibalikpo_val': [')']
}


a = "hello"
b= 2

print(a,b)

