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

    def find_best_ideals(self):
        pass


class IdealFunctionSumSquareValues:
    def __init__(self, train_data, ideal_data):
        self.train_data = train_data
        self.ideal_data = ideal_data
        self.numIdealFns = len(self.ideal_data[0]) - 1
        self.numTrainFns = len(self.train_data[0]) - 1

    def find_best_ideals(self):
        """
        Find the best fitting  ideal functions using the ssr as metric

        For each of the 4 function in the train dataset, it will try to find the best fitting function in the ideal data.
        The result of this function is a list of 4 elements.
        Each element of this list is a number, representing the ideal function that best fit a train fnction.

        For example if the be find_best_ideals returns [4,6,22,11] it means that the best fitting function for train function 0 is the ideal function 4
        and the best fitting for the train function 1 is the ideal function 6 etc.
        """
        ordered_ideals = []
        points = len(self.train_data)

        # for each train function try to find the best fitting ideal function out of the 50 provided
        for j in range(0, self.numTrainFns):
            best_ssr = float('inf')
            best_ideal = 0
            for i in range(0, self.numIdealFns):
                ssr = 0
                for p in range(0, points):
                    ssr = ssr + (self.train_data[p][j + 1] - self.ideal_data[p][i + 1]) ** 2
                if best_ssr > ssr:
                    best_ssr = ssr
                    best_ideal = i

            ordered_ideals.append(best_ideal + 1)

        return ordered_ideals


class IdealFnValidatorSqrtN:

    def __init__(self, test_data, ideal_data, train_data, ordered_ideals):
        self.train_data = train_data
        self.test_data = test_data
        self.ideal_data = ideal_data
        self.ordered_ideals = ordered_ideals

    def findN(self, num_train_fns=4):
        """
        Finds N which is defined as the maximum error between an ideal function and train data.
        """
        N = 10.0
        numpoints = len(self.train_data)
        for idealFnIdx in self.ordered_ideals:
            for j in range(0, num_train_fns):
                for p in range(0, numpoints):
                    err = math.fabs(self.train_data[p][j] - self.ideal_data[p][idealFnIdx])
                    if err > N:
                        N = err
        return N

    def findM(self, idealFnIdx):
        """
        Calculate the max error between a particular ideal function idealFnIdx and the test data. The test data is a list of lists [[x,y]]
        The test data is not ordered by x so this is why i need to find the matching x from test data into the ideal function data
        """
        M = 0.0
        diffData = []
        pointstest = len(self.test_data)
        pointideal = len(self.ideal_data)
        for p in range(0, pointstest):
            for pi in range(0, pointideal):
                if self.test_data[p][0] == self.ideal_data[pi][0]:
                    err = math.fabs(self.test_data[p][1] - self.ideal_data[pi][idealFnIdx])
                    diffData.append([self.test_data[p][0], self.test_data[p][1], err, self.ideal_data[pi][idealFnIdx]])
                    if err > M:
                        M = err
        return (M, diffData)

    def validate(self):
        """
        Validates the selected ideal function using the criteria M < sqrt(N)
        If a selected ideal function is found to not satisfy that criteria an exception is raised: it means the selected function is not the right one.
        """
        diffDataList = []
        N = self.findN()
        for idealFnIdx in self.ordered_ideals:
            (M, diffData) = self.findM(idealFnIdx)
            if M >= math.sqrt(2) * N:
                raise Exception(f'the ideal function {idealFnIdx} is not confirmed by the test data')
            diffDataList.append(diffData)
        return diffDataList



