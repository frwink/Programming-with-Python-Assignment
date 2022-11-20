import math
class IdealFunctionProcessor:
    """
    This class is responsible to manage the ideal function data and to find the best k function that best fit 
    """
    def __init__(self, train_data, ideal_data):
        self.train_data = train_data
        self.ideal_data = ideal_data
    
    """
    Find the best fitting k ideal functions
    """
    def find_best_ideals(self, k):
        pass


class IdealFunctionSumSquareValues:
    def __init__(self, train_data, ideal_data):
        self.train_data = train_data
        self.ideal_data = ideal_data
        self.numIdealFns = len(self.ideal_data[0])-1
        self.numTrainFns = len(self.train_data[0])-1
    
    """
    Find the best fitting k ideal functions using the ssr as metric
    """
    def find_best_ideals(self,k):
        assert(k > 0 and k < self.numIdealFns)

        ordered_ideals = dict()
        points = len(self.train_data)

        for i in range(0,self.numIdealFns):
            ssr = 0
            for j in range(0,self.numTrainFns):
                for p in range(0,points):
                    ssr = ssr + (self.train_data[p][j+1]-self.ideal_data[p][i+1])**2
            ordered_ideals[i+1]=ssr

        ordered_ideals=dict(sorted(ordered_ideals.items(), key=lambda item: item[1]))
        ordered_ideals = list(ordered_ideals)[0:k]
        return ordered_ideals
    

class IdealFnValidatorSqrtN:
     
    def __init__(self, test_data, ideal_data, train_data, ordered_ideals):
        self.train_data = train_data
        self.test_data = test_data
        self.ideal_data = ideal_data
        self.ordered_ideals = ordered_ideals


    def findN(self):
        N=10.0
        numpoints = len(self.train_data)
        for idealFnIdx in self.ordered_ideals:
            for j in range(0,4):
                for p in range(0,numpoints):
                    err = math.fabs(self.train_data[p][j] - self.ideal_data[p][idealFnIdx])
                    if err > N:
                    # print(f'found  new max for ideal function {idealFnIdx} at location {p} = {err}')
                        N = err
        return N
    

    # calculate the max error between a particular ideal function idealFnIdx and the test data 
    # test data is a list of lists [[x,y]]
    # test data is not ordered by x so this is why i need to find the matching x from test data into the ideal function data 
    def findM(self,idealFnIdx):
        M = 0.0
        diffData = []
        pointstest = len(self.test_data)
        pointideal = len(self.ideal_data)
        for p in range(0,pointstest):
            for pi in range(0,pointideal):
                if self.test_data[p][0]==self.ideal_data[pi][0]:
                    err = math.fabs(self.test_data[p][1] - self.ideal_data[pi][idealFnIdx])
                    diffData.append([self.test_data[p][0], self.test_data[p][1], err, self.ideal_data[pi][idealFnIdx]])
                    if err > M:
                        M = err
                    # print(f'findM: found  new max for ideal function {idealFnIdx} at location {p} = {err}')
        return (M, diffData)

    def validate(self):
        diffDataList = []
        N = self.findN()
        for idealFnIdx in self.ordered_ideals:
            (M,diffData) = self.findM(idealFnIdx)
            if M >= math.sqrt(2)*N:
                raise Exception(f'the ideal function {idealFnIdx} is not confirmed by the test data')
            diffDataList.append(diffData)
        return diffDataList
        

    
