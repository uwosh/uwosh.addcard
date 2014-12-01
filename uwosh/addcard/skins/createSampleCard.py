## Script (Python) "createAddCard"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=testmode=0
##title=
if testmode=='1':
      context.Members.nguyen.invokeFactory('AddCard', 'card')
      card=context.Members.nguyen.card
      card.setTitle('T. Kim Nguyen 0665 13425 13010')
      card.edit(studentemail='nguyen@uwosh.edu', 
      fullname='T. Kim Nguyen',
      psterm='0665',
      subject1='COMPUTER SCIENCE', 
      catalognumber1=' 101',
      sectionnumber1='001C', 
      classnumber1='44444',
      instructorID1='nguyen',
      comments='I need this class'
      )
