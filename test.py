from deco import timer


@timer
def do_somthing(start, end):
    res = 0
    for i in range(start, end):
        for j in range(start, end):
            res += i*i+j*j
    return res


do_somthing(1, 100)

gss = "http://yuding.hrbeu.edu.cn/Field/OrderField?checkdata=%5B%7B%22FieldNo%22%3A%22006%22%2C%22FieldTypeNo%22%3A%22YMQ001%22%2C%22FieldName%22%3A%22%E7%BE%BD%E6%AF%9B%E7%90%8301%22%2C%22BeginTime%22%3A%2215%3A00%22%2C%22Endtime%22%3A%2216%3A00%22%2C%22Price%22%3A%2225.00%22%7D%5D&dataadd=1&VenueNo=002"
pss = "http://yuding.hrbeu.edu.cn/Field/OrderField?checkdata=%5B%7B%22FieldNo%22%3A%22006%22%2C%22FieldTypeNo%22%3A%22YMQ001%22%2C%22FieldName%22%3A%22%E7%BE%BD%E6%AF%9B%E7%90%8301%22%2C%22BeginTime%22%3A%2215%3A00%22%2C%22Endtime%22%3A%2216%3A00%22%2C%22Price%22%3A%2225.00%22%7D%5D&dateadd=1&VenueNo=002"
print(gss == pss)
