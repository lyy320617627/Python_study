import copy


def result_sum(param):
    list_lt_a = []
    a_result = 0
    for o in param:
        if float(o[4]) < 0:
            a_result = a_result + float(o[4])
            list_lt_a.append(o)
    # 去重
    list_aa = [i for i in param if i not in list_lt_a]
    # 将负数列表最后一项值变为sum后的值
    if len(list_lt_a) > 0:
        list_lt_a[-1][4] = str(a_result)
    else:
        return param
    # 将相加负数添加到列表最后一项
    list_lt_a[-1][-4] = ' '
    list_aa.append(list_lt_a[-1])

    return list_aa


def main(args):
    args = [
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 728000.0, '2022-10-20', '2023-01-18', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', -30000.0, '2022-09-26', '2022-09-26', '逾期43天', '分销', '33000000', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', -30000.0, '2022-09-26', '2022-09-26', '逾期43天', '分销', '33000000', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 20000.0, '2022-10-28', '2023-01-26', '', '分销', '33000400', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 20000.0, '2022-10-28', '2023-01-26', '', '分销', '33000400', 1000]];
    list_all = args
    maps = dict()
    list_a = []
    list_b = []
    list_c = []

    for t in list_all:
        if (t[-3] == "分销"):
            list_a.append(t)
        elif (("零售") in t[-3]):
            list_b.append(t)
        else:
            list_c.append(t)
    result_a = []
    result_b = []
    result_c = []
    if len(list_a) > 0:
        if all(map(lambda x: float(x[4]) < 0, list_a)) == True:
            result_a = list_a
        else:
            result_a = result_sum(list_a)
    if len(list_b) > 0:
        if all(map(lambda x: float(x[4]) < 0, list_b)) == True:
            result_b = list_b
        else:
            result_b = result_sum(list_b)
    if len(list_c) > 0:
        if all(map(lambda x: float(x[4]) < 0, list_c)) == True:
            result_c = list_c
        else:
            result_c = result_sum(list_c)

    # result_b=[]
    resultall = result_b + result_a + result_c

    boolean = False
    amount = 0
    # 返回总金额

    for i in resultall:
        i[0] = " "
        i[1] = " "
        i[2] = " "
        i[3] = " "
        i[-1] = " "
        i[-2] = " "
        i[-5] = str(i[-5])[0:10]
        i[-6] = str(i[-6])[0:10]
        if (float(i[4]) < 0):
            i[-4] = ''
        amount = amount + float(i[4])
        if float(i[4]) > 0 and i[-3] != "互联网":
            boolean = True
        # 即将到期的账款
    if boolean == False:
        amount = 0

    lingshous = []
    fenxiaos = []
    internts = []

    newlingshous = []
    newfenxiaos = []
    newinternts = []
    for i in resultall:
        if ('零售' in i[-3]):
            lingshous.append(i)
        elif ('分销' == i[-3]):
            fenxiaos.append(i)
        elif ('互联网' == i[-3]):
            internts.append(i)
        else:
            print()
    newlingshous = copy.deepcopy(lingshous)
    newfenxiaos = copy.deepcopy(fenxiaos)
    newinternts = copy.deepcopy(internts)

    summ = 0.0
    if (len(lingshous) > 0):
        if all(map(lambda x: float(x[4]) < 0, lingshous)) == True:
            print('true')
        elif (float(lingshous[-1][4]) < 0):
            for a in lingshous:
                summ = summ + float(a[4])
                res = 0.0
                res = summ + float(lingshous[-1][4])
                newlingshous.remove(a)
                if (res > 0):
                    a[4] = copy.deepcopy(res)
                    newlingshous.insert(0, a)
                    newlingshous.remove(newlingshous[-1])
                    break;
                else:
                    if (len(newlingshous) == 1):
                        newlingshous[0][4] = copy.deepcopy(res)
                        break;
    summb = 0.0
    if (len(fenxiaos) > 0):
        if all(map(lambda x: float(x[4]) < 0, fenxiaos)) == True:
            print('true')
        elif (float(fenxiaos[-1][4]) < 0):
            for b in fenxiaos:
                summb = summb + float(b[4])
                resb = 0.0
                resb = summb + float(fenxiaos[-1][4])
                newfenxiaos.remove(b)
                if (resb > 0):
                    b[4] = copy.deepcopy(resb)
                    newfenxiaos.insert(0, b)
                    newfenxiaos.remove(newfenxiaos[-1])
                    break;
                else:
                    if (len(newfenxiaos) == 1):
                        newfenxiaos[0][4] = copy.deepcopy(resb)
                        # b[4]=copy.deepcopy(resb)
                        break;

    summc = 0.0
    if (len(internts) > 0):
        if all(map(lambda x: float(x[4]) < 0, internts)) == True:
            print('true')
        elif (float(internts[-1][4]) < 0):
            for c in internts:
                summc = summc + float(c[4])
                resc = 0.0
                resc = summc + float(internts[-1][4])
                newinternts.remove(c)
                if (resc > 0):
                    c[4] = copy.deepcopy(resc)
                    newinternts.insert(0, c)
                    newinternts.remove(newinternts[-1])
                    break;
                else:
                    if (len(newinternts) == 1):
                        newinternts[0][4] = copy.deepcopy(resc)
                        break;

    result = newlingshous + newfenxiaos + newinternts
    # 即将到期的账款

    # note
    # 今日到期
    # 明日到期
    # 5日内到期
    # 逾期*天

    # 零售/分销

    aTodayList = []
    aTomorrow = []
    aFiveDays = []
    aFifteenDays = []
    aLateList = []

    bTodayList = []
    bTomorrow = []
    bFiveDays = []
    bFifteenDays = []
    bLateList = []

    cTodayList = []
    cTomorrow = []
    cFiveDays = []
    cFifteenDays = []
    cLateList = []

    retailList = []
    distributionList = []
    internetList = []

    retailResult = []
    distributionResult = []
    internetResult = []

    for r in result:
        if (("零售") in r[-3]):
            retailList.append(r)
        elif (("分销") == r[-3]):
            distributionList.append(r)
        elif (("互联网") == r[-3]):
            internetList.append(r)

    if (len(retailList) > 0):
        for a in retailList:
            aList = []
            aList.append(a[4])
            aList.append(a[-4])
            if (("零售") in a[-3]):
                aList.append("零售")
            else:
                aList.append(a[-3])
            if (aList[1] == '今日到期'):
                aTodayList.append(aList)
            elif (aList[1] == '明日到期'):
                aTomorrow.append(aList)
            elif (aList[1] == '5日内到期'):
                aFiveDays.append(aList)
            elif (aList[1] == '15日内到期'):
                aFifteenDays.append(aList)
            elif ('逾期' in aList[1]):
                aLateList.append(aList)
            else:
                print("不符合")
        atsum = 0
        awsum = 0
        afsum = 0
        ansum = 0
        alsum = 0
        if (len(aTodayList) > 0):
            for at in aTodayList:
                atsum = atsum + float(at[0])
            aTodayList.clear()
            if (atsum > 0):
                aTodayList.append(atsum)
            else:
                aTodayList.append("-")
            aTodayList.append("今日到期")
            aTodayList.append("零售")

        if (len(aTomorrow) > 0):
            for aw in aTomorrow:
                awsum = awsum + float(aw[0])
            aTomorrow.clear()
            if (awsum > 0):
                aTomorrow.append(awsum)
            else:
                aTomorrow.append("-")
            aTomorrow.append("明日到期")
            aTomorrow.append("零售")

        if (len(aFiveDays) > 0):
            for af in aFiveDays:
                afsum = afsum + float(af[0])
            aFiveDays.clear()
            if (afsum > 0):
                aFiveDays.append(afsum)
            else:
                aFiveDays.append("-")
            aFiveDays.append("5日内到期")
            aFiveDays.append("零售")

        if (len(aFifteenDays) > 0):
            for an in aFifteenDays:
                ansum = ansum + float(an[0])
            aFifteenDays.clear()
            if (ansum > 0):
                aFifteenDays.append(ansum)
            else:
                aFifteenDays.append("-")
            aFifteenDays.append("15日内到期")
            aFifteenDays.append("零售")

        if (len(aLateList) > 0):
            for al in aLateList:
                alsum = alsum + float(al[0])
            aLateList.clear()
            if (alsum > 0):
                aLateList.append(alsum)
            else:
                aLateList.append("-")
            aLateList.append("逾期*天")
            aLateList.append("零售")

    if (len(distributionList) > 0):
        for b in distributionList:
            bList = []
            bList.append(b[4])
            bList.append(b[-4])
            bList.append(b[-3])
            if (bList[1] == '今日到期'):
                bTodayList.append(bList)
            elif (bList[1] == '明日到期'):
                bTomorrow.append(bList)
            elif (bList[1] == '5日内到期'):
                bFiveDays.append(bList)
            elif (bList[1] == '15日内到期'):
                bFifteenDays.append(bList)
            elif ('逾期' in bList[1]):
                bLateList.append(bList)
            else:
                print("不符合")
        btsum = 0
        bwsum = 0
        bfsum = 0
        bnsum = 0
        blsum = 0
        if (len(bTodayList) > 0):
            for bt in bTodayList:
                btsum = btsum + float(bt[0])
            bTodayList.clear()
            if (btsum > 0):
                bTodayList.append(btsum)
            else:
                bTodayList.append("-")
            bTodayList.append("今日到期")
            bTodayList.append("分销")

        if (len(bTomorrow) > 0):
            for bw in bTomorrow:
                bwsum = bwsum + float(bw[0])
            bTomorrow.clear()
            if (bwsum > 0):
                bTomorrow.append(bwsum)
            else:
                bTomorrow.append("-")
            bTomorrow.append("明日到期")
            bTomorrow.append("分销")

        if (len(bFiveDays) > 0):
            for bf in bFiveDays:
                bfsum = bfsum + float(bf[0])
            bFiveDays.clear()
            if (bfsum > 0):
                bFiveDays.append(bfsum)
            else:
                bFiveDays.append("-")
            bFiveDays.append("5日内到期")
            bFiveDays.append("分销")

        if (len(bFifteenDays) > 0):
            for bn in bFifteenDays:
                bnsum = bnsum + float(bn[0])
            bFifteenDays.clear()
            if (bnsum > 0):
                bFifteenDays.append(bnsum)
            else:
                bFifteenDays.append("-")
            bFifteenDays.append("15日内到期")
            bFifteenDays.append("分销")

        if (len(bLateList) > 0):
            for bl in bLateList:
                blsum = blsum + float(bl[0])
                print("blsum:{blsum}")
            bLateList.clear()
            if (blsum > 0):
                bLateList.append(blsum)
            else:
                bLateList.append("-")
            bLateList.append("逾期*天")
            bLateList.append("分销")

    if (len(internetList) > 0):
        for c in internetList:
            cList = []
            cList.append(c[4])
            cList.append(c[-4])
            cList.append(c[-3])
            if (cList[1] == '今日到期'):
                cTodayList.append(cList)
            elif (cList[1] == '明日到期'):
                cTomorrow.append(cList)
            elif (cList[1] == '5日内到期'):
                cFiveDays.append(cList)
            elif (cList[1] == '15日内到期'):
                cFifteenDays.append(cList)
            elif ('逾期' in cList[1]):
                cLateList.append(cList)
            else:
                print("不符合")

        ctsum = 0
        cwsum = 0
        cfsum = 0
        cnsum = 0
        clsum = 0
        if (len(cTodayList) > 0):
            for ct in cTodayList:
                ctsum = ctsum + float(ct[0])
            cTodayList.clear()
            if (ctsum > 0):
                cTodayList.append(ctsum)
            else:
                cTodayList.append("-")
            cTodayList.append("今日到期")
            cTodayList.append("互联网")

        if (len(cTomorrow) > 0):
            for cw in cTomorrow:
                cwsum = cwsum + float(cw[0])
            cTomorrow.clear()
            if (cwsum > 0):
                cTomorrow.append(cwsum)
            else:
                cTomorrow.append("-")
            cTomorrow.append("明日到期")
            cTomorrow.append("互联网")

        if (len(cFiveDays) > 0):
            for cf in cFiveDays:
                cfsum = cfsum + float(cf[0])
            cFiveDays.clear()
            if (cfsum > 0):
                cFiveDays.append(cfsum)
            else:
                cFiveDays.append("-")
            cFiveDays.append("5日内到期")
            cFiveDays.append("互联网")

        if (len(cFifteenDays) > 0):
            for cn in cFifteenDays:
                cnsum = cnsum + float(cn[0])
            cFifteenDays.clear()
            if (cnsum > 0):
                cFifteenDays.append(cnsum)
            else:
                cFifteenDays.append("-")
            cFifteenDays.append("15日内到期")
            cFifteenDays.append("互联网")

        if (len(cLateList) > 0):
            for cl in cLateList:
                clsum = clsum + float(cl[0])
            cLateList.clear()
            if (clsum > 0):
                cLateList.append(clsum)
            else:
                cLateList.append("-")
            cLateList.append("逾期*天")
            cLateList.append("互联网")

    # for k in distributionList:
    # for l in internetList:

    eTodayList = ["-", "今日到期", "零售"]
    eTomorrow = ["-", "明日到期", "零售"]
    eFiveDays = ["-", "5日内到期", "零售"]
    eFifteenDays = ["-", "15日内到期", "零售"]
    eLateList = ["-", "逾期*天", "零售"]

    fTodayList = ["-", "今日到期", "分销"]
    fTomorrow = ["-", "明日到期", "分销"]
    fFiveDays = ["-", "5日内到期", "分销"]
    fFifteenDays = ["-", "15日内到期", "分销"]
    fLateList = ["-", "逾期*天", "分销"]

    gTodayList = ["-", "今日到期", "互联网"]
    gTomorrow = ["-", "明日到期", "互联网"]
    gFiveDays = ["-", "5日内到期", "互联网"]
    gFifteenDays = ["-", "15日内到期", "互联网"]
    gLateList = ["-", "逾期*天", "互联网"]

    eTodayList = aTodayList if len(aTodayList) > 0 else eTodayList
    eTomorrow = aTomorrow if len(aTomorrow) > 0 else eTomorrow
    eFiveDays = aFiveDays if len(aFiveDays) > 0 else eFiveDays
    eFifteenDays = aFifteenDays if len(aFifteenDays) > 0 else eFifteenDays
    eLateList = aLateList if len(aLateList) > 0 else eLateList

    fTodayList = bTodayList if len(bTodayList) > 0 else fTodayList
    fTomorrow = bTomorrow if len(bTomorrow) > 0 else fTomorrow
    fFiveDays = bFiveDays if len(bFiveDays) > 0 else fFiveDays
    fFifteenDays = bFifteenDays if len(bFifteenDays) > 0 else fFifteenDays
    fLateList = bLateList if len(bLateList) > 0 else fLateList

    gTodayList = cTodayList if len(cTodayList) > 0 else gTodayList
    gTomorrow = cTomorrow if len(cTomorrow) > 0 else gTomorrow
    gFiveDays = cFiveDays if len(cFiveDays) > 0 else gFiveDays
    gFifteenDays = cFifteenDays if len(cFifteenDays) > 0 else gFifteenDays
    gLateList = cLateList if len(cLateList) > 0 else gLateList

    resultList = []

    resultList.append(eTodayList)
    resultList.append(eTomorrow)
    resultList.append(eFiveDays)
    resultList.append(eFifteenDays)
    resultList.append(eLateList)
    print(f"在appendeLateList:\n{resultList} eLateList长度为:{len(eLateList)}")
    resultList.append(fTodayList)
    print(f"在appendfTodayList:\n{resultList} fTodayList:{len(fTodayList)}")
    resultList.append(fTomorrow)
    print(f"在appendfTomorrow:\n{resultList} fTomorrow长度为:{len(fTomorrow)}")
    resultList.append(fFiveDays)
    print(f"在appendfFiveDays:\n{resultList} fFiveDays长度为:{len(fFiveDays)}")
    resultList.append(fFifteenDays)
    print(f"在appendfFifteenDays:\n{resultList} fFifteenDays长度为:{len(fFifteenDays)}")
    resultList.append(fLateList)
    print(f"在appendfLateList:\n{resultList} fLateList长度为:{len(fLateList)}")
    resultList.append(gTodayList)
    resultList.append(gTomorrow)
    resultList.append(gFiveDays)
    resultList.append(gFifteenDays)
    resultList.append(gLateList)
    print(f"resultlist:\n{resultList} 长度为：{len(resultList)}")

    results = []
    p = 0
    m = 0
    n = 0
    for re in resultList:
        if (re[0] == '-' and re[2] == '零售'):
            p = p + 1
        if (re[0] == '-' and re[2] == '分销'):
            m = m + 1
        if (re[0] == '-' and re[2] == '互联网'):
            n = n + 1

    if (p != 5):
        results.append(eTodayList)
        results.append(eTomorrow)
        results.append(eFiveDays)
        results.append(eFifteenDays)
        results.append(eLateList)
        results.append([])
    if (m != 5):
        results.append(fTodayList)
        results.append(fTomorrow)
        results.append(fFiveDays)
        results.append(fFifteenDays)
        results.append(fLateList)
        results.append([])
    if (n != 5):
        results.append(gTodayList)
        results.append(gTomorrow)
        results.append(gFiveDays)
        results.append(gFifteenDays)
        results.append(gLateList)
        results.append([])

    print(results)

    maps = {"result": result, "boolean": boolean, "amount": amount, "dateList": results}

    print(maps)
    return maps
    pass
args = [
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 728000.0, '2022-10-20', '2023-01-18', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 6500.0, '2022-10-21', '2023-01-19', '', '嘉兴零售', '33000400', 2000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', -30000.0, '2022-09-26', '2022-09-26', '逾期43天', '分销', '33000000', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', -30000.0, '2022-09-26', '2022-09-26', '逾期43天', '分销', '33000000', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 20000.0, '2022-10-28', '2023-01-26', '', '分销', '33000400', 1000],
            [101257, '中移建设有限公司嘉兴分公司', 2000000.0, ' ', 20000.0, '2022-10-28', '2023-01-26', '', '分销', '33000400', 1000]];
main(args)