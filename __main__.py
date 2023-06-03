from utils import *
from strategy import *
from mappers import *

def main():
    cutil = ClassUtils(Mapper2023.cProcess,"data","output")
    rutil = ResponseUtils(Mapper2023.rProcess,"data","output")


    strategy = GreedyRandomStudent(cutil,rutil)
    strategy.eval()
    strategy.metrics()


    rutil.publishOverall()
    cutil.publishClasses()


if __name__ == "__main__":
    main()