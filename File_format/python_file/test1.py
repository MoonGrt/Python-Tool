import re


# 词法分析器
def lexer(program):
    pattern = r'\b(?:print|if|else|for|while)\b|\d+|\w+|"[^"]*"|[-+*/<>=;(){}#]'
    tokens = [match.group(0) for match in re.finditer(pattern, program)]
    
    
    
    print(tokens)
    return tokens


# 语法分析器
def parse_expression(tokens, start):
    expression = ''
    i = start
    while i < len(tokens) and tokens[i] not in (';', ')'):
        expression += tokens[i]
        i += 1
    return expression, i + 1 # 跳过 '}' 可能越界

def parse_block(tokens, start):
    block = ''
    bracket_cnt = 0
    i = start + 1 # 跳过 '{'
    while i < len(tokens):
        if tokens[i] == '{':
            bracket_cnt += 1
        elif tokens[i] == '}':
            if(not bracket_cnt):
                break
            else:
                bracket_cnt -= 1
        block += tokens[i] + ' '
        i += 1
    return block, i + 1  # 跳过 '}' 可能越界

def parser(tokens):
    # 简单的语法规则，支持基本的赋值、打印、if、for和while语句
    statements = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '#':
            abandon, i = parse_expression(tokens, i) # 跳过一条语句
        elif tokens[i] == '/' and tokens[i+1] == '/':
            abandon, i = parse_expression(tokens, i) # 跳过一条语句
        elif tokens[i] == 'print':
            i += 1
            expression, i = parse_expression(tokens, i)
            statements.append(('print', expression))
        elif tokens[i] == 'if':
            i += 2  # 跳过'if', '('
            condition, i = parse_expression(tokens, i)
            if_body, i = parse_block(tokens, i)
            else_body, i = parse_block(tokens, i + 1) if i < len(tokens) and tokens[i] == 'else' else ('', i)
            statements.append(('if', condition, if_body, else_body))
        elif tokens[i] == 'while':
            i += 2  # 跳过'while', '('
            condition, i = parse_expression(tokens, i)
            while_body, i = parse_block(tokens, i)
            statements.append(('while', condition, while_body))
        elif tokens[i] == 'for':
            i += 2  # 跳过'for', '('
            init, i = parse_expression(tokens, i)
            condition, i = parse_expression(tokens, i)
            update, i = parse_expression(tokens, i)
            body, i = parse_block(tokens, i)
            statements.append(('for', init, condition, update, body))
        else:
            # 默认为赋值语句
            variable = tokens[i]
            i += 2  # 跳过变量,等号
            value = ''
            while i < len(tokens) and tokens[i] != ';':
                value += tokens[i]
                i += 1
            statements.append(('ASSIGN', variable, value))
            i += 1  # 跳过分号
    # print(statements)
    return statements


# 解释执行
variables = {}

def safe_eval(expression,variables):
    # 使用正则表达式提取表达式中的变量
    expression_variables = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression))
    # 将expression中的变量添加到variables中，设置为0
    for var in expression_variables:
        if var not in variables:
            variables[var] = 0
    return eval(expression, variables)  # 计算表达式的结果

def interpreter(statements):
    global variables
    for statement in statements:
        if statement[0] == 'ASSIGN':
            variable, value = statement[1], statement[2]
            variables[variable] = safe_eval(value, variables)
        elif statement[0] == 'print':
            expression = statement[1]
            print(safe_eval(expression, variables))
        elif statement[0] == 'if':
            condition, if_body, else_body = statement[1], statement[2], statement[3]
            if safe_eval(condition, variables):
                interpreter(parser(lexer(if_body)))
            else:
                interpreter(parser(lexer(else_body)))
        elif statement[0] == 'while':
            condition, body = statement[1], statement[2]
            while safe_eval(condition, variables):
                interpreter(parser(lexer(body)))
        elif statement[0] == 'for':
            initialization, condition, update, body = statement[1], statement[2], statement[3], statement[4]
            variables[initialization.split('=')[0]] = safe_eval(initialization.split('=')[1], variables)
            while safe_eval(condition, variables):
                interpreter(parser(lexer(body)))
                variables[update.split('=')[0]] = safe_eval(update.split('=')[1], variables)


# 汇编器
def operate(op, left, right, imm):
    # 根据运算符生成相应的汇编指令
    code = ''
    if(op == '+'):
        if(imm):
            code = f"    addi {left}, {left}, {right}\n"
        else:
            code = f"    add {left}, {left}, {right}\n"
    elif(op == '-'):
        if(imm):
            code = f"    addi {left}, {left}, {right}\n"
        else:
            code = f"    sub {left}, {left}, {right}\n"
    return code

def generate_expression_code(expression, left_reg, right_reg, label):
    global variable_regs
    code = ""
    # 检查值是否为整数或浮点数
    if expression.isdigit ():
        code = f"    li t0, {expression}\n"
    else:
        # 使用正则表达式提取表达式中的变量
        expression_variables = set(re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', expression))

        # 将expression中的变量添加到variables中，设置为0
        for var in expression_variables:
            if var not in variable_regs:
                code += f"    li {left_reg}, 0\n"
                code += f"    sw {left_reg}, {var}\n"
                variable_regs[var] = 0

        expression_token = lexer(expression)
        # 如果是二元运算，递归处理左右操作数
        op = expression_token[1]
        left_operand, right_operand = expression_token[0], expression_token[2]

        if not left_operand.isdigit():
            code += f"    lw {left_reg}, {left_operand}\n"
            if not right_operand.isdigit():
                code += f"    lw {right_reg}, {right_operand}\n"
                if op in ('+', '-'):
                    code += operate(op, left_reg, right_operand, 0)
                elif op == '<':
                    code += f"    ble {right_reg}, {left_reg}, {label}\n"
                elif op == '>':
                    code += f"    ble {left_reg}, {right_reg}, {label}\n"
            else:
                if op in ('+', '-'):
                    code += operate(op, left_reg, right_operand, 1)
                elif op == '<':
                    code += f"    li {right_reg}, {right_operand}\n"
                    code += f"    ble {right_reg}, {left_reg}, {label}\n"
                elif op == '>':
                    code += f"    li {right_reg}, {right_operand}\n"
                    code += f"    ble {left_reg}, {right_reg}, {label}\n"
        else:
            code += f"    li {left_reg}, {left_operand}\n"
            if not right_operand.isdigit():
                code += f"    lw {right_reg}, {right_operand}\n"
                if op in ('+', '-'):
                    code += operate(op, left_reg, right_reg, 0)
                elif op == '<':
                    code += f"    blt {right_reg}, {left_reg}, {label}\n"
                elif op == '>':
                    code += f"    blt {left_reg}, {right_reg}, {label}\n"
            else:
                if op in ('+', '-'):
                    code += operate(op, left_reg, right_reg, 1)
                elif op == '<':
                    code += f"    li {right_reg}, {right_operand}\n"
                    code += f"    blt {right_reg}, {left_reg}, {label}\n"
                elif op == '>':
                    code += f"    li {right_reg}, {right_operand}\n"
                    code += f"    blt {left_reg}, {right_reg}, {label}\n"
    return code

variable_regs = {}
def generate_riscv(statements):
    code = ""
    label_cnt = 0  # 用于生成唯一的循环标签

    for statement in statements:
        if statement[0] == 'ASSIGN':
            variable, expression = statement[1], statement[2]
            if variable not in variable_regs:   # 如果变量在变量字典中不存在，则初始化为0
                variable_regs[variable] = 0
            code += generate_expression_code(expression, 't0', 't1', "")
            code += f"    sw t0, {variable}\n"
        elif statement[0] == 'print':
            expression = statement[1]
            # code += f"    li a0, {expression}\n"
            # code += "    call print\n"
        elif statement[0] == 'if':
            condition, if_body, else_body = statement[1], statement[2], statement[3]
            # if(else_body):
            #     # 生成条件评估的代码
            #     code += generate_expression_code(condition, 't0', 't1', f"else_{label_cnt}") # 成立跳转
            #     # 生成else体的代码
            #     code += generate_riscv(parser(lexer(else_body)))
            #     code += f"    j if_{label_cnt}\n"
            #     # 开始else语句的唯一标签
            #     code += f"else_{label_cnt}:\n"
            #     # 生成if体的代码
            #     code += generate_riscv(parser(lexer(if_body)))
            #     code += f"if_{label_cnt}:\n"
            # else:
            #     # 生成条件评估的代码
            #     code += generate_expression_code(condition, 't0', 't1', f"if_{label_cnt}") # 成立跳转
            #     # 生成if体的代码
            #     code += generate_riscv(parser(lexer(if_body)))
            #     code += f"if_{label_cnt}:\n"
            # 生成条件评估的代码
            code += generate_expression_code(condition, 't0', 't1', f"else_{label_cnt}") # 成立跳转
            # 生成if体的代码
            code += generate_riscv(parser(lexer(if_body)))
            code += f"    j if_{label_cnt}\n"
            # 开始else语句的唯一标签
            code += f"else_{label_cnt}:\n"
            # 生成else体的代码
            code += generate_riscv(parser(lexer(else_body)))    
            code += f"if_{label_cnt}:\n"
            label_cnt += 1
        elif statement[0] == 'while':
            condition, body = statement[1], statement[2]
            # 跳到循环体的结束标签
            code += f"    j while_{label_cnt}\n"
            # 循环体的唯一标签
            code += f"while_body_{label_cnt}:\n"
            # 生成循环体的代码
            code += generate_riscv(parser(lexer(body)))
            # 开始while循环的唯一标签
            code += f"while_{label_cnt}:\n"
            # 生成条件评估的代码
            code += generate_expression_code(condition, 't0', 't1', f"while_body_{label_cnt}") # 成立跳转
            label_cnt += 1
        elif statement[0] == 'for':
            initialization, condition, update, body = statement[1], statement[2], statement[3], statement[4]
            # 生成初始化的代码
            code += generate_riscv(parser(lexer(initialization)))
            # 跳到循环体的结束标签
            code += f"    j for_{label_cnt}\n"
            # 循环体的唯一标签
            code += f"for_body_{label_cnt}:\n"
            # 生成循环体的代码
            code += generate_riscv(parser(lexer(body)))
            # 生成更新的代码
            code += generate_riscv(parser(lexer(update)))
            # 开始for循环的唯一标签
            code += f"for_{label_cnt}:\n"
            # 生成条件评估的代码
            code += generate_expression_code(condition, 't0', 't1', f"for_body_{label_cnt}")   # 成立跳转
            label_cnt += 1
    return code

# 从文件读取程序
def read_program_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
program_file_path = 'F:\Project\Python\Project\Compiler\code.txt'
program = read_program_from_file(program_file_path)

# program = """
#     X = 10;
#     Y = 15;
#     if(X > Y)
#     {
#         X = X - Y;
#     }
#     else
#     {
#         Y = Y - X;
#     }
# """

program = """
    X = 10;
    Y = 15;
    if(X > Y)
    {
        X = X - Y;
    }
"""

# program = """
#     X = 10;
#     while(X < 15)
#     {
#         X = X + 1;
#     }
# """

# program = """
#     Y = 15;
#     for(i = 0; i < 3; i = i + 1)
#     {
#         Y = Y + 2;
#     }
# """

# program = """
#     X = 14;
#     Y = 15;
#     for(i = 0; i < 3; i = i + 1)
#     {
#         if(X < Y)
#         {
#             X = X + 1;
#             print X;
#         }
#         else
#         {
#             Y = Y + 2;
#             print Y;
#         }
#     }
# """

tokens = lexer(program)
statements = parser(tokens)
interpreter(statements)

assembly_code = ".text\n.globl main\nmain:\n"
assembly_code += generate_riscv(statements)
print(assembly_code)