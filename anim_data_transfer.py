def readButtonPush(*args):
    """
        Reads animation data from file
    """        
    #Change the path to the desired file    
    filename = "C:\Users\emachines\Desktop\workfile.txt"
    selected = mc.ls(selection = True)
    f = open(filename, 'r+')
    line = " "
    while line != "":
        endit = 0
        line = f.readline()
        weightState = 0
        if line[:5] == "anim ":
            buffer = line.split()
            size = len(buffer)
            node = buffer[3]
            attr = buffer[2]
            curAttr = node + "." + attr
            curAttrTest = node + "."
            if mc.objExists(node):
                test = mc.ls(curAttr)
                if test != curAttrTest:
                    while endit == 0:
                        line = f.readline()
                        if line[2:11] == "weighted ":
                            if line[11:12] == 1:
                                weightState = 1
                        if line[2:14] == "preInfinity ":
                            buffer = line.split()
                            buffer = buffer[1].split(';')
                            preInfinity = buffer[0]
                        if line[2:15] == "postInfinity ":
                            buffer = line.split()
                            buffer = buffer[1].split(';')
                            postInfinity = buffer[0]
                        if line[2:8] == "keys {":
                            line = f.readline()
                            while line[2:3] != "}":
                                buffer = line.split()
                                numberOfArguments = len(buffer)
                                time = buffer[0]
                                value = buffer[1]
                                inType = buffer[2]
                                outType = buffer[3]
                                tanLock = buffer[4]
                                weightLock = buffer[5]
                                if numberOfArguments == 7:
                                    buffer2 = buffer[6].split(';')
                                    breakDown = buffer2[0]
                                else:
                                    breakDown = buffer[6]
                                    if numberOfArguments > 7:
                                        tanAngle1 = buffer[7]
                                        buffer2 = buffer[8].split(';')
                                        tanWeight1 = float(buffer2[0])
                                    if numberOfArguments > 9:
                                        tanAngle2 = buffer[9]
                                        buffer2 = buffer[8].split(';')
                                        tanWeight2 = float(buffer2[0])
                                mc.setKeyframe(node, attribute = attr, breakdown= int(breakDown), time = time, value = float(value))
                                tanl=0                                                        
                                t1=float(time)
                                t2=int(t1)
                                mc.keyTangent(node, attribute = attr, lock = tanl, time = (t2,t2))
                                if weightState == 1:
                                    mc.keyTangent(node, edit = True, attribute = attr, weightedTangents = True)
                                    mc.keyTangent(node, attribute = attr, time = time, weightLock = weightLock)
                                if inType != "fixed" and outType != "fixed":
                                    mc.keyTangent(node, edit = True, absolute = True, attribute = attr, inTangentType = inType, outTangentType = outType,
                                    time = (t2,t2))
                                if inType == "fixed" and outType != "fixed":
                                    mc.keyTangent(node, edit = True, absolute = True, attribute = attr, inAngle = tanAngle1, inTangentType = inType,
                                    inWeight = tanWeight1, outTangentType = outType, time = (t2,t2))
                                if inType != "fixed" and outType == "fixed":
                                    mc.keyTangent(node, edit = True, absolute = True, attribute = attr, outAngle = tanAngle1, inTangentType = inType,
                                    inWeight = tanWeight1, outTangentType = outType, time = (t2,t2))
                                if inType == "fixed" and outType == "fixed":
                                    mc.keyTangent(node, edit = True, absolute = True, attribute = attr, inAngle = tanAngle1, inTangentType = inType,
                                    inWeight = tanWeight1, outAngle = tanAngle2, outTangentType = outType, outWeight = tanWeight2, time = (t2,t2))
                                line = f.readline()
                            mc.setInfinity( attribute = attr, postInfinite = postInfinity, preInfinite = preInfinity)
                            endit = 1
                else:
                    print 'Warning: ' + curAttr + ' does not exist!'
            else:
                print 'Warning: ' + node + 'does not exist!'
    f.close()
    print 'Done reading animation curves'
    mc.select(clear = True)
    for item in selected:
        mc.select(item, toggle = True)

def writeButtonPush(*args):
    #Change the path to the desired file
    filename = "C:\Users\emachines\Desktop\workfile.txt"
    selected = mc.ls(selection = True)
    f = open(filename, 'w')
    objects = mc.ls(long = True, selection = True)
    for item in objects:
        shortItem = mc.ls(item, selection = True)
        channels = mc.listConnections(item)
        for chan in channels:
            connects = mc.listConnections(chan, plugs = True)
            curAttr = connects[0]
            buffer = curAttr.split('.')
            num = len(buffer)
            num = num - 1
            node = ""
            for i in range(num):
                if i == 0:
                    node = buffer[i]
                else:
                    node = node + "." + buffer[i]
            nodeTemp = mc.ls(node, long = True)
            attr = buffer[num]
            node = nodeTemp[0]
            nodeTemp = mc.listRelatives(node, parent = True)
            if nodeTemp != "":
                parent = "1"
            else:
                parent = "0"
            testit = mc.listAnimatable(curAttr)
            testit2 = mc.keyframe(chan, query = True, keyframeCount = True)
            if testit[0] != "" and testit2 != 0:
                expr = chan + ".preInfinity"
                value = mc.getAttr(expr)
                if value == 0:
                    preIn = "constant"
                elif value == 1:
                    preIn = "linear"
                elif value == 2:
                    preIn = "constant"
                elif value == 3:
                    preIn = "cycle"
                elif value == 4:
                    preIn = "cycleRelative"
                elif value == 5:
                    preIn = "oscillate"
                expr = chan + ".postInfinity"
                value = mc.getAttr(expr)
                if value == 0:
                    postIn = "constant"
                elif value == 1:
                    postIn = "linear"
                elif value == 2:
                    postIn = "constant"
                elif value == 3:
                    postIn = "cycle"
                elif value == 4:
                    postIn = "cycleRelative"
                elif value == 5:
                    postIn = "oscillate"
                expr = chan + ".weightedTangents"
                weighted = mc.getAttr(expr)
                f.write("anim " + attr + " " + attr + " " + node + " " + parent + " 0 0;\n")
                f.write("animData {\n")
                f.write("  weighted " + str(weighted) + ";\n")
                f.write("  preInfinity " + preIn + ";\n")
                f.write("  postInfinity " + postIn + ";\n")
                f.write("  keys {\n")
                keys = mc.keyframe(chan, query = True)
                num = mc.keyframe(chan, query = True, keyframeCount = True)
                values = mc.keyframe(chan, query = True, valueChange = True)
                inTan = mc.keyTangent(chan, query = True, inTangentType = True)
                outTan = mc.keyTangent(chan, query = True, outTangentType = True)
                tanLock = mc.keyTangent(chan, query = True, lock = True)
                weightLock = mc.keyTangent(chan, query = True, weightLock = True)
                breakDown = mc.keyframe(chan, query = True, breakdown = True)
                inAngle = mc.keyTangent(chan, query = True, inAngle = True)
                outAngle = mc.keyTangent(chan, query = True, outAngle = True)
                inWeight = mc.keyTangent(chan, query = True, inWeight = True)
                outWeight = mc.keyTangent(chan, query = True, outWeight = True)
                for i in range(num):
                    if breakDown is None:
                        bd = 0
                    else:
                        for bd_item in breakDown:
                            if bd_item == keys[i]:
                                bd = 1
                    f.write("    " + str(keys[i]) + " " + str(values[i]) + " " + str(inTan[i]) + " " + str(outTan[i]) + " " + str(tanLock[i]) + " " + str(weightLock[i]) + " " + str(bd))
                    if inTan[i] == "fixed":
                        f.write(" " + inAngle[i] + " " + inWeight[i])
                    if outTan[i] == "fixed":
                        f.write(" " + outAngle[i] + " " + outWeight[i])
                    f.write(";\n")
                f.write("  }\n}\n")
    f.close()
    mc.select(clear = True)
    for item in selected:
        mc.select(item, toggle = True)
    print '\nDone writing animation curves'
    
transferWindow = mc.window(title = 'Animation data transfer', widthHeight = (110,55), resizeToFitChildren = True)
mc.columnLayout(rowSpacing = 5)
mc.button(label='Write data to file', command = writeButtonPush )
mc.button(label='Read data from file', command = readButtonPush )
mc.showWindow()
