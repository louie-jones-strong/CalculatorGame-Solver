import GameSolver
import Operations


def TestOperations():
    #Add
    add = Operations.Add(1)
    assert add.DoAction(1) == 2

    return

def TestSolves():
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
    TestOperations()
    TestSolves()
    input("")
