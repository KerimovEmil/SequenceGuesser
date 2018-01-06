from Sequences.BaseClass import Sequence

if __name__ == '__main__':
    # user_input = [1, 2, 4, 8, 16, 32]
    # user_input = [1, 2, 3, 5, 8, 13]
    # user_input = [2, 5, 14, 35, 74, 137, 230, 359, 530, 749]
    # user_input = [2, 5, 10, 17, 26, 37, 50, 65, 82, 101]
    # user_input = [5, 10, 17, 26, 37, 50, 65, 82, 101]
    # user_input = [313, 331, 367, 421]
    # user_input = [0, 2, 6, 12, 20]
    # user_input = [6, 6, 6, 6]
    # user_input = [0, 0, 0, 0]
    # user_input = [1, -1, 1, -1]
    # user_input = [-3, 4, 23, 60, 121]
    # user_input = [2.718281828459045, 7.3890560989306495, 20.085536923187664, 54.59815003314423, 148.41315910257657]
    # user_input = [1, 22, 97, 286, 673, 1366, 2497, 4222, 6721]
    # user_input = [6, 7, 12, 14, 24, 28, 48, 56, 96]  # TODO: make this work f(n) = 2 f(n-2)
    # user_input = [6, 7, 13, 20, 33, 53, 86, 139, 225]
    user_input = [2, 1, 3, 4, 7, 11]
    index = 20

    Seq = Sequence(user_input)
    print(Seq.get_type())
    print(Seq.get_next_number())
    print(Seq.get_ith_number(index))
    print(Seq.get_term_str())
