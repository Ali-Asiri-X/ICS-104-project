def main():
    try:
        sectionsInfo = open("sectionsInfo.txt","r")
        crnDictionary = dictionaryOfSectionsInfo(sectionsInfo)
        mainMenu()
        userInput = float(input("\nEnter your choice: "))
        uniqueCoursesDictionary = CourseStatistics(crnDictionary)
        while userInput != 8:
            if userInput == 1 :
                viewOfferedSections(crnDictionary)
            elif userInput == 2 :
                searchForSection(crnDictionary)
            elif userInput == 3 :
                updateSection (crnDictionary)
            elif userInput == 4 :
                deleteSection(crnDictionary)
            elif userInput == 5 :
                addSection(crnDictionary)
            elif userInput == 6 :
                printCourseStatistics(uniqueCoursesDictionary)
            elif userInput == 7 :
                printDepartmentStatistics(uniqueCoursesDictionary , crnDictionary)
            else :
                print("\nWrong input please choose again.")
            mainMenu()
            userInput = float(input("\nEnter your choice: "))

        sectionsInfo.close()
    except FileNotFoundError :
        print("Input file is not found")
    except ValueError :
        print("wrong input")

         
def dictionaryOfSectionsInfo(sectionsInfo):
    crnDictionary = {}
    for line in sectionsInfo:
        if line.rstrip() != "":
            courseDataList = (line.rstrip()).split(",")
            dictionaryKey = courseDataList[0]
            courseDataList.pop(0)
            crnDictionary[dictionaryKey]=courseDataList
    return crnDictionary
    
def mainMenu():
    print()
    print("Course Offering System")
    print("==============================")
    print("1. View offered sections")
    print("2. Search for a section")
    print("3. Update a section")
    print("4. Delete a section")
    print("5. Add new section")
    print("6. View Courses Information")
    print("7. View departments Information")
    print("8. Exit")
    print("===============================")

    
def header():
    #This function will print the header of tabular format.
    print("-"*127)
    print("%-7s%-47s%-19s%-15s%-21s%-7s%s" % ("CRN","Course name","Section number","Department","Number of students","Day","Time"))
    print("-"*127)
    
    
def viewOfferedSections(crnDictionary):
    #This function displays all Offered Sections in a proper tabular format.
    header()
    for key in crnDictionary:
        coursesInformation(key,crnDictionary)
        
        
def  searchForSection(crnDictionary):
    userInput = input("Enter C to search for a section by CRN Or N to search for a section by course name Or Q to quit: ")
    userInput = userInput.lower()
    while userInput != "q" :
        if userInput == "c":
            display_validate_crn(crnDictionary)
        
        elif userInput == "n":
            found = True
            userCourse = input("\nEnter the course name: ")
            for key in crnDictionary:
                infoList = crnDictionary[key]
                userCourse = (userCourse.replace(" ","")).lower()
                courseName = (infoList[0].replace(" ","")).lower()
                if userCourse in courseName:
                    if found:
                        header()
                        found = False
                    print("%-7s%-47s%-19s%-15s%-23s%-7s%s" % (key,infoList[0],infoList[1],infoList[2],infoList[3],infoList[4],infoList[5]))
            if found:
                print("\nError: Course name \"%s\" not found." % userCourse)
                
        else:
            print("\nWrong input please try again.")
            
        userInput = input("\nEnter C to search for a section by CRN Or N to search for a section by course name Or Q to quit: ")
        userInput = userInput.lower()
        
def updateSection (crnDictionary):
    userCrn = display_validate_crn(crnDictionary)
    if userCrn != None:
        userInput = input("Enter D to update the day OR T to update the time OR S to update the number of students and Q to quit: ")
        userInput = userInput.lower()
        while userInput != "q":
            if userInput == "d":
                userUpdate = input("please Enter the new day/s for the section\nU = sunday    M = monday    T = tuesday    W = wednseday    R = thursday : ")
                userUpdate = userUpdate.upper()
                checkFlag = True 
                for char in userUpdate:
                    if not char in "UMTWR":
                        checkFlag = False
                if checkFlag:
                    infoList = crnDictionary[userCrn] 
                    infoList.insert(4,userUpdate)
                    infoList.pop(5)
                    crnDictionary[userCrn] = infoList
                    updateFile(crnDictionary)

                else:
                    print("Error: Wrong day")

            elif userInput == "t":
                newStartingTime = input("please Enter the new starting time(0000) of the section: ")
                newEndingTime = input("please Enter the new ending time(0000) of the section :")
                if len(newStartingTime) != 4 or len(newEndingTime) != 4 or not newEndingTime.isdigit() or not newStartingTime.isdigit() or int(newStartingTime) < 0 or int(newStartingTime) >= 2400 or int(newEndingTime) < 0 or int(newEndingTime)>=2400:
                    print("Error: wrong time or not in the form of 0000")
                else:
                    newTime = newStartingTime+"-"+newEndingTime
                    infoList = crnDictionary[userCrn] 
                    infoList.insert(5,newTime)
                    infoList.pop(6)
                    crnDictionary[userCrn] = infoList
                    updateFile(crnDictionary)


            elif userInput == "s":
                numOfStudent = input("please Enter the new number of students in the section: ")
                if not numOfStudent.isdigit() or int(numOfStudent) < 0:
                    print("Error: wrong number")
                else:
                    infoList = crnDictionary[userCrn] 
                    infoList.insert(3,numOfStudent)
                    infoList.pop(4)
                    crnDictionary[userCrn] = infoList
                    updateFile(crnDictionary)
            else:
                print("Error: Wrong input(choose either D or T or S or Q)")


            userInput = input("Enter D to update the day OR T to update the time OR S to update the number of students and Q to quit: ")    
            userInput = userInput.lower()

def deleteSection(crnDictionary):
    userCrn = display_validate_crn(crnDictionary)
    if userCrn != None:
        userChoice = input("Are you sure that want to delete the section with CRN %s (Enter Y to confirm or press any key to return to main menu): ")
        userChoice = userChoice.upper()
        if userChoice == "Y":
            crnDictionary.pop(userCrn)
            updateFile(crnDictionary)
            
def addSection(crnDictionary):
    newCrn = input("Enter the crn: ")
    newCrn = newCrn.upper()
    while  not (newCrn.isdigit() and len(newCrn) == 5) and newCrn != "Q" :
        print("\nError: invalid CRN; please enter the CRN again.")
        newCrn = input("\nEnter the CRN of the section OR Q to quit: ")
        newCrn = newCrn.upper()
    if newCrn != "Q":
        courseName = input("Enter the course name OR Q to quit: ")
        courseName = courseName.strip().rstrip()
        if courseName.upper() != "Q": 
            sectionNum = input("Enter the section number OR Q to quit: ")
            sectionNum = sectionNum.upper()
            while not sectionNum.isdigit() and sectionNum != "Q" and int(sectionNum) < 1 and int(sectionNum) > 99 :
                sectionNum = input("Error: invalid section number; please enter the section number again OR Q to quit: ")
                sectionNum = sectionNum.upper()
            if sectionNum != "Q":
                Department = input("Enter the Department name OR Q to quit: ")
                Department = Department.strip().rstrip()
                if Department.upper() != "Q":
                    numOfStudent = input("Enter the number of students in the section OR Q to quit: ")
                    numOfStudent = numOfStudent.upper()
                    while not numOfStudent.isdigit() and numOfStudent != "Q" and float(numOfStudent) % 1 != 0 and int(numOfStudent) < 0:
                        numOfStudent = input("Error: invalid number of students; please enter the number of students again OR Q to quit: ")
                        numOfStudent = numOfStudent.upper()
                    if numOfStudent != "Q":
                        day = input("Enter the day OR Q to quit: ")
                        day = day.strip().rstrip().upper()
                        if day != "Q":
                            startingTime = input("Enter the starting time of the section OR Q to quit: ")
                            startingTime = startingTime.strip().rstrip()
                            if startingTime.upper() != "Q":
                                endingTime = input("Enter the ending time of the section OR Q to quit: ")
                                endingTime = endingTime.strip().rstrip()
                                if endingTime.upper() != "Q":
                                    infoList = []
                                    infoList.append(courseName)
                                    infoList.append(sectionNum)
                                    infoList.append(Department)
                                    infoList.append(numOfStudent)
                                    infoList.append(day)
                                    infoList.append(startingTime+"-"+endingTime)
                                    crnDictionary[newCrn] = infoList
                                    updateFile(crnDictionary)
                                

def printCourseStatistics(uniqueCoursesDictionary):
    print("Unique Courses table\n")
    print("-"*127)
    print("%-60s%-35s%s"%("Course Name","Number of offered section/s","number of the total students"))
    print("-"*127)
    for key in uniqueCoursesDictionary:
        print("%-60s%-35s%s"%(key,uniqueCoursesDictionary[key][0],uniqueCoursesDictionary[key][1]))

def printDepartmentStatistics(uniqueCoursesDictionary,crnDictionary):
    uniqueDepartmentDictionary = {}
    coursesPerDepartment = {}
    listOfCoursesPerDepartment = []
    for key in crnDictionary.values():
        if not key[2] in uniqueDepartmentDictionary:
            uniqueDepartmentDictionary[key[2]] = [1,int(key[3])] #key[3] is the number of students
                
        else:
            departmentInfoList = uniqueDepartmentDictionary[key[2]] #key[2] is the department name.
            numOfOfferedSections = departmentInfoList[0] + 1
            numOfStudents = int(departmentInfoList[1]) + int(key[3]) #key[3] is the number of students
            uniqueDepartmentDictionary[key[2]] = [numOfOfferedSections,numOfStudents]
            
    print("-"*127)        
    print("%-50s%-40s%-30s" % ("Department name","Total number of registered students","Total number of sections offered"))
    print("-"*127)
    for key in uniqueDepartmentDictionary:
        print("%-50s%-40s%-30s" % (key,uniqueDepartmentDictionary[key][1],uniqueDepartmentDictionary[key][0]))
    
    print()
    print("-"*127)
    print("%-20s%-48s%-30s%s" % ("Department name","Course name","Number of offered section/s","number of the total students"))
    print("-"*127)
    for courseName in uniqueCoursesDictionary:
        print("%-20s%-48s%-30s%s" % (uniqueCoursesDictionary[courseName][2],courseName,uniqueCoursesDictionary[courseName][0],uniqueCoursesDictionary[courseName][1]))
      
         
    
def CourseStatistics(crnDictionary):
    uniqueCoursesDictionary = {}
    for key in crnDictionary.values():
        if not key[0] in uniqueCoursesDictionary:
            uniqueCoursesDictionary[key[0]] = [1,int(key[3]),key[2]]
        else:
            courseInfoList = uniqueCoursesDictionary[key[0]]
            numOfOfferedSections = courseInfoList[0] + 1
            numOfStudents = int(courseInfoList[1]) + int(key[3])
            uniqueCoursesDictionary[key[0]] = [numOfOfferedSections,numOfStudents,key[2]]
    return uniqueCoursesDictionary
            

def display_validate_crn(crnDictionary):
    userCrn = input("Enter the CRN of the section: ")
    while not (userCrn.isdigit() and len(userCrn) == 5) and userCrn != "Q":
        print("\nError: invalid CRN; please enter the CRN again.")
        userCrn = input("\nEnter the CRN of the section Or Q to quit: ")
        
    checkFlag = False        
    for key in crnDictionary:
        if userCrn == key and userCrn.lower() != "q":
            header()
            listOFCourseData = crnDictionary[key]
            print("%-7s%-47s%-19s%-15s%-23s%-7s%s" % (key,listOFCourseData[0],listOFCourseData[1],listOFCourseData[2],listOFCourseData[3],listOFCourseData[4],listOFCourseData[5]))
            checkFlag = True     
    if not checkFlag :
        print("\nError: CRN not found.")    
    if checkFlag :
        return userCrn
    
def coursesInformation(key,crnDictionary):
    #This function displays the Course name and the complete details of the Course.
    listOFCourseData = crnDictionary[key]
    print("%-7s%-47s%-19s%-15s%-21s%-7s%s" % (key,listOFCourseData[0],listOFCourseData[1],listOFCourseData[2],listOFCourseData[3],listOFCourseData[4],listOFCourseData[5]))

def updateFile(crnDictionary):  
    sectionsInfo = open("sectionsInfo.txt","w")
    for key in crnDictionary:
        lineList = crnDictionary[key]
        sectionsInfo.write("%s,%s,%s,%s,%s,%s,%s\n" % (key,lineList[0],lineList[1],lineList[2],lineList[3],lineList[4],lineList[5]))
main() 
