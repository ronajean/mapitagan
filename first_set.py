
first_set = {
    'program':['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', 'estruktura_po', 'null', '#'],
    'global_dec':['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', 'estruktura_po', 'null', '#'],
    'declaration':['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'lagi_po', 'null', '#'],
    'var_dec':['int_po', 'float_po', 'bool_po', 'char_po', 'str_po'],
    'int_value':['=', '[', 'null'],
    'int_value_prod':['intlit', 'id', '(', '-', 'floatlit', '++', '--', 'strlen_po'],
    'int_value_tail':[',', 'null'],
    'int_array_dec':['['],
    'array_size':['intlit', 'id'],
    'int_array_dec2':['=', '['],
    'int_array_item':['intlit', 'id'],
    'int_array_item_val': ['intlit', 'id'],
    'int_array_dec2_tail': [',', 'null'],
    'int_array_2d_val': ['='],
    'int_array_2d_item': ['{'],
    'int_array_item_tail': [',', 'null'],
    'id_prod': ['id'],
    'id_tail': ['[', '_ni_', '(', 'null'],
    'array_access': ['['],
    'index': ['intlit', 'id', '(', '-', 'floatlit'],
    'index_tail': ['[', '_', '(', 'null'],
    'struct_access': ['_ni_'],
    'func_call': ['('],
    'arguments': ['intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', 'id', '!', '++', '--', 'strlen', 'null'],
    'arguments_val': ['intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', 'id', '!', '++', '--', 'strlen', 'null'],
    'args_tail': [',', 'null'],
    'arithmetic': ['(', '-', 'intlit', 'floatlit', 'id'],
    'math_val': ['(', '-', 'intlit', 'floatlit', 'id'],
    'arithmetic_tail': ['+', '-', '*', '/', '%', 'null'],
    'arithmetic_op': ['+', '-', '*', '/', '%'],
    'unary': ['++', '--', 'intlit', 'id'],
    'unary_op': ['++', '--'],
    'unary_val': ['intlit', 'id'],
    'unary_id_tail': ['_', '[', 'null'],
    'strlen_exp': ['strlen'],
    'strlen_item_val': ['id', 'stringlit'],
    'strlen_val': ['id', 'stringlit'],
    'strlen_val_tail': ['+'],
    'value': ['intlit', 'floatlit', 'boollit', 'charlit', 'stringlit'],
    'value_tail': [',', 'null'],
    'expression': ['(', '-', 'intlit', 'floatlit', 'id', '!', '++', '--', 'stringlit', 'strlen', 'null'],
    'relational': ['(', '-', 'intlit', 'floatlit', 'id'],
    'relational_tail': ['==', '!=', '<=', '>=', '<', '>', 'null'],
    'relational_op': ['==', '!=', '<=', '>=', '<', '>'],
    'logical': ['!', 'null'],
    'logical_tail': ['&&', '||', 'null'],
    'not': ['!', 'null'],
    'logical_op': ['&&', '||'],
    'string_cont': ['stringlit', 'id'],
    'string_cont_val': ['stringlit', 'id'],
    'float_value': ['=', '[', 'null'],
    'float_value_prod': ['floatlit', 'id', '(', '-', 'intlit', 'null'],
    'float_value_tail': [',', 'null'],
    'float_array_dec': ['['],
    'float_array_dec2': ['=', '['],
    'float_array_item': ['floatlit', 'id'],
    'float_array_item_val': ['floatlit', 'id'],
    'float_array_dec2_tail': [',', 'null'],
    'float_array_2d_val': ['='],
    'float_array_2d_item': ['{'],
    'float_array_item_tail': [',', 'null'],
    'bool_value': ['=', '[', 'null'],
    'bool_value_prod': ['boollit', '(', '-', 'intlit', 'floatlit', 'id', '!', 'null'],
    'bool_value_tail': [',', 'null'],
    'bool_array_dec': ['['],
    'bool_array_dec2': ['=', '['],
    'bool_array_item': ['boollit', 'id'],
    'bool_array_item_val': ['boollit', 'id'],
    'bool_array_dec2_tail': [',', 'null'],
    'bool_array_2d_val': ['='],
    'bool_array_2d_item': ['{'],
    'bool_array_item_tail': [',', 'null'],
    'char_value': ['=', '[', 'null'],
    'char_value_prod': ['charlit', 'id'],
    'char_value_tail': [',', 'null'],
    'char_array_dec': ['['],
    'char_array_dec2': ['=', '['],
    'char_array_item': ['charlit', 'id'],
    'char_array_item_val': ['charlit', 'id'],
    'char_array_dec2_tail': [',', 'null'],
    'char_array_2d_val': ['='],
    'char_array_2d_item': ['{'],
    'char_array_item_tail': [',', 'null'],
    'str_value': ['=', '[', 'null'],
    'str_value_prod': ['stringlit', 'id'],
    'str_value_tail': [',', 'null'],
    'str_array_dec': ['['],
    'str_array_dec2': ['=', '['],
    'str_array_item': ['stringlit', 'id'],
    'str_array_item_val': ['stringlit', 'id'],
    'str_array_dec2_tail': [',', 'null'],
    'str_array_2d_val': ['='],
    'str_array_2d_item': ['{'],
    'str_array_item_tail': [',', 'null'],
    'kons_dec': ['lagi_po'],
    'kons_dec_data_type': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po'],
    'int_kons_dec': ['=', '['],
    'int_kons_dec_val': ['intlit', 'id'],
    'int_kons_tail': [',', 'null'],
    'float_kons_dec': ['=', '['],
    'float_kons_dec_val': ['floatlit', 'id'],
    'float_kons_tail': [',', 'null'],
    'bool_kons_dec': ['=', '['],
    'bool_kons_dec_val': ['boollit', 'id'],
    'bool_kons_tail': [',', 'null'],
    'char_kons_dec': ['=', '['],
    'char_kons_dec_val': ['charlit', 'id'],
    'char_kons_tail': [',', 'null'],
    'str_kons_dec': ['=', '['],
    'str_kons_dec_val': ['stringlit', 'id'],
    'str_kons_tail': [',', 'null'],
    'func_dec': ['#'],
    'func_type': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'wala_po'],
    'data_type': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po'],
    'parameter': ['int_po', 'float_po', 'bool_po', 'char_po', 'str_po', 'null'],
    'parameter_tail': [',', 'null'],
    'struct_dec': ['estruktura_po'],
    'struct_body': ['{'],
    'statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po', 'ulit_po', 'gawin_po', 'habang_po', 'null'],
    'input_statement': ['id'],
    'prompt': ['stringlit', 'null'],
    'output_statement': ['ilabas_po'],
    'output_val': ['id', 'intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', '!', '++', '--', 'strlen', 'null'],
    'assignment_statement': ['id'],
    'assignment_val': ['id', 'intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', '!', '++', '--', 'strlen', 'null'],
    'assign_op': ['+=', '-=', '*=', '/='],
    'assign_op_eq': ['=', '+=', '-=', '*=', '/='],
    'conditional_statement': ['kung_po', 'mamili_po'],
    'conditional_val': ['!', 'null'],
    'okayapo_statement': ['okaya_po', 'null'],
    'kundipo_statement': ['kundi_po', 'null'],
    'switch_body': ['sakali_po'],
    'case': ['sakali_po'],
    'case_tail': ['sakali_po', 'null'],
    'default': ['default_po', 'null'],
    'switch_val': ['intlit', 'charlit'],
    'switch_statement': ['id', 'ilabas_po', 'kung_po', 'mamili_po'],
    'for_statement': ['ulit_po'],
    'initialization': ['id'],
    'for_condt': ['!', 'null'],
    'update': ['++', '--', 'intlit', 'id'],
    'update_val': ['id', 'intlit'],
    'do-while_statement': ['gawin_po'],
    'while_statement': ['habang_po'],
    'func_call_statement': ['id'],
    'func_definition': ['#'],
    'func_definition_tail': ['#', 'null'],
    'ibalikpo_statement': ['ibalik_po'],
    'ibalikpo_val': ['id', 'intlit', 'floatlit', 'boollit', 'charlit', 'stringlit', '(', '-', '!', '++', '--', 'strlen', '#']
}

