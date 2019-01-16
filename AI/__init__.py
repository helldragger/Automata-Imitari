from AI.explorator import discover_function_from_sig, \
    get_builtin_func_signature, init_exploration
from AI.generator import genint
from AI.operations import mean, operations


if __name__ == "__main__":
    # method = "__set__"
    # sig = get_builtin_func_signature(method)
    # discover_function_from_sig("builtins", "object", method, sig)
    init_exploration()
    print(mean(genint()))
    print(mean(genint()))
    print(mean(genint()))
    print(mean(genint()))
    # TODO add a requirement or assertions table per funciton to determine
    # which known classes can be used in which function
    print(mean(genint()))

    print("initialization done")
