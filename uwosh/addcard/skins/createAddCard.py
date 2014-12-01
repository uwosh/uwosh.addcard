## Script (Python) "createAddCard"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
request = container.REQUEST
response =  request.response

pm=context.portal_membership
member = pm.getAuthenticatedMember()
if member == 'Anonymous User':
    return "You must be logged in to do this"

homeFolder = pm.getHomeFolder()
theTime = str(int(context.ZopeTime()))
appId = 'addcard_' + member.getId() + theTime
homeFolder.invokeFactory("AddCard", appId)
msg = "A new add card has been created for you.  You may now fill in the details by clicking on the purple 'Edit request' button below." 

context.plone_utils.addPortalMessage(msg)
#state.setNextAction('redirect_to:string:%s'%homeFolder.absolute_url())
response.redirect("%s/%s?portal_status_message=%s" % (homeFolder.absolute_url(), appId, msg))
#return state
