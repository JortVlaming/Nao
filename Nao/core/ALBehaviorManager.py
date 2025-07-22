from typing import List, Callable

from ..proxy import Proxy
from ..robot import Robot


class ALBehaviorManager(Proxy):
    def __init__(self, robot: Robot, name: str):
        super().__init__(robot, name)

    """
    Methods
    """

    def addDefaultBehavior(self, prefixedBehavior: str) -> None:
        """
        Set the given behavior as default
        :param prefixedBehavior: Behavior name.
        :return:
        """
        self.proxy.addDefaultBehavior(prefixedBehavior)

    def getBehaviorTags(self, behavior: str) -> List[str]:
        """
        Get tags found on the given behavior.
        :param behavior: The local path towards a behavior or a directory.
        :return: The list of tags found.
        """
        return self.proxy.getBehaviorTags(behavior)

    def getBehaviorsByTag(self, tag: str) -> List[str]:
        """
        Get installed behaviors directories names and filter it by tag.
        :param tag: A tag to filter the list with.
        :return: Returns the behaviors list.
        """
        return self.proxy.getBehaviorsByTag(tag)

    def getBehaviorNature(self, behavior: str) -> str:
        """
        Get the nature of the given behavior.
        :param behavior: Behavior name.
        :return: Returns the nature name of the behavior.
        """
        return self.proxy.getBehaviorNature(behavior)

    def getDefaultBehaviors(self) -> List[str]:
        """
        Get default behaviors
        :return: Return default behaviors
        """
        return self.proxy.getDefaultBehaviors()

    def getInstalledBehaviors(self) -> List[str]:
        """
        :return: Returns the behaviors list
        """
        return self.proxy.getInstalledBehaviors()

    def getLoadedBehaviors(self) -> List[str]:
        """
        Get loaded behaviors
        :return: Returns loaded behaviors
        """
        return self.proxy.getLoadedBehaviors()

    def getRunningBehaviors(self) -> List[str]:
        """
        Get running behaviors
        :return: Return running behaviors
        """
        return self.proxy.getRunningBehaviors()

    def getTagList(self) -> List[str]:
        """
        Get tags found on installed behaviors.
        :return: The list of tags found.
        """
        return self.proxy.getTagList()

    def isBehaviorInstalled(self, name: str) -> bool:
        """
        :param name: The behavior directory name
        :return: Returns true if it is a valid behavior
        """
        return self.proxy.isBehaviorInstalled(name)

    def isBehaviorLoaded(self, name: str) -> bool:
        """
        Tell if supplied name corresponds to a loaded behavior
        :param name: Behavior name.
        :return: Returns true if the name supplied is a loaded behavior
        """
        return self.proxy.isBehaviorLoaded(name)

    def isBehaviorRunning(self, name: str) -> bool:
        """
        Tell if supplied name corresponds to a running behavior
        :param name: Behavior name.
        :return: Returns true if the name supplied is a running behavior
        """
        return self.proxy.isBehaviorRunning(name)

    def playDefaultProject(self) -> None:
        """
        Play default behaviors
        :return:
        """
        self.proxy.playDefaultProject()

    def preloadBehavior(self, name: str) -> bool:
        """
        Load a behavior
        :param name: Behavior name.
        :return: Returns true if it was successfully loaded.
        """
        return self.proxy.preloadBehavior(name)

    def removeDefaultBehavior(self, name: str) -> None:
        """
        Remove the given behavior from the default behaviors
        :param name: Behavior name.
        :return:
        """
        self.proxy.removeDefaultBehavior(name)

    def resolveBehaviorName(self, behaviorName: str) -> str:
        """
        Find out the actual <package>/<behavior> path behind a behavior name.
        :param behaviorName: name of a behavior
        :return: Returns the actual <package>/<behavior> path if found, else an empty string. Throws an ALERROR if two behavior names conflicted.
        """
        return self.proxy.resolveBehaviorName(behaviorName)

    def runBehavior(self, name: str) -> None:
        """
        Start a behavior and wait for its end. Return when the behavior is stopped. Throw if the behavior cannot be started or does not exist.
        :param name: Behavior name.
        :return:
        """
        self.proxy.runBehavior(name)

    def startBehavior(self, name: str) -> None:
        """
        Start a behavior. Return when the behavior is started. Throw if the behavior cannot be started or does not exist.
        :param name: Behavior name.
        :return:
        """
        self.proxy.startBehavior(name)

    def stopAllBehaviors(self) -> None:
        """
        Stop all behaviors
        :return:
        """
        self.proxy.stopAllBehaviors()

    def stopBehavior(self, name: str) -> None:
        """
        Stop a behavior
        :param name: Behavior name.
        :return:
        """
        self.proxy.stopBehavior(name)

    """
    Events
    """

    def onBehaviorAdded(self, callback: Callable[[str, str, str], None]) -> None:
        """
        Register a method that is raised when a behavior is installed.
        :param callback: Method that is called. method has 3 parameters: eventName: “ALBehaviorManager/BehaviorAdded”, behavior: str - the name of the behavior installed, subscriberIdentifier: str
        :return:
        """
        self._on("BehaviorAdded", callback, "event")

    def onBehaviorRemoved(self, callback: Callable[[str, str, str], None]) -> None:
        """
        Register a method that is raised when a behavior is removed.
        :param callback: Method that is called. method has 3 parameters: eventName: “ALBehaviorManager/BehaviorRemoved”, behavior: str - the name of the behavior removed, subscriberIdentifier: str
        :return:
        """
        self._on("BehaviorRemoved", callback, "event")

    def onBehaviorUpdated(self, callback: Callable[[str, str, str], None]) -> None:
        """
        Register a method that is raised when a behavior is updated.
        :param callback: Method that is called. method has 3 parameters: eventName: “ALBehaviorManager/BehaviorUpdated”, behavior: str - the name of the behavior updated, subscriberIdentifier: str
        :return:
        """
        self._on("BehaviorUpdated", callback, "event")

    def onBehaviorsAdded_e(self, callback: Callable[[str, List[str], str], None]) -> None:
        """
        Register a method that is raised when a package containing behaviors is installed
        :param callback: Method that is called. method has 3 parameters: eventName: “ALBehaviorManager/BehaviorsAdded”, behaviors: List[str] - a list containing the names of the behaviors installed, subscriberIdentifier: str
        :return:
        """
        self._on("BehaviorsAdded", callback, "event")

    def onBehaviorsRun(self, callback: Callable[[str, List[str], str], None]) -> None:
        """
        Register a method that is raised when the list of running behaviors change.
        :param callback: Method that is called. method has 3 parameters: eventName: “BehaviorsRun”, runningBehaviorList: List[str] - list of all running behaviors, subscriberIdentifier: str
        :return:
        """
        self._on("BehaviorsRun", callback, "event")

    """
    Signals
    """

    def onBehaviorsRemoved(self, callback: Callable[[List[str]], None]) -> None:
        """
        Register a method that is raised when behaviors are removed
        :param callback: Method that is called. method has 1 parameter: behaviorsRemoved: List[str] - Paths of the removed behaviors.
        :return:
        """
        self._on("behaviorsRemoved", callback, "signal")

    def onBehaviorFailed(self, callback: Callable[[str, str, str], None]) -> None:
        """
        Register a method that is raised when a behavior stops on error
        :param callback: Method that is called. method has 3 parameters: behaviorName: str - Name of the failing behavior, boxName: str - Name of the box where the error occurred, error: str - Error message.
        :return:
        """
        self._on("behaviorFailed", callback, "signal")

    def onBehaviorsAdded_s(self, callback: Callable[[List[str]], None]) -> None:
        """
        Register a method that is raised when behaviors are added.
        :param callback: Method that is called. Method has 1 parameter: behaviorsAdded: List[str] - Paths of the added behaviors.
        :return:
        """
        self._on("behaviorsAdded", callback, "signal")

    def onBehaviorStopped(self, callback: Callable[[str], None]) -> None:
        """
        Register a method that is raised when a behavior is stopped.
        :param callback: Method that is called. Method has 1 parameter: behaviorName: str - Name of the stopped behavior.
        :return:
        """
        self._on("behaviorStopped", callback, "signal")

    def onBehaviorStarted(self, callback: Callable[[str], None]) -> None:
        """
        Register a method that is raised when a behavior is started.
        :param callback: Method that is called. Method has 1 parameter: behaviorName: str - Name of the started behavior
        :return:
        """

        self._on("behaviorStarted", callback, "signal")

    def onBehaviorLoaded(self, callback: Callable[[str], None]) -> None:
        """
        Register a method that is raised when a behavior is started.
        :param callback: Method that is called. Method has 1 parameter: behaviorName: str - Name of the loaded behavior
        :return:
        """

        self._on("behaviorLoaded", callback, "signal")