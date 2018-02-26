import uno
import config_init
configuration = config_init.config_init


def get_sheets_from_ods():
    """Перед вызовом этой функции убедитесь, что либреоффис запущен с параметрами:
     soffice.exe -accept=socket,host=0,port=2002;urp;
     - это позволит ему принимать соединения от скрипта с локальной машины """
    # get the uno component context from the PyUNO runtime
    localContext = uno.getComponentContext()

    # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext)

    # connect to the running office
    ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    smgr = ctx.ServiceManager

    # get the central desktop object
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)

    components = desktop.getComponents()
    e = components.createEnumeration()
    while e.hasMoreElements():
        component = e.nextElement()
        if configuration.get("sheet_service") in component.getSupportedServiceNames():
            if component.URL == configuration.get("ods_url"):
                return component
    return desktop.loadComponentFromURL(configuration.get("ods_url"), "_blank", 0, ())



