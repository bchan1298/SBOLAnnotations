from sbol import * # noqa
import ipywidgets as widgets


def findModulesInDoc(doc):
    device_test_context = None
    device_test = None
    device = None

    for md in doc.moduleDefinitions:
        if md.displayId == 'context':
            device_test_context = md
        if md.displayId == 'device_test':
            device_test = md
        if md.displayId == 'device':
            device = md

    return (device_test_context, device_test, device)


def createDTCList(doc, originalCDs, addedCDs, cdDisplayIDMap):
    dtcList = []
    for cd in originalCDs:
        cdDisplayIDMap[cd.displayId] = cd
        dtcList.append(cd.displayId)
        for c in cd.components:
            subCD = doc.getComponentDefinition(c.definition)
            cdDisplayIDMap[subCD.displayId] = subCD
            dtcList.append(c.name.replace(' ', '_'))

    for cd in addedCDs:
        cdDisplayIDMap[cd.displayId] = cd
        dtcList.append(cd.displayId)

    dtcList.sort()
    return dtcList


def createColumnWidgets(moduleNames, componentLists, nameList, selectedLists, leftVBox, rightVBox): # noqa
    hBoxChildren = []
    for module in moduleNames:
        vBox = widgets.VBox()

        label = widgets.HTML('<h4>' + module + '</h4>')
        textBox = widgets.Text(value='',
                               placeholder=str('Enter ' + module + ' name'),
                               layout=widgets.Layout(width='265px'),
                               description='Name:',
                               style={'description_width': '40px'},
                               disabled=False)
        selectList = widgets.SelectMultiple(options=componentLists[module],
                                            description='',
                                            rows=20,
                                            layout=widgets.Layout(width='265px')) # noqa

        nameList.append(textBox)
        selectedLists.append(selectList)

        vBox.children = [label, textBox, selectList]

        hBoxChildren.append(vBox)

        if module == 'Device-Test-Context':
            hBoxChildren.append(leftVBox)

        if module == 'Device-Test':
            hBoxChildren.append(rightVBox)

    return hBoxChildren


# Device-Test-Context -> Device-Test
def leftRightClick(selectedLists, componentLists):
    dtcListWidget = selectedLists[0]
    dtListWidget = selectedLists[1]

    dtcList = componentLists['Device-Test-Context']
    dtList = componentLists['Device-Test']

    for selected in dtcListWidget.value:
        dtcList.remove(selected)
        dtList.append(selected)

    dtcList.sort()
    dtList.sort()

    dtcListWidget.options = dtcList
    dtListWidget.options = dtList


# Device-Test -> Device-Test-Context
def leftLeftClick(selectedLists, componentLists):
    dtListWidget = selectedLists[1]
    dtcListWidget = selectedLists[0]

    dtList = componentLists['Device-Test']
    dtcList = componentLists['Device-Test-Context']

    for selected in dtListWidget.value:
        dtList.remove(selected)
        dtcList.append(selected)

    dtList.sort()
    dtcList.sort()

    dtListWidget.options = dtList
    dtcListWidget.options = dtcList


# Device-Test -> Device
def rightRightClick(selectedLists, componentLists):
    dtListWidget = selectedLists[1]
    dListWidget = selectedLists[2]

    dtList = componentLists['Device-Test']
    dList = componentLists['Device']

    for selected in dtListWidget.value:
        dtList.remove(selected)
        dList.append(selected)

    dtList.sort()
    dList.sort()

    dtListWidget.options = dtList
    dListWidget.options = dList


# Device -> Device-Test
def rightLeftClick(selectedLists, componentLists):
    dListWidget = selectedLists[2]
    dtListWidget = selectedLists[1]

    dList = componentLists['Device']
    dtList = componentLists['Device-Test']

    for selected in dListWidget.value:
        dList.remove(selected)
        dtList.append(selected)

    dList.sort()
    dtList.sort()

    dListWidget.options = dList
    dtListWidget.options = dtList


plasmidPartDictionary = {}  # fc displayid : component in component definition
addedPlasmidParts = {}  # fc displayid : functional component


def addPlasmidParts(doc, originalCDs, device_test, device, plasmidPartDictionary, addedPlasmidParts): # noqa
    device_test_context, device_test, device = findModulesInDoc(doc)
    for plasmid in originalCDs:
        name = plasmid.displayId

        dtName = name + '__'
        dName = name + '__'

        dtList = []
        dList = []

        for fc in device_test.functionalComponents:
            if name in fc.displayId:
                dtList.append(fc)
                dtName += fc.displayId.replace(name + '_', '') + '__'

        for fc in device.functionalComponents:
            if name in fc.displayId:
                dList.append(fc)
                dName += fc.displayId.replace(name + '_', '') + '__'

        if len(dtList) != 0:
            dtCD = ComponentDefinition(dtName[:-2]) # noqa
            fcList = []

            for fc in dtList:
                c = dtCD.components.create(fc.displayId)
                c.definition = fc.definition

                plasmidPartDictionary[fc.displayId] = c
                fcList.append(fc.displayId)

            try:
                doc.addComponentDefinition(dtCD)
            except: # noqa
                pass

            fc = device_test.functionalComponents.create(dtName[:-2])
            fc.definiton = dtCD.identity

            for fcD in fcList:
                addedPlasmidParts[fcD] = fc

        if len(dList) != 0:
            dCD = ComponentDefinition(dName[:-2]) # noqa
            fcList = []

            for fc in dList:
                c = dCD.components.create(fc.displayId)
                c.definition = fc.definition

                plasmidPartDictionary[fc.displayId] = c
                fcList.append(fc.displayId)

            try:
                doc.addComponentDefinition(dCD)
            except: # noqa
                pass

            fc = device.functionalComponents.create(dName[:-2])
            fc.definition = dCD.identity

            for fcD in fcList:
                addedPlasmidParts[fcD] = fc


def resetModules(device_test_context, device_test, device):
    device.functionalComponents.clear()
    device_test.functionalComponents.clear()
    device_test_context.functionalComponents.clear()


def setNames(device_test_context, device_test, device, nameList):
    device_test_context.name = nameList[0].value
    device_test.name = nameList[1].value
    device.name = nameList[2].value


def createFunctionalComponents(doc,
                               selectedLists,
                               cdDisplayIDMap,
                               modulesDictionary,
                               moduleNames,
                               fcDictionary):

    for index, selectWidget in enumerate(selectedLists):
        currentModule = modulesDictionary[moduleNames[index]]

        for component in selectWidget.options:
            fc = currentModule.functionalComponents.create(component)
            fc.definition = cdDisplayIDMap[component]
            fc.direction = SBOL_DIRECTION_NONE # noqa

            cd = doc.getComponentDefinition(fc.definition)
            fcDictionary[component] = cd.name
