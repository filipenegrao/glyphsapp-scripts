# -*- coding: utf-8 -*-

"""
This code uses several extracts from Toshi Omagari's Nudge-move by Numerical Value
published on https://github.com/Tosche/Glyphs-Scripts/blob/master/Path/Nudge-Move%20by%20Numerical%20Value.py
Thank you for the author to share these! 

"""

def nudge(onMv, off1, off2, onSt, offsetX, offsetY):
        try:
            # onST = starting on-curve
            # onMv = moving on-curve
            distanceX = onMv.x - onSt.x
            distanceX1 = onMv.x - off1.x
            distanceX2 = off2.x - onSt.x
            if distanceX != 0:
                valueX1 = distanceX1/distanceX
                valueX2 = distanceX2/distanceX
            else:
                valueX1 = 0
                valueX2 = 0
            if distanceX1 != 0:
                off1.x += (1-valueX1)*offsetX
            else:
                off1.x += offsetX

            if distanceX2 != 0:
                off2.x += (valueX2)*offsetX

            distanceY = onMv.y - onSt.y
            distanceY1 = onMv.y - off1.y
            distanceY2 = off2.y - onSt.y

            if distanceY1 != 0:
                off1.y += (1-distanceY1/distanceY)*offsetY
            else:
                off1.y += offsetY

            if distanceY2 != 0:
                off2.y += (distanceY2/distanceY)*offsetY

        except Exception, e:
            # brings macro window to front and reports error:
            Glyphs.showMacroWindow()
            print "Nudge-move by Numerical Value Error (nudge): %s" % e


def nudgeMove(val, direction):

    try:
        if direction is 'left':
            offsetX = -float(val)
            offsetY = 0.0

        elif direction is 'right':
            offsetX = float(val)
            offsetY = 0.0

        elif direction is 'up':
            offsetX = 0.0
            offsetY = float(val)

        elif direction is 'down':
            offsetX = 0.0
            offsetY = -float(val)
    
    except:
        Glyphs.displayDialog_withTitle_("Something got wrong...", "Let me know at hello@filipenegrao.com")

    try:
        Font = Glyphs.font # frontmost font
        Font.disableUpdateInterface()
        listOfSelectedLayers = Font.selectedLayers
        
        for thisLayer in Font.selectedLayers:
            glyph = thisLayer.parent
            glyph.beginUndo()
        
            for thisPath in thisLayer.paths:
                numOfNodes = len(thisPath.nodes)
        
                for i in range(numOfNodes):
                    node = thisPath.nodes[i]
                    if node in thisLayer.selection:
                        nodeBefore = thisPath.nodes[i-1]
                        if (nodeBefore != None) and (not nodeBefore in thisLayer.selection):
                            if nodeBefore.type == GSOFFCURVE: # if on-curve is the edge of selection
                                
                                if thisPath.nodes[i-2].type == GSOFFCURVE:
                                    oncurveMv = node
                                    offcurve1 = nodeBefore
                                    offcurve2 = thisPath.nodes[i-2]
                                    oncurveSt = thisPath.nodes[i-3]
                                    nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
                                
                                elif thisPath.nodes[i-2].type == GSCURVE: # if off-curve is the edge of selection
                                    oncurveMv = thisPath.nodes[i+1]
                                    offcurve1 = node
                                    offcurve2 = nodeBefore
                                    oncurveSt = thisPath.nodes[i-2]
                                    nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
                                    node.x -= offsetX
                                    node.y -= offsetY

                        nodeAfter = thisPath.nodes[i+1]

                        if (nodeAfter != None) and (not nodeAfter in thisLayer.selection):
                            if nodeAfter.type == GSOFFCURVE: # if on-curve is the edge of selection
                                if thisPath.nodes[i+2].type == GSOFFCURVE:
                                    oncurveMv = node
                                    offcurve1 = nodeAfter
                                    offcurve2 = thisPath.nodes[i+2]
                                    oncurveSt = thisPath.nodes[i+3]
                                    nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)

                                elif thisPath.nodes[i+2].type == GSCURVE: # if off-curve is the edge of selection
                                    thisPath.nodes[i-1].x -= offsetX
                                    thisPath.nodes[i-1].y -= offsetY
                                    oncurveMv = thisPath.nodes[i-1]
                                    offcurve1 = node
                                    offcurve2 = nodeAfter
                                    oncurveSt = thisPath.nodes[i+2]

                                    nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY)
                                    
                                    thisPath.nodes[i-1].x += offsetX
                                    thisPath.nodes[i-1].y += offsetY
                                    node.x -= offsetX
                                    node.y -= offsetY

                        node.x += offsetX
                        node.y += offsetY
            glyph.endUndo()
            Font.enableUpdateInterface()

    except Exception, e:
        # brings macro window to front and reports error:
        
        Glyphs.showMacroWindow()
        print "Nudge-move by Numerical Value Error: %s" % e