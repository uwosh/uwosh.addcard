import logging
logger = logging.getLogger('uwosh.addcard: setuphandlers')

import os
# import transaction

# from config import product_globals
# from Globals import package_home
# from Products.Archetypes import types_globals
# from App.Common import package_home

from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
# from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

# from plone.app.kss import content_replacer

# from Products.UWOshAddCard.config import PROJECTNAME
# from Products.UWOshAddCard.config import DEPENDENCIES


def isNotUWOshAddCardProfile(context):
    return context.readDataFile("UWOshAddCard_marker.txt") is None


def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    if isNotUWOshAddCardProfile(context):
        return
    site = context.getSite()
    # Create vocabularies in vocabulary lib
    atvm = getToolByName(site, ATVOCABULARYTOOL)
    vocabmap = {
        'PSSemesters' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
        'PSSubjects' : ('SimpleVocabulary', 'SimpleVocabularyTerm'),
    }

    for vocabname in vocabmap.keys():
        if vocabname in atvm.contentIds():
            atvm.manage_delObjects(vocabname)
        atvm.invokeFactory(vocabmap[vocabname][0], vocabname)

        if len(atvm[vocabname].contentIds()) < 1:
            if vocabmap[vocabname][0] == 'SimpleVocabulary':
                # csvpath = os.path.join(package_home(types_globals), 'data', '%s.csv' % vocabname)
                # import pdb; pdb.set_trace()
                csvpath = os.path.join(os.path.dirname(__file__), 'data', '%s.csv' % vocabname)

                if not (os.path.exists(csvpath) and os.path.isfile(csvpath)):
                    logger.warn('No csv import file provided at %s.' % csvpath)
                    continue
                try:
                    f = open(csvpath, 'r')
                    data = f.read()
                    f.close()
                except:
                    logger.warn("Problems while reading csv import file provided at %s." % csvpath)
                    continue
                atvm[vocabname].importCSV(data)


def createRegistrarGroup(context):
    """ creates a group with ID 'Registrar' if necessary """
    if isNotUWOshAddCardProfile(context):
        return
    site = context.getSite()
    pg = getToolByName(site, 'portal_groups')
    if not pg.getGroupById('Registrar'):
        g = pg.addGroup('Registrar', ['Registrar'], [],
                    {
                    # 'email': 'registrar@uwosh.edu',
                     'title': 'Registrar'
                     })
        g = pg.getGroupById('Registrar')
        g.addMember('jaekes')
        g.addMember('schettle')
        g.addMember('nguyen')
        g.addMember('hrenj')
        # except Exception, e:
        #     pass



def install(context):
    """ set up collections, publish content, set titles, etc. """
    if isNotUWOshAddCardProfile(context):
        return
    site = context.getSite()

    # hide stuff from nav
    site['news'].setExcludeFromNav(True)
    site['news'].reindexObject()

    site['events'].setExcludeFromNav(True)
    site['events'].reindexObject()
    
    site['Members'].setExcludeFromNav(True)
    site['Members'].reindexObject()

    # enable home folders
    site.portal_membership.setMemberareaCreationFlag()

    # publish default content
    site['application-states-and-workflow'].content_status_modify(workflow_action='publish')
    site['welcome'].content_status_modify(workflow_action='publish')
    site.setDefaultPage('welcome')

    # set up collections
    pt = getToolByName(site, 'portal_atct')
    if pt:
        pt.addIndex('addcard-instructorID1', enabled=True, criteria=('ATCurrentAuthorCriterion',))

        reports = site.reports
        reports.setDescription('all reports show most recently modified items first')
        reports.reindexObject()
        reports.content_status_modify(workflow_action='publish')

        r = reports['all-add-card']
        r.setTitle('All Add Card')
        r.reindexObject()
        crit = r.addCriterion('portal_type', 'ATSimpleStringCriterion')
        crit.setValue('AddCard')
        r.setSortCriterion('modified', True)
        r.content_status_modify(workflow_action='publish')
        
        studentreports = reports['for-students']
        studentreports.setTitle('For Students')
        studentreports.content_status_modify(workflow_action='publish')
        studentreports.reindexObject()

        for i in ('student-my-add-card', 'student-my-add-card-needing-a-response', 'student-my-cards-waiting-for-approval', 'student-my-add-card-awaiting-registrar-processing', 'student-my-add-card-completed', 'student-my-add-card-denied', 'student-my-add-card-archived',):
            r = studentreports[i]
            crit = r.addCriterion('portal_type', 'ATSimpleStringCriterion')
            crit.setValue('AddCard')
            r.setSortCriterion('modified', True)
            crit2 = r.addCriterion('Creator', 'ATCurrentAuthorCriterion')
            r.content_status_modify(workflow_action='publish')

        r = studentreports['student-my-add-card']
        r.setTitle('Student: All My Add Cards')
        r.reindexObject()
        
        r = studentreports['student-my-add-card-needing-a-response']
        r.setTitle('Student: My Add Card Needing a Response')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['instructor1waitingforstudentresponse',])

        r = studentreports['student-my-cards-waiting-for-approval']
        r.setTitle('Student: My Add Card Waiting for Instructor Approval')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['needinstructor1approval',])

        r = studentreports['student-my-add-card-awaiting-registrar-processing']
        r.setTitle('Student: My Add Card Waiting for Registrar to Process')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['registrarprocessing',])

        r = studentreports['student-my-add-card-completed']
        r.setTitle('Student: My Add Card That Have Been Processed')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['completed',])

        r = studentreports['student-my-add-card-denied']
        r.setTitle('Student: My Add Card That Have Been Denied')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['studenthasbeeninformedenrollmentdenied',])

        r = studentreports['student-my-add-card-archived']
        r.setTitle('Student: My Add Card that have been Archived')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['archived',])

        instructorreports = reports['for-instructors']
        instructorreports.setTitle('For Instructors')
        instructorreports.reindexObject()
        instructorreports.content_status_modify(workflow_action='publish')

        for i in ('instructors-add-card-awaiting-my-approval-as-instructor1', 'instructors-add-card-i-have-approved-as-instructor1',):
            r = instructorreports[i]
            crit = r.addCriterion('portal_type', 'ATSimpleStringCriterion')
            crit.setValue('AddCard')
            r.setSortCriterion('modified', True)
            r.content_status_modify(workflow_action='publish')

        r = instructorreports['instructors-add-card-awaiting-my-approval-as-instructor1']
        r.setTitle('Instructors: Add Card Awaiting my Approval as Instructor 1')
        r.reindexObject()
        crit = r.addCriterion('addcard-instructorID1', 'ATCurrentAuthorCriterion')
        crit2 = r.addCriterion('review_state', 'ATListCriterion')
        crit2.setValue(['needinstructor1approval',])

        r = instructorreports['instructors-add-card-i-have-approved-as-instructor1']
        r.setTitle('Instructors: Add Card I Have Approved as Instructor 1')
        r.reindexObject()
        crit = r.addCriterion('addcard-instructorID1', 'ATCurrentAuthorCriterion')
        crit2 = r.addCriterion('review_state', 'ATListCriterion')
        crit2.setValue(['registrarprocessing', 'completed', 'archived', ])

        registrarreports = reports['for-registrar']
        registrarreports.setTitle('For Registrar')
        registrarreports.reindexObject()
        registrarreports.content_status_modify(workflow_action='publish')

        for i in ('registrar-add-card-awaiting-processing', 'registrar-add-card-to-archive', 'registrar-archived-add-card', 'registrar-add-card-late-needinstructorapproval', 'registrar-add-card-late-instructorwaitingforstudentresponse', 'registrar-add-card-late-registrarprocessing', ):
            r = registrarreports[i]
            crit = r.addCriterion('portal_type', 'ATSimpleStringCriterion')
            crit.setValue('AddCard')
            r.setSortCriterion('modified', True)
            r.content_status_modify(workflow_action='publish')

        r = registrarreports['registrar-add-card-awaiting-processing']
        r.setTitle('Registrar: Add Card Awaiting Processing')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['registrarprocessing', ])

        r = registrarreports['registrar-add-card-to-archive']
        r.setTitle('Registrar: Add Card to Archive')
        r.setDescription('cards that are "completed" and were last modified more than 3 months ago')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['completed', ])
        # add relative date criterion here: 30 days old
        date_crit = r.addCriterion('modified', 'ATFriendlyDateCriteria')
        date_crit.setValue(30) # 1 month
        date_crit.setDateRange('+') 
        date_crit.setOperation('more')

        r = registrarreports['registrar-archived-add-card']
        r.setTitle('Registrar: Archived Add Card')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['archived', ])

        r = registrarreports['registrar-add-card-late-needinstructorapproval']
        r.setTitle('Registrar: Add Card that are LATE (waiting for instructor)')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['needinstructor1approval',])
        # add relative date criterion here: 1 day old
        date_crit = r.addCriterion('modified', 'ATFriendlyDateCriteria')
        date_crit.setValue(1)
        date_crit.setDateRange('+') 
        date_crit.setOperation('more')

        r = registrarreports['registrar-add-card-late-instructorwaitingforstudentresponse']
        r.setTitle('Registrar: Add Card that are LATE (waiting for student to respond to instructor)')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['instructor1waitingforstudentresponse',])
        # add relative date criterion here: 1 day old
        date_crit = r.addCriterion('modified', 'ATFriendlyDateCriteria')
        date_crit.setValue(1)
        date_crit.setDateRange('+') 
        date_crit.setOperation('more')

        r = registrarreports['registrar-add-card-late-registrarprocessing']
        r.setTitle('Registrar: Add Card that are LATE (waiting to be processed)')
        r.reindexObject()
        crit = r.addCriterion('review_state', 'ATListCriterion')
        crit.setValue(['registrarprocessing', ])
        # add relative date criterion here: 1 day old
        date_crit = r.addCriterion('modified', 'ATFriendlyDateCriteria')
        date_crit.setValue(1)
        date_crit.setDateRange('+') 
        date_crit.setOperation('more')

