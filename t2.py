import uno
#import populate_profit_sheet

# get the uno component context from the PyUNO runtime
localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)

# connect to the running office
ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
smgr = ctx.ServiceManager

# get the central desktop object
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
# access the current writer document
# document=desktop.loadComponentFromURL("file:///f:/dev/evedev/libreOfficeDocs/test1.ods","_blank",0,())
#model = desktop.getCurrentComponent()

#dir(model)

# buy_orders=document.getSheets().getByName("buyOrders")

x=3

x=+1