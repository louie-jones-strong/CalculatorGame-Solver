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
        return value == expectedValue

    def TestOperations(self):
        
        self.SetGroup("Add")
        add = Operations.Add()
        add.Setup(1)
        self.Assert(add.DoAction(1), 2, "+1 DoAction()")
        self.Assert(add.ToString(), "+1", "+1 ToString()")

        add = Operations.Add()
        add.Setup(-1)
        self.Assert(add.DoAction(1), 0, "-1 DoAction()")
        self.Assert(add.ToString(), "-1", "-1 ToString()")

        self.SetGroup("Multiply")
        multiply = Operations.Multiply()
        multiply.Setup(3)
        self.Assert(multiply.DoAction(1), 3, "3 DoAction()")
        self.Assert(multiply.ToString(), "X3", "3 ToString()")

        self.SetGroup("Divide")
        divide = Operations.Divide()
        divide.Setup(3)
        self.Assert(divide.DoAction(9), 3, "3 DoAction()")
        self.Assert(divide.ToString(), "/3", "3 ToString()")

        self.SetGroup("Shift")
        shiftRight = Operations.ShiftRight()
        shiftRight.Setup()
        self.Assert(shiftRight.DoAction(10), 1, "right DoAction()")
        self.Assert(shiftRight.ToString(), "<<", "right ToString()")

        shiftLeft = Operations.ShiftLeft()
        shiftLeft.Setup()
        self.Assert(shiftLeft.DoAction(1), 10, "Left DoAction()")
        self.Assert(shiftLeft.ToString(), ">>", "Left ToString()")

        self.SetGroup("Insert")
        insert = Operations.Insert()
        insert.Setup(12)
        self.Assert(insert.DoAction(1), 112, "DoAction()")
        self.Assert(insert.ToString(), "Insert 12", "ToString()")

        self.SetGroup("Translate")
        translate = Operations.Translate()
        translate.Setup(1,2)
        self.Assert(translate.DoAction(121), 222, "DoAction()")
        self.Assert(translate.ToString(), "1=>2", "ToString()")

        self.SetGroup("Pow")
        powOp = Operations.Pow()
        powOp.Setup()
        self.Assert(powOp.DoAction(4), 16, "DoAction()")
        self.Assert(powOp.ToString(), "Pow 2", "ToString()")

        self.SetGroup("Flip")
        flip = Operations.Flip()
        flip.Setup()
        self.Assert(flip.DoAction(1), -1, "DoAction()")
        self.Assert(flip.ToString(), "+/- ", "ToString()")

        self.SetGroup("Reverse")
        reverse = Operations.Reverse()
        reverse.Setup()
        self.Assert(reverse.DoAction(1234), 4321, "DoAction()")
        self.Assert(reverse.ToString(), "Reverse", "ToString()")

        self.SetGroup("Sum")
        sumOp = Operations.Sum()
        sumOp.Setup()
        self.Assert(sumOp.DoAction(1234), 10, "DoAction()")
        self.Assert(sumOp.ToString(), "Sum", "ToString()")


        return

    def TestSolves(self):
        
        self.SetGroup("Simple Solve")
        op = Operations.Add()
        op.Setup(1)
        found, steps = GameSolver.Solve(1, [op], 0, 1)
        self.Assert(found, True, "found Add Solve")
        return

if __name__ == "__main__":
    UnitTests()
