
def npp3(a):
    for z in a:
        for y in z:
            xs = []
            for x in y:
                xs.append(" ".join(map(lambda x: str(x).zfill(3), x)))
            print("   ".join(xs))
        print()


def npp2(a):
    for y in a:
        xs = []
        for x in y:
            xs.append(" ".join(map(lambda x: str(x).zfill(3), x)))
        print("   ".join(xs))

