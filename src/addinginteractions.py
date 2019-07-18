from sbol import * # noqa
import ipywidgets as widgets


typesInteractions = ['Inhibition', 'Stimulation', 'Biochemical Reaction',
                     'Non-Covalent Binding', 'Degradation', 'Genetic Production', # noqa
                     'Control']
mapInteractions = {'Inhibition': 'http://identifiers.org/biomodels.sbo/SBO:0000169', # noqa
                   'Stimulation': 'http://identifiers.org/biomodels.sbo/SBO:0000170', # noqa
                   'Biochemical Reaction': 'http://identifiers.org/biomodels.sbo/SBO:0000176', # noqa
                   'Non-Covalent Binding': 'http://identifiers.org/biomodels.sbo/SBO:0000177', # noqa
                   'Degradation': 'http://identifiers.org/biomodels.sbo/SBO:0000179', # noqa
                   'Genetic Production': 'http://identifiers.org/biomodels.sbo/SBO:0000589', # noqa
                   'Control': 'http://identifiers.org/biomodels.sbo/SBO:0000168'} # noqa

typesParticipants = ['Inhibitor', 'Inhibited', 'Stimulator', 'Stimulated', 'Reactant', # noqa
                     'Product', 'Promoter', 'Modifier', 'Modified', 'Template']
mapParticipants = {'Inhibitor': 'http://identifiers.org/biomodels.sbo/SBO:0000020', # noqa
                   'Inhibited': 'http://identifiers.org/biomodels.sbo/SBO:0000642', # noqa
                   'Stimulator': 'http://identifiers.org/biomodels.sbo/SBO:0000459', # noqa
                   'Stimulated': 'http://identifiers.org/biomodels.sbo/SBO:0000643', # noqa
                   'Reactant': 'http://identifiers.org/biomodels.sbo/SBO:0000010', # noqa
                   'Product': 'http://identifiers.org/biomodels.sbo/SBO:0000011', # noqa
                   'Promoter': 'http://identifiers.org/biomodels.sbo/SBO:0000598', # noqa
                   'Modifier': 'http://identifiers.org/biomodels.sbo/SBO:0000019', # noqa
                   'Modified': 'http://identifiers.org/biomodels.sbo/SBO:0000644', # noqa
                   'Template': 'http://identifiers.org/biomodels.sbo/SBO:0000645'} # noqa


def findPlasmid(fc, fcDictionary):
    plasmidName = ''

    if fc.displayId not in fcDictionary:
        return None

    if fcDictionary[fc.displayId] is None:
        return None

    name = fcDictionary[fc.displayId]

    if name != fc.displayId:
        plasmidName = fc.displayId.replace(name, '')[:-1]
    else:
        plasmidName = 'Other'

    return plasmidName


def createHBoxChildren(moduleName, customNameDictionary, fcDictionary):
    module = customNameDictionary[moduleName]

    selectWidgetDictionary = {}

    for fc in module.functionalComponents:
        plasmid = findPlasmid(fc, fcDictionary)

        if plasmid is None:
            continue

        name = fcDictionary[fc.displayId]

        if plasmid not in selectWidgetDictionary:
            selectWidgetDictionary[plasmid] = []

        selectWidgetDictionary[plasmid].append(name)

    hboxChildren = []

    for plasmid in selectWidgetDictionary.keys():
        nameList = []

        for component in selectWidgetDictionary[plasmid]:
            nameList.append(component)

        selectWidget = widgets.SelectMultiple(
            options=nameList,
            description=plasmid,
            rows=len(nameList),
            style={'description_width': '125px'},
            layout=widgets.Layout(width='325px')
        )

        hboxChildren.append(selectWidget)

    return hboxChildren


participantDictionary = {}  # fc display id : participation


def createParticipationChildren(hBoxChildren):
    selectedFC = []
    participationChildren = []
    for widget in hBoxChildren:
        if len(widget.value) != 0:
            participationChildren.append(widgets.HTML('<b>' +
                                                      widget.description +
                                                      '</b>'))
        for selected in widget.value:
            dropdown = widgets.Dropdown(
                            options=typesParticipants,
                            description=selected,
                            value=None,
                            style={'description_width': '150px'},
                            layout=widgets.Layout(width='325px'))
            participationChildren.append(dropdown)

            if widget.description != 'Other':
                selectedFC.append(widget.description + '_' + selected)
            else:
                selectedFC.append(selected)

        participationChildren.append(widgets.HTML('<br>'))

    return (participationChildren, selectedFC)


def createInteraction(customNameDictionary,
                      moduleName,
                      interactionName,
                      interactionType,
                      participantDictionary,
                      selectedFC):
    module = customNameDictionary[moduleName]
    try:
        interaction = module.interactions.create(interactionName)
        interaction.types = mapInteractions[interactionType]
    except: # noqa
        raise Exception(str(interactionName.value + ' already exists!'))

    for fc in module.functionalComponents:
        if fc.displayId in selectedFC:
            participation = interaction.participations.create(fc.displayId)
            participation.participant = fc.identity

            participantDictionary[fc.displayId] = participation


def createMapsTos(doc,
                  participationWidgetsChildren,
                  participantDictionary,
                  plasmidPartDictionary,
                  addedPlasmidParts):
    plasmid = ''
    for widget in participationWidgetsChildren:
        if widget.value != '<br>':
            if '<b>' in widget.value:
                plasmid = widget.value.replace('<b>', '').replace('</b>', '')
            else:
                if plasmid != 'Other':
                    fcName = plasmid + '_' + widget.description
                else:
                    fcName = widget.description

                participantDictionary[fcName].roles = mapParticipants[widget.value] # noqa

                fc = doc.find(participantDictionary[fcName].participant).cast(FunctionalComponent) # noqa

                if fcName not in addedPlasmidParts:
                    continue

                mapsto = addedPlasmidParts[fcName].mapsTos.create(fc.displayId)
                mapsto.refinement = SBOL_REFINEMENT_USE_LOCAL # noqa
                mapsto.local = fc.identity
                mapsto.remote = plasmidPartDictionary[fcName].identity
