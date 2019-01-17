import AI.config
from AI.caching import init_cache
from AI.explorator import discover_function_from_sig, \
    get_builtin_func_signature, init_exploration
from AI.generator import genint
from AI.operations import mean, operations
from AI.protocols import get_applicable_protocols


if __name__ == "__main__":

    init_cache()
    init_exploration()
    print(mean(genint()))
    print(mean(genint()))
    print(mean(genint()))
    print(mean(genint()))
    # TODO add a requirement or assertions table per funciton to determine
    # which known classes can be used in which function
    print(mean(genint()))

    print("initialization done")
