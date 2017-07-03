class BaseEvent(object):
    """
    A superclass for any events that might be generated by
    an object and sent to the EventManager.
    """
    def __init__(self):
        self.name = "Generic event"
    def __str__(self):
        return self.name

class Event_Quit(BaseEvent):
    """
    Quit event.
    """
    def __init__ (self):
        self.name = "Quit event"

class Event_Initialize(BaseEvent):
    """
    Initialize all object/player
    """
    def __init__(self):
        self.name = "Initialize game"

class Event_StateChange(BaseEvent):
    """
    change game state
    """
    def __init__(self,state):
        self.name = "StateChangingEvent"
        self.state = state    

class Event_EveryTick(BaseEvent):
    """
    Tick event.
    """
    def __init__ (self):
        self.name = "Tick event"

class Event_TimeUp(BaseEvent):
    """
    Time's Up
    """
    def __init__(self):
        self.name = "Time's Up"
    def __str__(self):
        return "TimeUp"

class Event_SkillCard(BaseEvent):
    """
    UseSkillCard
    """
    def __init__(self,SkillIndex,PlayerIndex):
        self.name = "Use SkillCard"
        self.SkillIndex = SkillIndex
        self.PlayerIndex = PlayerIndex
    def __str__(self):
        return "UseSkillCard" 

class Event_Action(BaseEvent):
    """
    UseSkill
    """
    def __init__(self,ActionIndex,PlayerIndex):
        self.name = "Use Action"
        self.ActionIndex = ActionIndex
        self.PlayerIndex = PlayerIndex
    def __str__(self):
        return "UseAction"

class Event_Move(BaseEvent):
    """
    Move event.
    """
    def __init__(self, player, direction):
        self.name = "Move event"
        self.PlayerIndex = player
        self.Direction = direction

class Event_PlayerModeChange(BaseEvent):
    """
    Mode change event.
    """
    def __init__(self, player):
        self.name = "ModeChange event"
        self.PlayerIndex = player
class Event_EverySec():
    """
    model needs timer
    """
    def __init__(self):
        self.name = "Timer"

class EventManager(object):
    """
    We coordinate communication between the Model, View, and Controller.
    """
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def RegisterListener(self, listener):
        """ 
        Adds a listener to our spam list. 
        It will receive Post()ed events through it's notify(event) call. 
        """
        self.listeners[listener] = 1

    def UnregisterListener(self, listener):
        """ 
        Remove a listener from our spam list.
        This is implemented but hardly used.
        Our weak ref spam list will auto remove any listeners who stop existing.
        """
        if listener in self.listeners.keys():
            del self.listeners[listener]
        
    def Post(self, event):
        """
        Post a new event to the message queue.
        It will be broadcast to all listeners.
        """
        # this segment use to debug
        if not isinstance(event, Event_EveryTick):
            print( str(event) )
        for listener in self.listeners.keys():
            listener.notify(event)
