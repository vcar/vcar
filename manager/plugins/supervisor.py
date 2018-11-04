import re
import xmlrpc
from xmlrpc.client import ServerProxy, Fault


class PluginManager(object):

    def __init__(self):
        """Initialize it"""
        self.status = None
        self.error = None
        # Init XmlRcp client
        self.server = xmlrpc.client.ServerProxy('http://localhost:9001/RPC2')

    # Plugin Manager Methods --------------------------------------------------

    def getState(self):
        """Return the plugin manager state as struct
                        #statecode 	statename 	Description
                        2 			FATAL 		PM has experienced a serious error.
                        1 			RUNNING 	PM is working normally.
                        0 			RESTARTING 	PM is in the process of restarting.
                        -1 			SHUTDOWN 	PM is in the process of shutting down.
        """
        state = {}
        try:
            state = self.server.supervisor.getState()
            self.status = state['statecode']
        except ConnectionRefusedError:
            self.status = -1

        return state

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

    # Plugins list Control Methods ----------------------------------------------

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

    def getPluginInfo(self, user, plugin_name):
        """Get info about a plugin named plugin_name.
                @return struct containing data about the plugin
        """
        try:
            name = "{user}@{plugin_name}".format(user=user, plugin_name=plugin_name)
            return self.server.supervisor.getProcessInfo(name)
        except Fault:
            return {'status': -1, "description": f"plugin for user '{user}' with name '{plugin_name}' not found"}

    def startPlugin(self, user, plugin_name):
        """Start a plugin.
                @param string : plugin_name, user:plugin_name, or user:*
        """
        name = "{user}@{plugin_name}".format(user=user, plugin_name=plugin_name)
        return self.server.supervisor.startProcess(name)

    def stopPlugin(self, user, plugin_name):
        """stop a plugin by name.
                @param string : plugin_name, user:plugin_name, or user:*
        """
        name = "{user}@{plugin_name}".format(user=user, plugin_name=plugin_name)
        return self.server.supervisor.stopProcess(name)

    def restartPlugin(self, user, plugin_name):
        """stop a plugin and started again.
                @param string : plugin_name, user:plugin_name, or user:*
        """
        name = "{user}@{plugin_name}".format(user=user, plugin_name=plugin_name)
        state = self.server.supervisor.stopProcess(name)
        return state and self.server.supervisor.startProcess(name)

    def suspendPlugin(self, user, plugin_name):
        """Suspend a plugin.
                :param user:
                :param plugin_name:
                :return: dict
        """
        name = f"{user}@{plugin_name}"

        return self.server.supervisor.signalProcess(name, "SIGSTOP")

    def resumePlugin(self, user, plugin_name):
        """Suspend a plugin.
                :param user:
                :param plugin_name:
                :return: dict
        """
        name = f"{user}@{plugin_name}"

        return self.server.supervisor.signalProcess(name, "SIGCONT")

    # User Plugin Control Methods ---------------------------------------------

    def startUserPlugins(self, user):
        """Start all user plugins.
                @return array result An array of plugins status info structs
        """
        plugins = []
        for process in self.server.supervisor.getAllProcessInfo():
            pattern = f"{user}@([a-zA-Z0-9]+)"
            try:
                match = re.match(pattern, process['name'])
                name = match.group(0)
                state = self.server.supervisor.startProcess(name)
                plugins.append({'name': name, 'state': state})
            except Fault as e:
                plugins.append({'name': name, 'state': e.faultCode})
            except AttributeError:
                pass

        # return self.server.supervisor.startProcessGroup(user)
        return plugins

    def stopUserPlugins(self, user):
        """stop all user plugins.
                @return array result An array of plugins status info structs
        """
        plugins = []
        for process in self.server.supervisor.getAllProcessInfo():
            pattern = f"{user}@([a-zA-Z0-9]+)"
            try:
                match = re.match(pattern, process['name'])
                name = match.group(0)
                state = self.server.supervisor.stopProcess(name)
                plugins.append({'name': name, 'state': state})
            except Fault as e:
                plugins.append({'name': name, 'state': e.faultCode})
            except AttributeError:
                pass

        # return self.server.supervisor.stopProcessGroup(user)
        return plugins

    def restartUserPlugins(self, user):
        """restart all user plugins.
                @return array result An array of plugins status info structs
        """
        plugins = []
        for process in self.server.supervisor.getAllProcessInfo():
            pattern = f"{user}@([a-zA-Z0-9]+)"
            try:
                match = re.match(pattern, process['name'])
                name = match.group(0)
                state_stop = self.server.supervisor.stopProcess(name)
                state_start = self.server.supervisor.startProcess(name)
                plugins.append({'name': name, 'state': state_stop and state_start})
            except Fault as e:
                plugins.append({'name': name, 'state': e.faultCode})
            except AttributeError:
                pass

        # return self.server.supervisor.stopProcessGroup(user)
        return plugins

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
    # pm.restart()
    print(pm.startPlugin(user="vcar", plugin_name="dashboard"))
