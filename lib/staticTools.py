from lib.header import *
from PyQt4 import QtGui 

"""
Semantic designer tools (sdt) are used for getting a good and logical look of the data for the user.
Basicly it knows how to make html out of raw data.
"""
class sdt:
    @staticmethod
    def aB(text):
        alertBox = QtGui.QMessageBox()
        alertBox.setText(text)
        alertBox.exec__()
    @staticmethod
    def calcDaySpace(startdate,  enddate,  wc,  weekendDays, noCalendar = False):
        if startdate.daysTo(enddate) == 0:
            daySpace = 1
        elif startdate.month() != enddate.month() and noCalendar==False:
            allDays = startdate.daysTo(enddate)
            if startdate.month() == wc.month():
                daySpace = allDays - enddate.day()+1
            else:
                daySpace = allDays - (startdate.daysInMonth() - startdate.day())
        elif noCalendar:
                daySpace = startdate.daysTo(enddate) + 1
        else:
            daySpace = startdate.daysTo(enddate) + 1
        weekendPart = int(daySpace / 7) * weekendDays
        daySpace = daySpace - weekendPart
        return (daySpace,  weekendPart)
    @staticmethod
    def createJobRow(ui,  job, company, workCalendar,  rowNr, sum):
        colNr = 0
        if not singleView:
            if ui.filterAll.isChecked() and ui.filterCalendar .isChecked():
                daySpace,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays)
            else:
                daySpace,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays, noCalendar=True)
            
        else:
            daySpace,  weekendPart = (workCalendar.daysInMonth() - (job.weekendDays * 4), job.weekendDays)
        #minSpace = daySpace * job.hours * 60
        loanSum,  loanDistractionSum, realHourLoan, realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
        #building table..
        if not singleView:
            w = QtGui.QTableWidgetItem(str(company.name))
            w.setToolTip(company.describtion)
            ui.infoExel.setItem(rowNr,  colNr,   w)
            colNr = colNr + 1
        w = QtGui.QTableWidgetItem(job.name)
        w.setToolTip(job.comment)
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.place) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(str(job.leader) ))
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(loanSum) + ".- ("+maths.rounder(realHourLoan)+"/std)" ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(maths.rounder((daySpace * job.hours)+job.correctionHours) +" Std")
        w.setToolTip(tr("From")+" "+job.startdate.toString(dbDateFormat)+" to "+job.enddate.toString(dbDateFormat)+ "<hr />"+maths.rounder(daySpace)+ "d (*"+str(job.hours)+"h)+"+str(job.correctionHours)+"correctionH. "+str(weekendPart)+"d was Weekenddays")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(chargeSum)+".- " ))
        colNr = colNr + 1
        w = QtGui.QTableWidgetItem(maths.rounder(realHourSplitSum)+".- @all")
        w.setToolTip(maths.rounder(loanDistractionSum)+".-/"+str(company.perHours)+tr("h")+")")
        ui.infoExel.setItem(rowNr,  colNr,   w)
        colNr = colNr + 1
        ui.infoExel.setItem(rowNr,  colNr,  QtGui.QTableWidgetItem(maths.rounder(sum + loanSum)+".-" ))
        return loanSum
    @staticmethod
    def colorChanger(color):
        if color > 200:
            return 25
        else:
            return color + 53
    @staticmethod
    def updateGraphicView(ui, companyList, workCalendar, infoSearch):
        #logger.debug("|SDT| update GraphicView")
        pen=QtGui.QPen(QtCore.Qt.red)
        r, g, b=(120, 77, 99)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setWidth(4)
        if ui.filterAll.isChecked() and ui.filterCalendar.isChecked():
            widthPerHour = 2.8
        else:
            widthPerHour = 2.0
        scene = QtGui.QGraphicsScene()
        pen.setColor(QtGui.QColor(188, 188, 188))
        scene.addLine(0,0,450,0,pen)
        pen=QtGui.QPen(QtCore.Qt.yellow)
        r, g, b=(120, 77, 99)
        pen.setColor(QtGui.QColor(r, g, b))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setWidth(1)
        #lastLine = 0
        oldDaySpace = 0.00
        oldValue = 0.00
        allValue = 0
#         qtPainter = QtGui.QPainter()
#         brush = QtGui.QBrush()
#         brush.setColor(QtGui.QColor(120,120,250))
#         qtPainter.setBackground()
        for company in companyList:
            for job in company.jobs:
                if cw.insertJobYesNo(ui, company, job, infoSearch, workCalendar):
                    daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
                    loanSum,  loanDistractionSum, realHourLoan,  realHourSplitSum,  chargeSum = maths.calcJobSum(company,  job,  workCalendar)
                    daySpace = ((daySpace * job.hours) + job.correctionHours )
                    daySpace = (daySpace + oldDaySpace) / 2
                    value = ((company.loan/10)*daySpace)
                    allValue += value
                    scene.addLine(float(oldDaySpace),0,float(daySpace*widthPerHour)/2,float(-loanSum/40),pen)
                    scene.addLine(float(daySpace*widthPerHour)/2,float(-loanSum/40),float(daySpace*widthPerHour),0,pen)
                    # old - scene.addLine(float(oldDaySpace),float(-oldValue),float(daySpace*widthPerHour),float(-loanSum/50),pen)
                    oldDaySpace = daySpace*widthPerHour
                    #oldValue = loanSum/50
                    r=sdt.colorChanger(r)
                    g=sdt.colorChanger(g)
                    b=sdt.colorChanger(b)
                    pen.setColor(QtGui.QColor(r, g, b))
        ui.graphView.setScene(scene)
        
    @staticmethod 
    def createCreditTextBox(company, ui):
        wc = QtCore.QDate.fromString(str(ui.workCalendar.monthShown())+"."+str(ui.workCalendar.yearShown()),"M.yyyy")
        creditString =""
        fCreditString = ""
        creditSum = 0
        #change to check credit-list-size
        for credit in company.credits:
            if (ui.filterCalendar.isChecked() and credit.date.month() == wc.month() and credit.date.year() == wc.year()) or ui.filterCalendar.isChecked() == False:
                creditSum += credit.value
                creditString += "<li><pre>"+credit.name+" @"+credit.date.toString(dbDateFormat)+":      "+str(credit.value)+"</pre><li/>"
        if len(company.credits) > 0 and creditSum > 0:
            fCreditString = "<ul>"
            creditString += "</ul>"+company.name+": "+str(creditSum)+"<br />"
            fCreditString += creditString
        return (fCreditString,  creditSum)
    @staticmethod
    def createDetailText(company, workCalendar, cvCalIsChecked):
        #logger.debug("|SDT| create DetailText")
        text = ""
        text += "<h1>"+company.name+"</h1>"+company.describtion+"<br />"+tr("Loan")+": "+str(company.loan)+" (per "+str(company.perHours)+tr("h")+")<hr />"
        loanDistractionSum = 0
        #LoanSplits
        text += "<h4>"+tr("loanDistractions")+"</h4><ul>"
        for ls in  company.loanDistractions:
            text += "<li>"+ls.name+": "+str(ls.value)
            if ls.money:
                loanDistractionSum += ls.value
                text += ".- </li>"
            else:
                inMoney = (company.loan / 100) * ls.value
                loanDistractionSum += inMoney
                text += "% ("+maths.rounder(inMoney)+".-) </li>"
        text += "</ul>"
        if loanDistractionSum > 0:
            text += tr("Loandistractionsum")+": "+maths.rounder(loanDistractionSum)+".-/"+str(company.perHours)+" "+tr("h")+"<hr />"
        creditSum = 0
        text += "<h4>"+tr("Credits")+"</h4><ul><pre>"
        for credit in company.credits:
            if (credit.date.month() == workCalendar.month() and credit.date.year() == workCalendar.year()) or True is not cvCalIsChecked:
                creditSum += credit.value
                text += "<li>"+credit.date.toString(dbDateFormat) + ": "+str(credit.value)+""
                if credit.payed:
                    text +=".-      "+ tr("is")+" "+tr("payed")+"</li>"
                else:
                    text +=".-      "+ tr("is NOT")+" "+tr("payed")+"</li>"
        text += "</ul></pre>"
        if creditSum > 0:
            text += tr("Creditsum")+": "+maths.rounder(creditSum)+".- <hr />"
        jobSum = 0
        jobDays = 0
        jobHours = 0

        chargeSum = 0
        text += "<h4>"+tr("Jobs")+"</h4>"
        text += "<ul>"
        for job in company.jobs:
            if cvCalIsChecked:
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar):
                    days,  weekendPart = sdt.calcDaySpace(job.startdate,  job.enddate, workCalendar,  job.weekendDays)
                else:
                    days = -1
            else:
                days = job.startdate.daysTo(job.enddate) + 1
            if days != -1:
                jobDays += days
                hourSpace = days * (job.hours / company.perHours ) +job.correctionHours
                jobHours += hourSpace
                jobSum += company.loan * hourSpace
                text += "<li>"+job.name+": "+maths.rounder(days)+"d * ("+maths.rounder(job.hours)+"h /"+str(company.perHours)+" )+" +str(job.correctionHours)+"h = "+maths.rounder(hourSpace)+"h * " + str(company.loan)+".-  ="+maths.rounder(hourSpace*company.loan)+".- </li>"
                text += "<ul>"
                for charge in job.wcharges:
                    if charge.howManyTimes > 0:
                        chargeSum += charge.value * charge.howManyTimes
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(charge.howManyTimes)+" times = "+maths.rounder(charge.value * charge.howManyTimes)+".-     (Sum: "+maths.rounder(chargeSum)+")</pre></li>"
                    else:
                        chargeSum += charge.value * days
                        text += "<li><pre>"+charge.name+": "+str(charge.value)+".- * "+str(days)+" days = "+maths.rounder(charge.value * days)+".-     (Sum: "+maths.rounder(chargeSum)+")</pre></li>"
                text += "</ul>"
        text += "</ul> Sum: "+maths.rounder(jobSum)+".- in "+maths.rounder(jobHours)+"h / "+maths.rounder(jobDays )+" d (+ "+maths.rounder(chargeSum)+".- charges) <hr />"
        if jobDays != 0:
            loanDistractionSumDays = loanDistractionSum * (jobDays * (jobHours/jobDays))
        else:
            loanDistractionSumDays = 0
        result = jobSum - loanDistractionSumDays - creditSum + chargeSum
        #the end of all results..
        text += "<h4>"+tr("Summary")+"</h4>"
        text += "<ul><li><b>"+maths.rounder(jobSum)+".-</b> </li><li><b> - "+maths.rounder(loanDistractionSumDays)+".-  </b>"+tr("Splits")+"</li><li><b> - "+maths.rounder(creditSum)+".- </b>"+tr(  "Credits")+"</li> <li><b> + "+maths.rounder(chargeSum)+".- </b> "+tr("Charges")+"</li></ul><hr /> "+tr("Your company should pay")+"<b> "+maths.rounder(result)+".- </b>"
        return text

    @staticmethod
    def createPersonalFinancesHtml(pfList, ui):
        pfHtml = "<ul>"
        pfSum = 0
        timeRepeat = 0
        calChecked = ui.pfCalendarEnabled.isChecked()
        for pf in pfList:
            if cw.ifInsertPersonalFinance(ui,pf):
                if pf.repeat != "None":
                    if pf.repeat=="Daily":
                        if calChecked:
                            timeRepeat = pf.date.daysInMonth() - pf.date.day()
                            if not pf.timesRepeat > timeRepeat:
                                 timeRepeat = pf.timesRepeat
                        else:
                            timeRepeat = pf.timesRepeat

                    elif pf.repeat=="Weekly":
                        if calChecked:
                            timeRepeat = pf.date.daysInMonth() - pf.date.day()
                            timeRepeat = timeRepeat / 7
                            if not pf.timesRepeat > timeRepeat:
                                 timeRepeat = pf.timesRepeat

                    
                pfHtml += "<li>" + pf.name+" @ "+pf.date.toString(dbDateFormat)+": "+pf.plusMinus+str(pf.value)+".- in "+str(timeRepeat)+" times = "+str(pf.value*timeRepeat)+"</li>"
                if pf.plusMinus == "+":
                    pfSum += pf.value
                else:
                    pfSum -= pf.value
        pfHtml += "</ul> <h3>Summe: "+str(pfSum)+"</h3>"
        return pfHtml
      
#cw = condition-wrapper
class cw:
    @staticmethod
    def checkForValidDate(startdate, enddate,  wCalendarDate):
        return (startdate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year()) or (enddate.month() == wCalendarDate.month() and startdate.year() == wCalendarDate.year())
    def filterTextSearch(infoSearch,  job,  company):
        return (re.search(infoSearch,  job.name.lower()) is not None  or re.search(infoSearch,  job.place.lower()) is not None or re.search(infoSearch,  job.comment.lower()) is not None or re.search(infoSearch,  job.leader.lower()) is not None or re.search(infoSearch, company.name.lower()) is not None)
    @staticmethod
    def ifInsertPersonalFinance(ui,  pf):
        pfCal = QtCore.QDate.fromString(str(ui.pfCalendar.monthShown())+"."+str(ui.pfCalendar.yearShown()), "M.yyyy")
        pfSearch = ui.pfSearch.text()
        pfSearch = pfSearch.lower()
        if ui.pfCalendarEnabled.isChecked() == False and ui.pfSearchEnabled.isChecked()==False:
            return True
        elif ui.pfCalendarEnabled.isChecked() and ui.pfSearchEnabled.isChecked()==False:
            if pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year():
                return True
        elif  ui.pfCalendarEnabled.isChecked() == False and  ui.pfSearchEnabled.isChecked():
            if ui.pfSearch.text() == "":
                return True
            elif re.search(pfSearch,  pf.name.lower()) is not None:
                return True
        elif ui.pfCalendarEnabled.isChecked() and ui.pfSearchEnabled.isChecked():
            if ui.pfSearch.text() == "" and  (pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year()):
                return True
            elif re.search(pfSearch,  pf.name.lower()) is not None  and  (pf.date.month() == pfCal.month() and pf.date.year() == pfCal.year()):
                return True
        else:
            return False
    @staticmethod
    def insertJobYesNo(ui, company, job, infoSearch, workCalendar):
        insertARow = False
        if ui.filterAll.isChecked():
            #cal + search
            if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch != "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and  cw.filterTextSearch(infoSearch, job, company):
                    #(ui,  job, company, rowNr,  daySpace, singleView, sum)
                    insertARow = True
            #cal +inactive + search
            if ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch != "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                    insertARow = True
            #search
            elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch != "":
                if cw.filterTextSearch(infoSearch, job, company):
                    insertARow = True
            #----- no filters (but filter@all)
            elif ui.filterCalendar.isChecked() == False and ui.filterInactive.isChecked() and infoSearch == "": 
                insertARow = True
            #calendar
            elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() and infoSearch == "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar):
                    insertARow = True
            #inactive calendar
            elif ui.filterCalendar.isChecked() and ui.filterInactive.isChecked() == False and infoSearch == "":
                if cw.checkForValidDate(job.startdate, job.enddate, workCalendar) and job.active == 1:
                    insertARow = True
            #inactive
            elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch == "":
                if  job.active == 1:
                    insertARow = True
            #inactive + search
            elif ui.filterCalendar.isChecked() ==False and ui.filterInactive.isChecked() == False and infoSearch != "":
                if  cw.filterTextSearch(infoSearch, job, company) and job.active == 1:
                    insertARow = True
        else:
            insertARow = True
        return insertARow

            
      
class maths:
    @staticmethod
    def rounder(nr):
        origNr = nr
        intNr = int(nr)
        afterComma = nr - intNr
        stringComma = str(afterComma)
        if len(stringComma) >= 5:
            stringComma = str(abs(float(stringComma)))
            if int(stringComma[4:5]) > 5:
                correctAfterComma = int(stringComma[2:3]) + 1
            else:
                correctAfterComma = int(stringComma[2:3]) 
            floatString = str(intNr)+"."+str(correctAfterComma)
            return floatString
        else:
            return str(origNr)
    
    @staticmethod
    def calcJobSum(company,  job, workCalendar):
        daySpace,  weekendPart = sdt.calcDaySpace(job.startdate, job.enddate, workCalendar,  job.weekendDays)
        hrSpace = daySpace * job.hours + job.correctionHours
        chargeSum = 0
        for charge in job.wcharges:
            if charge.howManyTimes == 0:
                chargeValue = daySpace * charge.value
            else:
                chargeValue = charge.howManyTimes * charge.value
            chargeSum += chargeValue
        loanDistractionSum = 0
        for loanDistraction in company.loanDistractions:
            if loanDistraction.money:
                loanDistractionSum += loanDistraction.value
            else:
                loanDistractionSum += (company.loan / 100) * loanDistraction.value
        realHourLoan = (company.loan - loanDistractionSum) 
        realHourSplitSum= loanDistractionSum * (hrSpace / company.perHours)
        loanSum = realHourLoan * (hrSpace / company.perHours) + chargeSum
        return  (loanSum,  loanDistractionSum, realHourLoan, realHourSplitSum,  chargeSum)

