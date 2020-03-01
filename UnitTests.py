import GameSolver
import Operations

class UnitTests:

    def __init__(self):
        self.AllPassed = True
        self.TestNumber = 1


        self.TestOperations()
        self.TestSolves()

        if not self.AllPassed:
            exit(code=1)
        return

    def Assert(self, value, expectedValue, testName=""):
        if value == expectedValue:
            print(str(self.TestNumber) + ") Passed " + str(testName))
        else:
            print(str(self.TestNumber) + ") Failed " + str(testName))
            print("\t=======================")
            print("\texpected: " + str(expectedValue) + " but got " + str(value))
            print("\t=======================")

        self.TestNumber += 1
        return

    def TestOperations(self):
        
        #add
        add = Operations.Add(1)
        self.Assert(add.DoAction(1), 2, "Add +1 DoAction()")
        self.Assert(add.ToString(), "+1", "Add +1 ToString()")

        add = Operations.Add(-1)
        self.Assert(add.DoAction(1), 0, "Add -1 DoAction()")
        self.Assert(add.ToString(), "-1", "Add -1 ToString()")

        #Multiply
        multiply = Operations.Multiply(3)
        self.Assert(multiply.DoAction(1), 3, "Multiply 3 DoAction()")
        self.Assert(multiply.ToString(), "X3", "Multiply 3 ToString()")

        #Divide
        divide = Operations.Divide(3)
        self.Assert(divide.DoAction(9), 3, "Divide 3 DoAction()")
        self.Assert(divide.ToString(), "/3", "Divide 3 ToString()")

        #Shift
        shift = Operations.Shift(True)
        self.Assert(shift.DoAction(10), 1, "Shift right DoAction()")
        self.Assert(shift.ToString(), "<<", "Shift right ToString()")

        shift = Operations.Shift(False)
        self.Assert(shift.DoAction(1), 10, "Shift Left DoAction()")
        self.Assert(shift.ToString(), ">>", "Shift Left ToString()")

        #Insert
        shift = Operations.Insert(12)
        self.Assert(shift.DoAction(1), 112, "Insert DoAction()")
        self.Assert(shift.ToString(), "Insert 12", "Insert ToString()")

        #Translate
        translate = Operations.Translate(1,2)
        self.Assert(translate.DoAction(121), 222, "Translate DoAction()")
        self.Assert(translate.ToString(), "1=>2", "Translate ToString()")

        #Pow
        powOp = Operations.Pow()
        self.Assert(powOp.DoAction(4), 16, "Pow DoAction()")
        self.Assert(powOp.ToString(), "Pow 2", "Pow ToString()")

        #Flip
        flip = Operations.Flip()
        self.Assert(flip.DoAction(1), -1, "Flip DoAction()")
        self.Assert(flip.ToString(), "+/- ", "Flip ToString()")

        #Reverse
        reverse = Operations.Reverse()
        self.Assert(reverse.DoAction(1234), 4321, "Reverse DoAction()")
        self.Assert(reverse.ToString(), "Reverse", "Reverse ToString()")

        #Sum
        sumOp = Operations.Sum()
        self.Assert(sumOp.DoAction(1234), 10, "Sum DoAction()")
        self.Assert(sumOp.ToString(), "Sum", "Sum ToString()")


        return

    def TestSolves(self):
        #load test data
        testDataList = []

        #Run tests
        for testData in testDataList:
            found, steps = GameSolver.Solve(testDataList[0], testData[1], testData[2], testData[3])

            if found != testData[4]:
                exit(code=1)

            if found:
                exit(code=1)
        return

if __name__ == "__main__":
    UnitTests()
