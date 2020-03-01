import GameSolver
import Operations

class UnitTests:

    def __init__(self):
        self.AllPassed = True
        self.TestNumber = 1
        self.GroupText = ""
        self.GroupStart = 1
        self.GroupPassed = True
        self.GroupName = ""


        self.TestOperations()
        self.TestSolves()

        self.SetGroup("Done")
        if not self.AllPassed:
            exit(code=1)
        return

    def SetGroup(self, groupName):

        if len(self.GroupText) > 0:
            text = str(self.GroupStart)+"-"+str(self.TestNumber-1)+") "

            if self.GroupPassed:
                text += "Passed "+str(self.GroupName)
                print(text)
            else:
                text += "Failed "+str(self.GroupName)
                print(text)
                print(self.GroupText)


        self.GroupText = ""
        self.GroupStart = self.TestNumber
        self.GroupName = groupName
        self.GroupPassed = True
        return

    def Assert(self, value, expectedValue, testName=""):
        self.GroupText += "\t"+str(self.TestNumber) + ") "

        if value == expectedValue:
            self.GroupText += "Passed " + str(testName) + "\n"
        else:
            self.GroupPassed = False
            self.AllPassed = False
            self.GroupText += "Failed " + str(testName) + "\n"
            self.GroupText += "\t\texpected: " + str(expectedValue) + " but got " + str(value) + "\n"

        self.TestNumber += 1
        return

    def TestOperations(self):
        
        self.SetGroup("Add")
        add = Operations.Add(1)
        self.Assert(add.DoAction(1), 2, "Add +1 DoAction()")
        self.Assert(add.ToString(), "+1", "Add +1 ToString()")

        add = Operations.Add(-1)
        self.Assert(add.DoAction(1), 0, "Add -1 DoAction()")
        self.Assert(add.ToString(), "-1", "Add -1 ToString()")

        self.SetGroup("Multiply")
        multiply = Operations.Multiply(3)
        self.Assert(multiply.DoAction(1), 3, "Multiply 3 DoAction()")
        self.Assert(multiply.ToString(), "X3", "Multiply 3 ToString()")

        self.SetGroup("Divide")
        divide = Operations.Divide(3)
        self.Assert(divide.DoAction(9), 3, "Divide 3 DoAction()")
        self.Assert(divide.ToString(), "/3", "Divide 3 ToString()")

        self.SetGroup("Shift")
        shift = Operations.Shift(True)
        self.Assert(shift.DoAction(10), 1, "Shift right DoAction()")
        self.Assert(shift.ToString(), "<<", "Shift right ToString()")

        shift = Operations.Shift(False)
        self.Assert(shift.DoAction(1), 10, "Shift Left DoAction()")
        self.Assert(shift.ToString(), ">>", "Shift Left ToString()")

        self.SetGroup("Insert")
        shift = Operations.Insert(12)
        self.Assert(shift.DoAction(1), 112, "Insert DoAction()")
        self.Assert(shift.ToString(), "Insert 12", "Insert ToString()")

        self.SetGroup("Translate")
        translate = Operations.Translate(1,2)
        self.Assert(translate.DoAction(121), 222, "Translate DoAction()")
        self.Assert(translate.ToString(), "1=>2", "Translate ToString()")

        self.SetGroup("Pow")
        powOp = Operations.Pow()
        self.Assert(powOp.DoAction(4), 16, "Pow DoAction()")
        self.Assert(powOp.ToString(), "Pow 2", "Pow ToString()")

        self.SetGroup("Flip")
        flip = Operations.Flip()
        self.Assert(flip.DoAction(1), -1, "Flip DoAction()")
        self.Assert(flip.ToString(), "+/- ", "Flip ToString()")

        self.SetGroup("Reverse")
        reverse = Operations.Reverse()
        self.Assert(reverse.DoAction(1234), 4321, "Reverse DoAction()")
        self.Assert(reverse.ToString(), "Reverse", "Reverse ToString()")

        self.SetGroup("Sum")
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
