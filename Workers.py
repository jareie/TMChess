from multiprocessing import Pool

#Just a simple helper file, that allows for easy usage of the multiproccesing library



def CreatePool(cores_leverage=3):
    return Pool(processes=cores_leverage)


def ReuseWorkers(function, argumentList, pooler):
    result = pooler.map(function,argumentList)
    return result

def MakeWorkers(function, argumentList, cores_leverage=3):
    result = []
    with Pool(processes=cores_leverage) as pool:
        result = pool.map(function,argumentList)
    return result

if __name__ == "__main__":
    print("Settup complete")