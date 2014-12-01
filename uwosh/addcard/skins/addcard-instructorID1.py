if hasattr(context, 'portal_type') and context.portal_type == 'AddCard' and hasattr(context, 'instructorID1'):
  return context.getInstructorID1()
else:
  return None
