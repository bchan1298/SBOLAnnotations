from sbol import * # noqa
import ipywidgets as widgets


typeDict = {'http://www.biopax.org/release/biopax-level3.owl#DnaRegion': 'DNA',
            'http://www.biopax.org/release/biopax-level3.owl#RnaRegion': 'RNA',
            'http://www.biopax.org/release/biopax-level3.owl#Protein': 'Protein', # noqa
            'http://www.biopax.org/release/biopax-level3.owl#SmallMolecule': 'Small Molecule', # noqa
            'http://www.biopax.org/release/biopax-level3.owl#Complex': 'Complex'} # noqa

roleDict = {'http://identifiers.org/so/SO:0000001': 'Miscellaneous',
            'http://identifiers.org/so/SO:0000167': 'Promoter',
            'http://identifiers.org/so/SO:0000139': 'RBS',
            'http://identifiers.org/so/SO:0000316': 'CDS',
            'http://identifiers.org/so/SO:0000141': 'Terminator',
            'http://identifiers.org/so/SO:0000704': 'Gene',
            'http://identifiers.org/so/SO:0000057': 'Operator',
            'http://identifiers.org/so/SO:0000280': 'Engineered Gene',
            'http://identifiers.org/so/SO:0000234': 'mRNA',
            'http://identifiers.org/chebi/CHEBI:35224': 'Effector',
            'http://identifiers.org/go/GO:0003700': 'Transcription Factor'}


def fixCDNames(doc):
    for cd in doc.componentDefinitions:
        num = 0
        name = cd.displayId
        for sa in cd.sequenceAnnotations:
            if sa.name == 'misc_feature':
                sa.name = 'misc_feature' + str(num)
                num = num + 1

            if name not in sa.name:
                sa.name = name + '_' + sa.name
                sa.displayId = name + '_' + sa.displayId


def extractSeqAnnotations(doc, cdDictionary):
    copyCDs = list(doc.componentDefinitions).copy()
    for cd in copyCDs:
        currentName = cd.displayId
        if len(cd.components) == 0 and len(cd.sequenceAnnotations) != 0:
            for sa in cd.sequenceAnnotations:
                if sa.component is None:
                    createdCD = sa.extract()
                    createdCD.name = createdCD.displayId.replace(currentName + '_', '') # noqa
                    cdDictionary[currentName].append(createdCD)


def createHTMLString(cd, parentName=None):
    htmlString = ''
    if cd.description is not None:
        htmlString += '<dt><u>Description</u>:</dt>' + cd.description + '</dt>'
    if len(cd.types) != 0:
        htmlString += '<dt><u>Type(s)</u>:</dt>'
        for typeComponent in cd.types:
            if typeComponent in typeDict:
                htmlString += '<dd>-&nbsp' + typeDict[typeComponent] + '</dd>'
            else:
                htmlString += '<dd>-&nbspOther</dd>'
    if len(cd.roles) != 0:
        htmlString += '<dt><u>Role(s)</u>:</dt>'
        for role in cd.roles:
            if role in roleDict:
                htmlString += '<dd>-&nbsp' + roleDict[role] + '</dd>'
            else:
                htmlString += '<dd>-&nbspOther</dd>'
    if len(cd.components) != 0:
        htmlString += '<dt><u>Sub-Components</u>:</dt>'
        for component in cd.components:
            if parentName is not None:
                htmlString += '<dd>-&nbsp' + component.name.replace(parentName + '_', '') + '</dd>' # noqa
            else:
                htmlString += '<dd>-&nbsp' + component.name + '</dd>'

    return htmlString


def createAccordionWidget(components, parentName=None):
    accordion = widgets.Accordion()
    accordionChildren = []

    for index, cd in enumerate(components):
        htmlWidget = widgets.HTML()
        accordionChildren.append(htmlWidget)

        if parentName is None:
            accordion.set_title(index, cd.displayId)
        else:
            accordion.set_title(index, cd.displayId.replace(parentName + '_', '')) # noqa
        htmlString = createHTMLString(cd, parentName)

        htmlWidget.value = '<d1>' + htmlString + '</d1>'

    accordion.children = accordionChildren

    return accordion


def createDisplayWidgetList(doc, originalCDs, addedCDs, cdDictionary):
    boxChildren = []

    for i, cd in enumerate(originalCDs):
        boxChildren.append(widgets.HTML('<font size=3><b>' + cd.displayId + '</b></font>')) # noqa
        name = cd.displayId
        subComponents = cdDictionary[name].copy()
        subComponents.insert(0, cd)

        accordion = createAccordionWidget(subComponents, name)

        boxChildren.append(accordion)
        boxChildren.append(widgets.HTML('<br>'))

    if len(addedCDs) != 0:
        boxChildren.append(widgets.HTML('<font size=3><b>Added Components</b></font>')) # noqa
        accordion = createAccordionWidget(addedCDs)
        accordion.selected_index = None
        boxChildren.append(accordion)

    return boxChildren


def fixAndCreateWidgets(doc, originalCDs, addedCDs, cdDictionary):
    fixCDNames(doc)
    extractSeqAnnotations(doc, cdDictionary)

    return createDisplayWidgetList(doc, originalCDs, addedCDs, cdDictionary)
