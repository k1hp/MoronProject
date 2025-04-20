import re


text = "Оперативная память ExeGate Value Special [EX287013RUS] 8 ГБ [DDR4, 8 ГБx1 шт, 2666 МГц, 19(CL)-19-19]"
re_shablon = r"Оперативная\sпамять\s(.+)\s\[.+\]\s.+\s\[(.+)\]"
match = re.fullmatch(re_shablon, text)
name_product = match.group(1)
specs_product = match.group(2).split(",")
result = dict(
                        name=name_product,
                        type=specs_product[0],
                        volume=specs_product[1][1:5],
                        quantity=specs_product[1][6:],
                        frequency=specs_product[2][1:],
                        cl=specs_product[3][1:3]
                    )
print(result)