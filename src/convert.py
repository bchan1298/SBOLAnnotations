from sbol import * # noqa
import requests


def getSBOLFiles(doc, originalCDs, cdDict, uploadDict, uriPrefix, version):
    files = []
    for key in uploadDict.keys():
        if key[-3:] == '.gb':
            file = open(key, 'w+')
            file.write(uploadDict[key]['content'].decode('utf-8'))
            file.close()

            files.append(key)

    for gbFileName in files:
        gbFile = open(gbFileName).read()
        request = {'options': {'language': 'SBOL2',
                               'test_equality': False,
                               'check_uri_compliance': False,
                               'check_completeness': False,
                               'check_best_practices': False,
                               'fail_on_first_error': False,
                               'provide_detailed_stack_trace': False,
                               'subset_uri': '',
                               'uri_prefix': uriPrefix,
                               'version': '1' if version == '' else version,
                               'insert_type': False,
                               'main_file_name': 'main file',
                               'diff_file_name': 'comparison file',
                               },
                   'return_file': True,
                   'main_file': gbFile
                   }

        response = requests.post("http://www.async.ece.utah.edu/validate/",
                                 json=request)
        xmlResponse = response.json()['result']

        sbolFile = open(gbFileName[:-3] + '.xml', 'w+')
        sbolFile.write(xmlResponse)
        sbolFile.close()

        fileNameSBOL = gbFileName[:-3] + '.xml'
        doc.append(fileNameSBOL)

        for cd in doc.componentDefinitions:
            exists = False
            for i in originalCDs:
                if i.displayId == cd.displayId:
                    exists = True
            if exists is False:
                originalCDs.append(cd)
                cdDict[cd.displayId] = []
