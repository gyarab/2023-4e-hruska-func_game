arr = []
def infra(s) -> str:
    index = 1
    my_str = s
    final_str = ""
    for i in range(len(my_str)):
        try:
            if my_str[i] == my_str[i+1]:
                index += 1
            else:
                final_str += str(index)
                final_str += my_str[i]
                index = 1
        except:
            final_str += str(index)
            final_str += my_str[i]
    arr.append(len(final_str))
    print(final_str, "*************")
    if final_str.__contains__("4") or len(final_str) >= 2000:
        return 0
    infra(final_str)

infra("1")