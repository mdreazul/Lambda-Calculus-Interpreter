from LambdaParser import parser

def read_input():
  result = ''
  while True:
    data = input('LAMBDA> ').strip()
    if ';' in data:
      i = data.index(';')
      result += data[0:i+1]
      break
    else:
      result += data + ' '
  return result


def free_variables(var, exp):
  if exp[0] == 'num':
    return set()
  elif exp[0] == 'name':
    if exp[1] not in var:
      return {exp[1]}
    else:
      return set()
  elif exp[0] == 'twoexp':
    return free_variables(var,exp[1]).union(free_variables(var,exp[2]))
  elif exp[0] == 'op':
    print(exp)
    return free_variables(var,exp[2]).union(free_variables(var,exp[3]))
  elif exp[0] == 'lambda':
    print(exp)
    var.add(exp[1])
    return free_variables(var, exp[2])
  else:
    return set() # Need to fix the logic for the recursion.

def alpha_conv(new_var, old_lst, exp):
  if exp[0] == 'num':
    return exp
  elif exp[0] == 'name':
    if exp[1] in old_lst:
      if type(new_var) == list:
        exp = new_var
      else:
        exp[1] = new_var
    return exp
  elif exp[0] == 'twoexp':
    exp[1] = alpha_conv(new_var, old_lst, exp[1])
    exp[2] = alpha_conv(new_var, old_lst, exp[2])
    return exp
  elif exp[0] == 'op':
    exp[2] = alpha_conv(new_var, old_lst, exp[2])
    exp[3] = alpha_conv(new_var, old_lst, exp[3])
    return exp
  elif exp[0] == 'lambda':
    if (exp[1] in old_lst):
      exp[1] = new_var
      exp[2] = alpha_conv(new_var, old_lst+[exp[1]], exp[2])
    else:
      exp[2] = alpha_conv(new_var, old_lst, exp[2])
    return exp
  else:
    return exp

def substitution(exp, fv_in_exp, var, val):
  if exp[0] == 'num':
    return exp
  elif exp[0] == 'name':
    if exp[1] in fv_in_exp and exp[1] == var:
      exp = val
    return exp
  elif exp[0] == 'twoexp':
    exp[1] = substitution(exp[1], fv_in_exp.union(free_variables(set(), exp[1])), var, val)
    exp[2] = substitution(exp[2], fv_in_exp.union(free_variables(set(), exp[2])), var, val)
    return exp
  elif exp[0] == 'op':
    exp[2] = substitution(exp[2], fv_in_exp.union(free_variables(set(), exp[2])), var, val)
    exp[3] = substitution(exp[3], fv_in_exp.union(free_variables(set(), exp[3])), var, val)
    return exp
  elif exp[0] == 'lambda':
    if exp[1] in free_variables(set(), val):
      print("Error: Capture case encountered")
      return
    if (exp[1] == var):
      return exp
    exp[2] = substitution(exp[2], fv_in_exp.union(free_variables({exp[1]}, exp[2])) , var, val)
    return exp


def beta(tree, value_stack):
  if type(tree) == float:
    return [tree,value_stack];
  if tree[0] == 'num':
    return [float(tree[1]), value_stack];
  elif tree[0] == 'twoexp':
    value_stack.append(tree[2])
    return [tree[1], value_stack];
  elif tree[0] == 'lambda':
    return [alpha_conv(value_stack.pop(), [tree[1]], tree[2]), value_stack];
  elif tree[0] == 'op':
    [v1, value_stack] = beta(tree[2], value_stack)
    [v2, value_stack] = beta(tree[3], value_stack)
    if (type(v1) != float) or (type(v2) != float):
      tree[2] = v1
      tree[3] = v2
      return [tree, value_stack]
    if tree[1] == '+':
      return [v1 + v2, value_stack];
    elif tree[1] == '-':
      return [v1 - v2, value_stack];
    elif tree[1] == '*':
      return [v1 * v2, value_stack];
    elif tree[1] == '/':
      if v2 == 0:
        return 'ERROR: Divide by 0'   
      return [v1 / v2, value_stack];


def printtree(tree):
  if (type(tree) != list):
    return str(tree)
  elif tree[0] == 'name':
    return str(tree[1])
  elif tree[0] == 'num':
    return str(tree[1])
  elif tree[0] == 'lambda':
    return '( lambda ' + str(tree[1]) + ' ' + str(printtree(tree[2])) + ' )'
  elif tree[0] == 'op':
    return '( ' + str(tree[1]) + ' ' + printtree(tree[2]) + ' ' + printtree(tree[3]) + ' )'
  elif tree[0] == 'twoexp':
    return '( ' + printtree(tree[1]) + ' ' + printtree(tree[2]) + ' )'


def main():
  while True:
    data = read_input()
    if data == 'exit;':
      break
    try:
      tree = parser.parse(data)
      #print(tree)
    except Exception as inst:
      print(inst.args[0])
      continue
    if (tree[0] == 'free'):
      print('Trying free variable calculation')
      print(free_variables(set(), tree[1]))
    elif (tree[0] == 'alpha'):
      print('Trying alpha conversion')
      print(printtree(alpha_conv(tree[2], [], tree[1])))
    elif (tree[0] == 'subs'):
      print('Trying substitution')
      print(printtree(substitution(tree[1], set(), tree[2], tree[3])))
    else:
      stack_lst = []
      while (not isinstance(tree, float) and not isinstance(tree, int)):
        print(printtree(tree))
        [tree, stack_lst] = beta(tree, stack_lst)
        print('\n')
      print(tree)

main()
