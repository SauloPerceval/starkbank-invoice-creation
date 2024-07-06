from random import randint


def generate_random_cpf() -> str:
    cpf_base = [randint(0, 9) for _ in range(9)]

    for i in range(2):
        digits_sum = sum([val * (10 + i - idx) for idx, val in enumerate(cpf_base)])

        if (rem := digits_sum % 11) <= 1:
            cpf_base.append(0)
        else:
            cpf_base.append(11 - rem)

    return "".join(str(n) for n in cpf_base)
