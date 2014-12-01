"""Definition of the AddCard content type
"""

from zope.interface import implements
from Products.Archetypes.Field import ComputedField
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
import datetime
from Products.ATVocabularyManager import NamedVocabulary

# -*- Message Factory Imported Here -*-
from uwosh.addcard import addcardMessageFactory as _

from uwosh.addcard.interfaces import IAddCard
from uwosh.addcard.config import PROJECTNAME
from Products.CMFCore.utils import getToolByName
import xmlrpclib
import socket
from Products.Archetypes.utils import DisplayList
from Products.PlonePAS.interfaces import group as igroup

webServiceBaseURL = 'http://ws.it.uwosh.edu:8081/ws'
webService = xmlrpclib.Server(webServiceBaseURL, allow_none=1)

AddCardSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    ComputedField('title',
        searchable=1,
        expression='context._computeTitle()',
        accessor='Title',
    ),

    atapi.StringField(
        'studentemail',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Your (the student's) UW Oshkosh email address"),
            description=_(u""),
        ),
        default_method="setDefaultEmail",
        required=True,
        validators=('isEmail'),
    ),
                                                                             
    atapi.StringField(
        'fullname',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Your full name"),
            description=_(u""),
        ),
        default_method="setDefaultFullName",
        required=True,
    ),
                                                                             
    ComputedField('studentemplid',
        searchable=0,
        expression='context._computeStudentEmplid()',
        accessor='getStudentemplid',
    ),

    atapi.StringField(
        'psterm',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Academic term"),
            description=_(u"Please select the academic term for the class you would like to add"),
        ),
        vocabulary=NamedVocabulary("PSSemesters"),
        # vocabulary="getPSSemesters",
        default_method="setDefaultPsterm",
        required=True,
   ),

    atapi.StringField(
        'creditaudit',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label=_(u"Credit or Audit"),
            description=_(u"Please select if the added class will be for Credit or Audit"),
        ),
        vocabulary=("Credit", "Audit",),
        required=True,
        default="Credit"
   ),

    atapi.StringField(
        'subject1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.SelectionWidget(
            label='Subject 1',
            description=_(u"Please choose the subject for the class you are adding, e.g. HISTORY"),
        ),
        required=1,
        vocabulary=NamedVocabulary("PSSubjects"),
        searchable=True,
        ),
        
                                                                                                                                                              
    atapi.StringField(
        'catalognumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Catalog Number 1',
            description=_(u"Please select the catalog number for the class you are adding, e.g. 101"),
        ),
        required=1,
        searchable=True,
    ),       

    atapi.StringField(
        'sectionnumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label='Section Number 1',
            description=_(u"Please select the section number for the class you are adding, e.g. 001"),
        ),
        required=1,
        searchable=True,
    ),      
    
    atapi.StringField(
        'classnumber1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Class Number 1"),
            description=_(u"This is the five (5) digit class number for the class you are adding, e.g. 50123, and is for your information only"),
        ),
        required=1,
    ),
                                                                                                                                                             
    atapi.StringField(
        'instructorID1',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Instructor 1's ID"),
            description=_(u"This is the user ID of the instructor for the class you are adding, and is for your information only"),
        ),
        required=True,
        searchable=True,
    ),

    atapi.StringField(
        'comments',
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Explanation"),
            description=_(u"Please explain why you need to add this class"),
        ),
        required=True,
    ),

     atapi.StringField(
        'legallabel',
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u"ATTENTION STUDENT"),
            description=_(u"By checking the box on the left, I (Student) agree to pay all costs associated with my enrollment at the University.  Furthermore, I agree to pay all collection expenses, including reasonable attorney's fees, which the University may incur if I do not fulfill my payment obligations.  Time Conflict Cards are not official until they are processed by the Registrar's Office."),
        ),
        required=True,
    ),

    atapi.StringField(
        'studentsignature',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Student Signature"),
            description=_(u"Signature of the Instructor or Department authorizing the drop."),
        ),
        searchable=True,
    ),   

    atapi.StringField(
        'studentsigndate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Date of Instructor/Department Signature"),
            description=_(u"The date the student signed the add card."),
        ),
        searchable=True,
    ),

    atapi.StringField(
        'insturctorsignature',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Instructor/Department Signature"),
            description=_(u"Signature approves consent, class limit, and requisites unless otherwise noted in comments section."),
        ),
        searchable=True,
    ),   

    atapi.StringField(
        'instructorsigndate',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Date of Instructor/Department Signature"),
            description=_(u"The date the instructor or department signed the add card."),
        ),
        searchable=True,
    ),   



))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

AddCardSchema['title'].storage = atapi.AnnotationStorage()
AddCardSchema['title'].required = 0
AddCardSchema['title'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

AddCardSchema['description'].storage = atapi.AnnotationStorage()
AddCardSchema['description'].widget.visible = {'edit': 'hidden', 'view': 'invisible'}

schemata.finalizeATCTSchema(AddCardSchema, moveDiscussion=False)


class AddCard(base.ATCTContent):
    """Implementation of the Add Card"""
    implements(IAddCard)

    meta_type = "AddCard"
    schema = AddCardSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    def setDefaultEmail(self):
        pm = getToolByName(self, "portal_membership", None)
        if pm:
            member = pm.getAuthenticatedMember()
            if member:
                return member.getProperty('email')


    def setDefaultFullName(self):
        pm = getToolByName(self, "portal_membership", None)
        if pm:
            member = pm.getAuthenticatedMember()
            if member:
                return member.getProperty('fullname')         


    def setDefaultPsterm(self):
        # psterm = ""
        # try:
        #     psterm = webService.getCurrentOrNextSemesterCX(WEBSERVICETESTMODE)
        # except Exception, e:
        #     pass
        psterm = webService.getCurrentOrNextSemesterCX()
        return psterm
    

    # def getPSSemesters(self):
    #     threesems = webService.getThreeSemestersCX(WEBSERVICETESTMODE)
    #     threesemstuple =xmlrpclib.loads(threesems)
    #     dl = DisplayList([(x, y) for x, y in threesemstuple])
    #     import pdb; pdb.set_trace( )
    #     return threesemstuple


    def getPsterm(self):
        vocab = NamedVocabulary("PSSemesters")
        try:
            displayval = vocab.getVocabularyDict(self)[self.psterm]
        except KeyError, e:
            retstr = ""
        else:
            retstr = "%s (%s)" % (displayval, self.psterm)
        return retstr


    def getRawPsterm(self):
        return self.psterm


    def _huntUserFolder(self, member_id, context):
        """Find userfolder containing user in the hierarchy
           starting from context
        """
        uf = context.acl_users
        while uf is not None:
            user = uf.getUserById(member_id)
            if user is not None:
                return uf
            container = aq_parent(aq_inner(uf))
            parent = aq_parent(aq_inner(container))
            uf = getattr(parent, 'acl_users', None)
        return None


    def _huntUser(self, member_id, context):
        """Find user in the hierarchy of userfolders
           starting from context
        """
        uf = self._huntUserFolder(member_id, context)
        if uf is not None:
            return uf.getUserById(member_id)


    def getMemberEmail(self, id):
        """ Need this because portal_membership.getMemberById() is for Manager role only.
            This code is based on getMemberById but doesn't use wrapUser().
        """
        user = self._huntUser(id, self)
        if user is not None:
            email = user.getProperty('email', None)
            return email
        # otherwise just return the userid with a domain name appended
        # return id + '@uwosh.edu'


    def getRegistrarGroupMemberEmails(self):
        """ Need this because portal_groups.getGroupMembers() is protected.
        """
        return [self.getMemberEmail(m) for m in self.getGroupMembers('Registrar')]


    def getGroupMembers(self, group_id):
        members = set()
        introspectors = self._getGroupIntrospectors()
        for iid, introspector in introspectors:
            members.update(introspector.getGroupMembers(group_id))
        return list(members)


    def _getGroupIntrospectors(self):
        return self._getPlugins().listPlugins(
            igroup.IGroupIntrospection
            )


    def _getPlugins(self):
        return self.acl_users.plugins


    def _computeTitle(obj):
        """Get object's title."""
        title = " ".join([obj.fullname or '?', obj.psterm or '?', obj.classnumber1 or '?',])
        return title


    def _computeStudentEmplid(obj):
        """Get student's emplid via web service"""
        # emplid = ''
        # try:
        #     emplid = webService.getEmplidFromEmailAddressCX(obj.studentemail, WEBSERVICETESTMODE)
        # except xmlrpclib.ResponseError, e:
        #     pass
        # except socket.error, e:
        #     pass
        emplid = webService.getEmplidFromEmailAddressCX(obj.studentemail)
        return emplid

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    comments = atapi.ATFieldProperty('comments')

    fullname = atapi.ATFieldProperty('fullname')

    studentemail = atapi.ATFieldProperty('studentemail')

    instructorID1 = atapi.ATFieldProperty('instructorID1')

    psterm = atapi.ATFieldProperty('psterm')

    classnumber1= atapi.ATFieldProperty('classnumber1')

    sectionnumber1 = atapi.ATFieldProperty('sectionnumber1')

    catalognumber1 = atapi.ATFieldProperty('catalognumber1')

    subject1 = atapi.ATFieldProperty('subject1')

    creditaudit = atapi.ATFieldProperty('creditaudit')

def objectSetTitle(obj, event):
    title = " ".join([obj.fullname or '?', obj.psterm or '?', obj.classnumber1 or '?',])
    if obj.Title() != title:
        obj.Title(title)
        obj.reindexObject()


def objectInitialized(obj, event):
    objectSetTitle(obj, event)
   

def objectEdited(obj, event):
    objectSetTitle(obj, event)

atapi.registerType(AddCard, PROJECTNAME)
