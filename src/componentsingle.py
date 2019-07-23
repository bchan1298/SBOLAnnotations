from sbol import * # noqa


componentTypes = ['DNA', 'RNA', 'Protein', 'Small Molecule', 'Complex']

componentRoles = ['', 'Miscellaneous', 'Promoter', 'RBS', 'CDS', 'Terminator',
                  'Gene', 'Operator', 'Engineered Gene', 'mRNA', 'Effector']

typesMap = {'DNA': 'http://www.biopax.org/release/biopax-level3.owl#DnaRegion',
            'RNA': 'http://www.biopax.org/release/biopax-level3.owl#RnaRegion',
            'Protein': 'http://www.biopax.org/release/biopax-level3.owl#Protein', # noqa
            'Small Molecule': 'http://www.biopax.org/release/biopax-level3.owl#SmallMolecule', # noqa
            'Complex': 'http://www.biopax.org/release/biopax-level3.owl#Complex'} # noqa

rolesMap = {'Miscellaneous': 'http://identifiers.org/so/SO:0000001',
            'Promoter': 'http://identifiers.org/so/SO:0000167',
            'RBS': 'http://identifiers.org/so/SO:0000139',
            'CDS': 'http://identifiers.org/so/SO:0000316',
            'Terminator': 'http://identifiers.org/so/SO:0000141',
            'Gene': 'http://identifiers.org/so/SO:0000704',
            'Operator': 'http://identifiers.org/so/SO:0000057',
            'Engineered Gene': 'http://identifiers.org/so/SO:0000280',
            'mRNA': 'http://identifiers.org/so/SO:0000234',
            'Effector': 'http://identifiers.org/chebi/CHEBI:35224',
            'Transcription Factor': 'http://identifiers.org/go/GO:0003700'}


def addComponent(doc, addedCDs, componentName, componentType, componentRole):
    try:
        newComponentDefinition = ComponentDefinition(componentName, typesMap[componentType]) # noqa
        newComponentDefinition.name = componentName
        if componentRole != '':
            newComponentDefinition.roles = rolesMap[componentRole]
    except Exception as e:
        print(e)
        return

    try:
        doc.addComponentDefinition(newComponentDefinition)
        addedCDs.append(newComponentDefinition)
        print('Component created!')
    except RuntimeError:
        print('Component name already exists.')
