from sbol import * # noqa
import ipywidgets as widgets


moduleNames = ['Device-Test-Context', 'Device-Test', 'Device']

typesInteractions = ['Inhibition', 'Stimulation', 'Biochemical Reaction',
                     'Non-Covalent Binding', 'Degradation',
                     'Genetic Production', 'Control']
interactionMap = {'http://identifiers.org/biomodels.sbo/SBO:0000169': 'Inhibition', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000170': 'Stimulation', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000176': 'Biochemical Reaction', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000177': 'Non-Covalent Binding', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000179': 'Degradation', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000589': 'Genetic Production', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000168': 'Control'} # noqa

typesParticipants = ['Inhibitor', 'Inhibited', 'Stimulator', 'Stimulated',
                     'Reactant', 'Product', 'Promoter', 'Modifier', 'Modified',
                     'Template']

participantMap = {'http://identifiers.org/biomodels.sbo/SBO:0000020': 'Inhibitor', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000642': 'Inhibited', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000459': 'Stimulator', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000643': 'Stimulated', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000010': 'Reactant', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000011': 'Product', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000598': 'Promoter', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000019': 'Modifier', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000644': 'Modified', # noqa
                  'http://identifiers.org/biomodels.sbo/SBO:0000645': 'Template'} # noqa


def createInteractionAccordion(module):
    interactionWidget = widgets.Accordion()
    interactionList = []

    for i, inter in enumerate(module.interactions):
        htmlInteraction = ''
        htmlInteraction += '<dt><u>Interaction Type(s)</u>:</dt>'
        for typeI in inter.types:
            if typeI not in interactionMap:
                htmlInteraction += '<dd>This one isn\'t right.</dd>'
            else:
                htmlInteraction += '<dd>' + interactionMap[typeI] + '</dd>'

        htmlInteraction += '<dt><u>Participants</u>:</dt>'
        for participation in inter.participations:
            htmlInteraction += '<dd>-&nbsp' + participation.displayId
            for role in participation.roles:
                htmlInteraction += str('&nbsp(' + participantMap[role] + ')')
            htmlInteraction += '</dd>'

        interactionList.append(widgets.HTML(htmlInteraction))
        interactionWidget.children = interactionList

        interactionWidget.set_title(i, inter.displayId)

    interactionWidget.selected_index = None

    return interactionWidget


def createSingleAccordion(module, moduleName):
    accordionWidgets = []

    htmlString = ''
    htmlString += '<b><h5>(' + moduleName + ')</h5></b>'
    if len(module.modules) != 0:
        htmlString += '<u><dt>Modules</dt></u>'
        for m in module.modules:
            htmlString += str('<dd>-&nbsp' +
                              str(m.displayId if m.name is None else m.name) +
                              '</dd>')
    if len(module.functionalComponents) != 0:
        htmlString += '<u><dt>Functional&nbspComponents</dt></u>'
        for fc in module.functionalComponents:
            if '__' not in fc.displayId:
                htmlString += '<dd>-&nbsp' + fc.displayId

    interactionWidget = None
    if len(module.interactions) != 0:
        interactionWidget = createInteractionAccordion(module)
        htmlString += '<br><br><b><u>Interactions</u></b>'

    accordionWidgets.append(widgets.HTML(htmlString))

    if interactionWidget is not None:
        accordionWidgets.append(interactionWidget)

    return accordionWidgets


def createAccordionWidgets(vBoxChildren, modules):
    for index, module in enumerate(modules):
        accordionWidgets = createSingleAccordion(module, moduleNames[index])
        vBoxChildren[index].children = accordionWidgets


def createParentAccordion(modules, modulesDictionary):
    accordion = widgets.Accordion()
    children = [widgets.VBox(), widgets.VBox(), widgets.VBox()]

    createAccordionWidgets(children, modules)

    accordion.children = children

    accordion.set_title(0, modulesDictionary['Device-Test-Context'].name if modulesDictionary['Device-Test-Context'].name is not None else 'Device-Test-Context') # noqa
    accordion.set_title(1, modulesDictionary['Device-Test'].name if modulesDictionary['Device-Test'].name is not None else 'Device-Test') # noqa
    accordion.set_title(2, modulesDictionary['Device'].name if modulesDictionary['Device'].name is not None else 'Device') # noqa

    return accordion
