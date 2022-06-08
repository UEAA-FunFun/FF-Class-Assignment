from utils import *
from strategy import *
from mappers import *

def main():
    cutil = ClassUtils(Mapper2022.cProcess,"data","output")
    rutil = ResponseUtils(Mapper2022.rProcess,"data","output")


    strategy = GreedyRandomStudent(cutil,rutil)
    strategy.eval()
    strategy.metrics()


    rutil.publishOverall()
    cutil.publishClasses()


if __name__ == "__main__":
    main()