"""
    Consits of funtions for boolean solver
    F = f_1 * f_2 * f_3...f_m
        where f_i is boolean function in ANF on set {0,1} in n-variables
        f_i is of form anf_stuct i.e. f_i = [0, [[1],[2,3]]] => x1 xor (x2*x3)
    I is the implicant set for F

    Sample:
        F = [[0, [[1], [2, 3]]], [0, [[1], [4]]], [1, [[2, 3], [1, 3, 4]]]]
        here F = f_1 * f_2 * f_3
        where f_1 = x1 xor (x2*x3)
        f_2 = x1 xor x4
        f_3 = 1 xor (x2*x3) xor x1*x3*x4

    For simplicity the first function is considered as the pivot
"""

from helping_functions.basic                        import reduce_anf_stuct
from helping_functions.orthonormal_set              import get_variable_set_length
from implicant_genrator.src.implicant_calculation   import get_implicant
from implicant_genrator.src.quotient_calculation    import anf_quotient_from_stuct
from satisfy_formula.src.multiply_function          import get_multiplication_set, merge_terms

def get_pivot_least_variables(bool_func):
    """
        Given all the equations, choose the pivot with the least number of terms
    """
    len_list    = map(get_variable_set_length, bool_func)
    pivot_index = len_list.index(min(len_list))
    pivot       = bool_func[pivot_index]

    return pivot, pivot_index
    

def reduce_bool_func(bool_func, term):
    """
        Divide each of the functions with term and 
    """
    bool_func = map(lambda x: anf_quotient_from_stuct(x), bool_func)
    bool_func = map(lambda x: reduce_anf_stuct(x), bool_func)

def boolean_solver(bool_func):
    """
        given a boolean function solve for the SOP form
        This is the main function that is used to solve the boolean system
    """
    f_pivot, pivot_index = get_pivot_least_variables(bool_func)
    implicant_pivot = get_implicant(f_pivot)
    
    if len(bool_func) == 1:
        return implicant_pivot

    implicant_set   = []

    for term in implicant_pivot:
        new_bool_func = []
        unit_quotient = 0
        zero_quotient = 0
        
        for f_j in (bool_func[:pivot_index] + bool_func[pivot_index+1:]):
            f_j_quotient = anf_quotient_from_stuct(f_j, term)
            
            if f_j_quotient == [0, []]:
                zero_quotient = 1
                break
            elif f_j_quotient == [1, []]:
                unit_quotient += 1
            else:
                if f_j_quotient not in new_bool_func:
                    new_bool_func.append(f_j_quotient)
        
        if unit_quotient == len((bool_func[:pivot_index] + bool_func[pivot_index+1:])):
            implicant_set.append(term)
            continue
        if zero_quotient > 0:
            continue

        reduced_implicants = boolean_solver(new_bool_func)
        
        temp_implicant_set = map(lambda x: sorted(merge_terms(x, term)), reduced_implicants)
        
        for temp_implicant in temp_implicant_set:
            if temp_implicant not in implicant_set:
                implicant_set.append(temp_implicant)

    return implicant_set

if __name__ == "__main__":
    test_set = [[0, [[1], [2], [1,2,3]]], [0, [[2],[3]]], [1, [[1,4], [2,3]]], [0, [[4], [2,3], [1,2,3]]]]

    print 'Implicant set -> ', boolean_solver(test_set)
