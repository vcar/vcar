import shutil
#import xmlrpc #py3
import xmlrpclib #py2
#from xmlrpc.client import ServerProxy
from xmlrpclib import ServerProxy


# SIGSTOP & SIGCONT for suspeding & resuming plugins
# Remove a all plugins/ user plugins/ plugin
#

class PluginManager(object):

    def __init__(self):
        """Initialize it"""
        self.status = None
        self.error = None
        #self.server = xmlrpc.client.ServerProxy('http://localhost:9001/RPC2')
        self.server = xmlrpclib.ServerProxy('http://localhost:9001/RPC2')

    # Plugin Manager Methods --------------------------------------------------

    def getState(self):
        """Return the plugin manager state as struct
                        #statecode 	statename 	Description
                        2 			FATAL 		PM has experienced a serious error.
                        1 			RUNNING 	PM is working normally.
                        0 			RESTARTING 	PM is in the process of restarting.
                        -1 			SHUTDOWN 	PM is in the process of shutting down.
        """
        return self.server.supervisor.getState()

    def shutdown(self):
        """Shut down the Plugin Manager process.
                @return boolean result always returns True unless error
        """
        return self.server.supervisor.shutdown()

    def restart(self):
        """Restart the Plugin Manager process.
                @return boolean result always return True unless error
        """
        return self.server.supervisor.restart()

    def reload(self):
        """Reload the configuration : 
                @return array result [[added, changed, removed]]
        """
        return self.server.supervisor.reloadConfig()

    # All Plugin Control Methods ----------------------------------------------

    def getAllPluginInfo(self):
        """Get info about all plugins"""
        return self.server.supervisor.getAllProcessInfo()

    def startAllPlugins(self):
        """Start all plugins.
                @return array result An array of plugins status info structs
        """
        return self.server.supervisor.startAllProcesses()

    def stopAllPlugins(self):
        """Stop all plugins.
                @return array result An array of plugins status info structs
        """
        return self.server.supervisor.stopAllProcesses()

    # Plugin Control Methods --------------------------------------------------

    def getPluginInfo(self, plugin_name):
        """Get info about a plugin named plugin_name.
                @return struct containing data about the plugin
        """
        return self.server.supervisor.getProcessInfo(plugin_name)

    def startPlugin(self, user, plugin_name):
        """Start a plugin.
                @param string : plugin_name, user:plugin_name, or user:*
        """
        name = "{user}:{plugin_name}".format(user=user, plugin_name=plugin_name)
        return self.server.supervisor.startProcess(name)

    def stopPlugin(self, user, plugin_name):
        """stop a plugin by name.
                @param string : plugin_name, user:plugin_name, or user:*
        """
        name = "{user}:{plugin_name}".format(user=user, plugin_name=plugin_name)
        return self.server.supervisor.stopProcess(name)

    # User Plugin Control Methods ---------------------------------------------

    def startUserPlugins(self, user):
        """Start all user plugins.
                @return array result An array of plugins status info structs
        """
        return self.server.supervisor.startProcessGroup(user)

    def stopUserPlugins(self, user):
        """stop all user plugins.
                @return array result An array of plugins status info structs
        """
        return self.server.supervisor.stopProcessGroup(user)

    # Help Methods ------------------------------------------------------------

    def help(self, name=None):
        """Return a string showing the method's documentation if the name is given
            otherwise liste all available methods. """
        if name:
            return self.server.system.methodHelp(name)
        else:
            return self.server.system.listMethods()


# Main ------------------------------------------------------------------------
if __name__ == "__main__":
    pm = PluginManager()
    print(pm.help())
