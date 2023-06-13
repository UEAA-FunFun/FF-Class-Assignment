'''
so true

here mostly for my own ammusement. Plus who doesn't like HoFs??

For nostalgia purposes here are the recursive hofs below (written in sml)

fun map _ [] = []
  | map f (x::xs) = (f x) :: (map f xs)

fun foldl _ z [] = z
  | foldl f z (x::xs) = foldl f (f x) xs 

fun foldr _ z [] = z
  | foldr f z (x::xs) = f (x, foldr f z xs)

Good exercise for me to write iterative hofs me thinks.
'''

class HoF:
    def __init__(self,funcList) -> None:
        self.funcList = funcList
        self.lastRes = None 

    #keep a cache of last result, may be helpful
    def lastApp(self):
        if self.lastRes != None:
            return self.lastRes
        
        return None 

class Map(HoF):
    '''
    meant to just be a simple map
    '''
    def __init__(self, mapFunc) -> None:
        super().__init__([mapFunc])
        self.mapFunc = mapFunc

    '''
    applyMap: ('a -> 'b) -> 'a list -> 'b list :)
    '''
    def applyMap(self,xs):
        res = []
        for x in xs:
            res.append(self.mapFunc(x))
        self.lastApp = res

        return res

    def mapZip(self,xs,ys):
        res = []
        for i in range(min(len(xs),len(ys))):
            res.append(self.mapFunc(xs[i]),self.mapFunc(ys[i]))

        self.lastApp = res 
        return res

class Filter(HoF):
    '''
    meant to just be a simple filter
    '''
    def __init__(self, filterFunc) -> None:
        super().__init__([filterFunc])
        self.filterFunc = filterFunc

    def applyFilter(self,xs):
        res = []
        for x in xs:
            if self.filterFunc(x):
                res.append(x)
        self.lastApp = res
        return res
    
class Fold(HoF):
    '''
    folds a list. If you want a better explanation, attend my 15-150 hof recitation
    '''
    def __init__(self, foldFunc) -> None:
        super().__init__([foldFunc])
        self.foldFunc = foldFunc

    def foldl(self,xs,z):
        res = z
        for x in xs:
            res = self.foldFunc(x,res)
        self.lastApp = res
        return res 

    def foldr(self,xs,z):
        #true!
        return self.foldl(xs.reverse(),z)        

