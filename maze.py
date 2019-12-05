import copy
import os
culdimatrix = []
from itertools import chain

class MazeError(Exception):
    def __init__(self,message):
        print(message)
class Maze():
    def __init__(self,file):
        self.file = file
        self.gates=0
        self.walls=0
        self.inaccessPoint=0
        self.accessibleArea=0
        self.culDeSac=0
        self.entryExitPath=0
        self.grid = []
        self.gridNew =[]
        self.dir_grid = []
        self.gridWalls = []
        self.gateSet = []
        self.gridWalls2 = []
        self.accessibleListInner = []
        self.accessibleList = []
        self.dirc = None
        self.countCuld =0
        self.countGate =0
        self.e=0
        self.uniquePath =[]
        self.uniquePathInner =[]
        self.displayPath = []
        self.displayPathInner = []
        self.culd_matrix_new = []

        input=open(file).readlines()
        input = [line.replace('',' ') for line in input]
        for line in input:
            if not line.isspace():
                readLine = line.strip().split()
                self.dir_grid.append(readLine)
                self.grid.append([int(e) for e in readLine])

        self.rowLength=len(self.grid[0])
        self.gridLength=len(self.grid)

        uiop = self.grid
        self.gridNew = copy.deepcopy(self.grid)
        self.gridDisplayWalls = copy.deepcopy(self.grid)

        for i in range(0,self.gridLength-1):

            self.temp = []
            for j in range(0,self.rowLength-1):
                countWalls = 0

                if self.grid[i][j] == 1 or self.grid[i][j] == 2:
                    countWalls+=1
                elif self.grid[i][j] == 3:
                    countWalls+=2
                if self.grid[i+1][j] == 3 or self.grid[i+1][j]== 1:
                    countWalls+=1
                if self.grid[i][j+1] == 2 or self.grid[i][j+1]== 3:
                    countWalls+=1
                self.temp.append(4-countWalls)
            self.gridWalls.append(self.temp)
        self.matrix_check()
        self.gridWalls2=copy.deepcopy(self.gridWalls)
        self.gridWallLength = len(self.gridWalls)
        self.gridWallRowLength = len(self.gridWalls[0])

        self.count_of_gates = self.calculateGates()

        self.count_of_walls = self.calculateWalls()
        self.count_of_accessibleAreas, self.count_of_inaccessiblePoints = self.inaccessiblePoints()
        self.count_of_culDeSacs = self.culDeSacs()
        self.count_of_entryExitPath = self.entryExitPathFn()


    def analyse(self):
        self.initialCheck(self.count_of_gates, self.count_of_walls, self.count_of_accessibleAreas, self.count_of_inaccessiblePoints, self.count_of_culDeSacs, self.count_of_entryExitPath)

    def matrix_check(self):

        if not 2<= self.gridLength <=41:
            raise MazeError('Incorrect input.')
        gridwidth = len(self.gridNew[0])
        if not 2 <= gridwidth <= 31:
            raise MazeError('Incorrect input.')

        for row in self.gridNew:
            for elem in row:
                if elem not in [0, 1, 2, 3]:
                    raise MazeError('Incorrect input.')

        for row in self.gridNew:
            if len(row) != len(self.gridNew[0]):
                raise MazeError('Incorrect input.')

        for i in range(self.gridLength):
            if self.gridNew[i][-1] == 3 or self.gridNew[i][-1] == 1:
                raise MazeError('Input does not represent a maze.')

        for i in range(self.gridLength):
            for j in range(len(self.gridNew[i])):
                if not len(self.gridNew[i]) == gridwidth:
                    raise MazeError('Incorrect input.')
                if self.gridNew[-1][j] == 3 or self.gridNew[-1][j] == 2:
                    raise MazeError('Input does not represent a maze.')

    def initialCheck(self,gates,walls,accessibleAreas,inaccessiblePoints,culDeSacs,entryExitPath):
        if gates == 0:
            print(f'The maze has no gate.')
        elif gates == 1:
            print(f'The maze has a single gate.')
        else:
            print(f'The maze has {gates} gates.')

        if walls == 0:
            print(f'The maze has no wall.')
        elif walls == 1:
            print(f'The maze has walls that are all connected')
        else:
            print(f'The maze has {walls} sets of walls that are all connected.')

        if inaccessiblePoints == 0:
            print(f'The maze has no inaccessible inner point.')
        elif inaccessiblePoints == 1:
            print(f'The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {inaccessiblePoints} inaccessible inner points.')

        if accessibleAreas == 0:
            print(f'The maze has no accessible area.')
        elif accessibleAreas == 1:
            print(f'The maze has a unique accessible area.')
        else:
            print(f'The maze has {accessibleAreas} accessible areas.')

        if culDeSacs == 0:
            print(f'The maze has no accessible cul-de-sac.')
        elif culDeSacs == 1:
            print(f'The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {culDeSacs} sets of accessible cul-de-sacs that are all connected.')

        if entryExitPath == 0:
            print(f'The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif entryExitPath == 1:
            print(f'The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {entryExitPath} entry-exit paths with no intersections not to cul-de-sacs.')

    def calculateGates(self):
        #print(self.grid)
        gateCount =0
        #print('------')
        self.tup = ()
        for i in range(0,len(self.grid)):
            if i == 0 or i == len(self.grid)-1:
                for j in range(0,len(self.grid[i])-1):
                    if self.grid[i][j] == 0 or self.grid[i][j] == 2:
                        if i == 0:
                            self.tup = (i, j)
                            self.gateSet.append(self.tup)
                        if i == len(self.grid) - 1:
                            self.tup = (i-1, j)
                            self.gateSet.append(self.tup)
                        gateCount+=1
        for k in range(0,len(self.grid)-1):
            if self.grid[k][0] == 0 or self.grid[k][0] == 1:
                self.tup=(k,0)
                self.gateSet.append(self.tup)
                gateCount+=1
            if self.grid[k][len(self.grid[k])-1] == 0:
                self.gateSet.append((k, len(self.grid[k])-1))
                self.tup = (k-1,len(self.grid[k])-1)
                self.gateSet.append(self.tup)
                gateCount+=1
        return gateCount

    def calculateWalls(self):
        walls =0
        for i in range(0,self.gridLength):
            for j in range(0,self.rowLength):
                if self.grid[i][j] == 0 or self.grid[i][j] < 0:
                    continue
                else:
                    self.recurFunction(i,j)

                    walls+=1
        return walls

    def recurFunction(self,row,col):
        if col <0 or col == self.rowLength or row<0 or row == self.gridLength:
            return
        if self.grid[row][col] < 0:# or self.grid[row][col] == '0':
            return

        if self.leftCheck(row,col):
            self.grid[row][col] = -1#self.grid[row][col]+1*(-1)
            self.recurFunction(row,col-1)

        if self.topCheck(row,col):
            self.grid[row][col] = -1#self.grid[row][col]+1*(-1)
            self.recurFunction(row-1,col)

        if self.rightCheck(row,col):
            self.grid[row][col] = -1#self.grid[row][col]+1*(-1)
            self.recurFunction(row,col+1)

        if self.downCheck(row,col):
            self.grid[row][col] = -1#self.grid[row][col]+1*(-1)
            self.recurFunction(row + 1, col)

    def leftCheck(self, r, c):
        if self.dir_grid[r][c-1] == '1' or self.dir_grid[r][c-1] == '3':
            return True

    def rightCheck(self, r, c):
        if self.dir_grid[r][c] == '1' or self.dir_grid[r][c] == '3':# or self.dir_grid[r][c] == '0':
            return True

    def topCheck(self, r, c):
        if self.dir_grid[r - 1][c] == '2' or self.dir_grid[r - 1][c] == '3':# or self.dir_grid[r - 1][c] == '0':
            return True
        return False

    def downCheck(self, r, c):
        if self.dir_grid[r][c] == '2' or self.dir_grid[r][c] == '3':# or self.dir_grid[r][c] == '0':
            return True

    def passLeft(self,r,c):
        if self.gridNew[r][c] != 2 and self.gridNew[r][c] != 3:
            return True
        return False

    def passTop(self,r,c):
        h=self.gridNew[r][c]
        s=self.gridNew[r][c] != 1
        return self.gridNew[r][c] != 1 and self.gridNew[r][c] != 3

    def passRight(self,r,c):
        if self.gridNew[r][c+1] != 2 and self.gridNew[r][c+1] != 3:
            return True
        return False

    def passDown(self,r,c):
        if self.gridNew[r+1][c] != 1 and self.gridNew[r+1][c] != 3:
            return True
        return False

    def inaccessiblePoints(self):
        l=0
        for i in range(self.gridWallLength):
            for j in range(self.gridWallRowLength):
                self.accessibleListInner = []

                if (i,j) in self.gateSet:
                    if self.gridWalls[i][j] != -1 and self.gridWalls[i][j] != 0:
                        self.accessibleListInner.append((i, j))
                        self.recurInaccess(i,j)
                        if self.accessibleListInner not in self.accessibleList:
                            self.accessibleList.append(self.accessibleListInner)
                        self.accessibleArea += 1

        for i in range(self.gridWallLength):
            for j in range(self.gridWallRowLength):
                if self.gridWalls[i][j] != -1:
                    l += 1
        return self.accessibleArea, l

    def recurInaccess(self,row,col):
        if col < 0 or col == self.gridWallRowLength or row < 0 or row == self.gridWallLength:
            return

        if self.gridWalls[row][col] == -1:
            return
        p=self.gridNew[row][col]
        q=self.gridWalls[row][col]
        if self.passLeft(row,col):
            if (row,col) not in self.accessibleListInner:
                self.accessibleListInner.append((row, col))
            self.gridWalls[row][col] = -1
            self.recurInaccess(row,col-1)
        if self.passTop(row,col) is True:
            if (row,col) not in self.accessibleListInner:
                self.accessibleListInner.append((row, col))
            self.gridWalls[row][col] = -1
            self.recurInaccess(row-1,col)
        if self.passRight(row,col):
            if (row,col) not in self.accessibleListInner:
                self.accessibleListInner.append((row, col))
            self.gridWalls[row][col] = -1
            self.recurInaccess(row,col+1)
        if self.passDown(row,col):
            if (row,col) not in self.accessibleListInner:
                self.accessibleListInner.append((row, col))
            self.gridWalls[row][col] = -1
            self.recurInaccess(row+1,col)

    def boundaryCheck(self,r,c):
        if c < 0 or c == self.gridWallRowLength or r < 0 or r == self.gridWallLength:
            return False
        return True
    def culDeSacs(self):
        culdList =[]
        for e in self.accessibleList:
            while True:
                cul_de_sac_present = False
                for r,c in e:
                    if self.gridWalls2[r][c] == 1:
                        cul_de_sac_present = True
                        self.gridWalls2[r][c] = -1
                        culdList.append((r,c))
                        self.checkCulDeSacs(r,c,e,culdList)
                if not cul_de_sac_present:
                    break
        countCuld=0
        check = False
        self.culd_matrix_new = copy.deepcopy(self.gridWalls2)
        return self.getCuldPaths()


    def getCuldPaths(self):
        count = 0
        for i in range(self.gridWallLength):
            for j in range(self.gridWallRowLength):
                if self.culd_matrix_new[i][j] == -1 and self.culd_matrix_new[i][j] != -10:
                    count+=1
                    self.culd_matrix_new[i][j] = -10
                    self.culdPathTraverse(i,j)
        return count
        
    def culdPathTraverse(self,row,col):
        if self.culd_matrix_new[row][col] == -1:
            return
        p =self.gridNew[row][col]
        q = self.gridWalls[row][col]
        if self.passLeft(row, col):
            if not col-1 < 0:
                if self.culd_matrix_new[row][col-1] == -1:
                    self.culd_matrix_new[row][col-1] = -10
                    self.culdPathTraverse(row,col-1)
        if self.passTop(row,col) is True:
            if not row-1 < 0:
                if self.culd_matrix_new[row-1][col] == -1:
                    self.culd_matrix_new[row-1][col] = -10
                    self.culdPathTraverse(row-1,col)
        if self.passRight(row,col):
            if col+1 != self.gridWallRowLength:
                if self.culd_matrix_new[row][col+1] == -1:
                    self.culd_matrix_new[row][col+1] = -10
                    self.culdPathTraverse(row,col+1)
        if self.passDown(row,col):
            if row+1 != self.gridWallLength:
                if self.culd_matrix_new[row+1][col] == -1:
                    self.culd_matrix_new[row+1][col] = -10
                    self.culdPathTraverse(row+1,col)

    def culdRecur(self,i,j,e,countCuld):
        if self.gridWalls2[i][j] == -1:
            countCuld+=1
            return countCuld
        if self.passLeft(i, j):
            if (i, j - 1) in e:
                if self.boundaryCheck(i, j - 1):
                    countCuld=self.culdRecur(i,j-1,e,countCuld)
        if self.passTop(i, j):
            if (i - 1, j) in e:
                if self.boundaryCheck(i - 1, j):
                    countCuld=self.culdRecur(i - 1, j, e,countCuld)
        if self.passDown(i, j):
            if (i + 1, j) in e:
                if self.boundaryCheck(i + 1, j):
                    countCuld=self.culdRecur(i+1, j, e,countCuld)
        if self.passRight(i, j):
            if (i, j + 1) in e:
                if self.boundaryCheck(i, j + 1):
                    countCuld=self.culdRecur(i, j + 1, e,countCuld)
        return countCuld

    def checkCulDeSacs(self,i,j,e,culdList):
        if self.passLeft(i,j):
            if (i, j - 1) in e:
                if self.boundaryCheck(i,j-1):
                    if self.gridWalls2[i][j-1] != -1:
                        self.gridWalls2[i][j-1] -= 1
        if self.passTop(i,j):
            if (i - 1, j) in e:
                if self.boundaryCheck(i-1,j):
                    if self.gridWalls2[i-1][j] != -1:
                        self.gridWalls2[i-1][j] -= 1
        if self.passDown(i, j):
            if (i + 1, j) in e:
                if self.boundaryCheck(i+1,j):
                    if self.gridWalls2[i+1][j] != -1:
                        self.gridWalls2[i+1][j] -= 1
        if self.passRight(i,j):
            if (i, j + 1) in e:
                if self.boundaryCheck(i,j+1):
                    if self.gridWalls2[i][j+1] != -1:
                        self.gridWalls2[i][j+1] -= 1


    def entryExitPathFn(self):
        for e in self.accessibleList:
            uniquePathInner = []
            for r,c in e:
                if self.gridWalls2[r][c] == 2:
                    uniquePathInner.append((r,c))
                elif self.gridWalls2[r][c] == -1:
                    continue
                else:
                    uniquePathInner.clear()
                    break
            if len(uniquePathInner) != 0:
                self.uniquePath.append(uniquePathInner)
        for i in range(self.gridWallLength):
            self.displayPathInner=[]
            for j in range(self.gridWallRowLength):
                self.displayPathInner.append(0)
            self.displayPath.append(self.displayPathInner)
        for i in self.uniquePath:
            for j in i:
                self.displayPath[j[0]][j[1]] = 1
        return len(self.uniquePath)

    def display(self):
        file = self.file.replace('.txt','.tex')
        with open(file, 'w') as tex_file:
            print(
                    '\\documentclass[10pt]{article}\n'
                    '\\usepackage{tikz}\n'
                    '\\usetikzlibrary{shapes.misc}\n'
                    '\\usepackage[margin=0cm]{geometry}\n'
                    '\\pagestyle{empty}\n'
                    '\\tikzstyle{every node}=[cross out, draw, red]\n'
                    
                    '\\begin{document}\n'
                    
                    '\\vspace*{\\fill}\n'
                    '\\begin{center}\n'
                    '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n',
                  file = tex_file)
            self.displayWalls(tex_file)
            self.displayPillars(tex_file)
            self.displayCulDeSacs(tex_file)
            self.displayUniquePath(tex_file)
            print('\\end{tikzpicture}\n'
                  '\\end{center}\n'
                  '\\vspace*{\\fill}\n\n'
                  '\\end{document}', file=tex_file
                  )
        os.system('pdflatex ' + file)

    def displayWalls(self,tex_file):
        print(f'% Walls', file=tex_file)
        count=0
        for i in range(self.gridLength):
            for j in range(1,self.rowLength):
                if count == 0 and (self.gridNew[i][j-1] == 1 or self.gridNew[i][j-1] == 3):
                    count += 1
                    print(f'    \\draw ({j-1},{i}) --',end='', file=tex_file)
                if self.gridNew[i][j] == 1 or self.gridNew[i][j] == 3:
                    continue
                if count > 0:
                    count=0
                    print(f' ({j},{i});', file=tex_file)
        for j in range(self.rowLength):
            for i in range(1, self.gridLength):
                if count == 0 and (self.gridNew[i-1][j] == 2 or self.gridNew[i-1][j] == 3):
                    count += 1
                    print(f'    \\draw ({j},{i-1}) --',end='', file=tex_file)
                if self.gridNew[i][j] == 2 or self.gridNew[i][j] == 3:
                    continue
                if count > 0:
                    count = 0
                    print(f' ({j},{i});', file=tex_file)

    def displayPillars(self,tex_file):
        print(f'% Pillars', file=tex_file)
        for i in range(self.gridLength):
            for j in range(self.rowLength):
                if self.gridDisplayWalls[i][j] == 0:
                    #if not self.boundaryCheck(i,j):
                    if (self.gridDisplayWalls[i-1][j] != 3 and self.gridDisplayWalls[i-1][j] != 2) and (self.gridDisplayWalls[i][j-1] != 3 and self.gridDisplayWalls[i][j-1] != 1):
                        print(f'    \\fill[green] ({j},{i}) circle(0.2);', file=tex_file)

    def displayCulDeSacs(self,tex_file):
        print(f'% Inner points in accessible cul-de-sacs', file=tex_file)
        for i in range(self.gridWallLength):
            for j in range(self.gridWallRowLength):
                if self.gridWalls2[i][j] == -1:
                    print(f'    \\node at ({j+0.5},{i+0.5}) {{}};', file=tex_file)



    def displayUniquePath(self, tex_file):
        print(f'% Entry-exit paths without intersections', file=tex_file)
        list=[]
        innerList = []
        innerInnerList = []
        innerList1 = []
        innerInnerList1 = []
        count=0
        for i in range(len(self.displayPath)):
            for j in range(len(self.displayPath[i])):
                # print(self.displayPath[i][j],i,j,self.rightCheck(i,j) )
                if self.displayPath[i][j] == 1:
                    #if self.rightCheck(i,j):
                    if self.dir_grid[i][j] == '1' or self.dir_grid[i][j] == '3' or self.dir_grid[i][j] == '0':
                        innerInnerList.append((i,j))
                        count+=1
                    else:
                        if len(innerInnerList) > 1:
                            innerList.append(innerInnerList)
                        innerInnerList=[]
                        count=0
                        innerInnerList.append((i,j))
                        count+=1
                else:
                    count=0
                    if len(innerInnerList) != 0 and len(innerInnerList) != 1 :
                        if len(innerInnerList) >1:
                            innerList.append(innerInnerList)
                    innerInnerList=[]
            if len(innerInnerList) > 1:
                innerList.append(innerInnerList)
            innerInnerList=[]
        col=0
        count1=0
        while col < len(self.displayPath[0]):
            count1 = 0
            for k in range(len(self.displayPath)):
                if self.displayPath[k][col] == 1:
                    if self.dir_grid[k][col] == '0' or self.dir_grid[k][col] == '2':
                        innerInnerList1.append((k,col))
                        count1+=1
                    else:
                        if len(innerInnerList1) > 1:
                            innerList1.append(innerInnerList1)
                        innerInnerList1=[]
                        count1=0
                        innerInnerList1.append((k,col))
                        count1+=1

                else:
                    count1 = 0
                    if len(innerInnerList1) != 0 and len(innerInnerList1) != 1:
                        if len(innerInnerList1) > 1:
                            innerList1.append(innerInnerList1)
                    innerInnerList1 = []
            if len(innerInnerList1) > 1:
                innerList1.append(innerInnerList1)
            col+=1
        for i in range(len(innerList)):
            print(f'    \draw[dashed, yellow] ({innerList[i][0][1]+0.5},{innerList[i][0][0]+0.5}) -- ({innerList[i][-1][1]+0.5},{innerList[i][-1][0]+0.5});',file=tex_file)

        for i in range(len(innerList1)):
            print(f'    \draw[dashed, yellow] ({innerList1[i][0][1]+0.5},{innerList1[i][0][0]+0.5}) -- ({innerList1[i][-1][1]+0.5},{innerList1[i][-1][0]+0.5});',file=tex_file)

