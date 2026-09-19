from crewai.utilities.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
    TaskCompletedEvent,
    FlowStartedEvent,
    FlowFinishedEvent,
    MethodExecutionStartedEvent,
    MethodExecutionFinishedEvent
)
from crewai.utilities.events.base_event_listener import BaseEventListener

class MyCustomListener(BaseEventListener):
    def __init__(self):
        super().__init__()

    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            print(f"Crew '{event.crew_name}' has started execution!")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            print(f"Crew '{event.crew_name}' has completed execution!")
            print(f"Output: {event.output}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_execution_completed(source, event):
            print(f"Agent '{event.agent.role}' completed task")
            print(f"Output: {event.output}")
            
        @crewai_event_bus.on(TaskCompletedEvent)
        def on_task_completed(source, event):
            print("the event is", event)
            print(f"Task '{event.task.name}' completed")
            print(f"Output: {event.output}")
            
        @crewai_event_bus.on(FlowStartedEvent)
        def on_flow_started(source, event):
            print("the event is", event)
            print(f"Flow '{event.flow_name}' started")
            
        @crewai_event_bus.on(FlowFinishedEvent)
        def on_flow_finished(source, event):
            print("the event is", event)
            print(f"Flow '{event.flow_name}' finished")
            
        @crewai_event_bus.on(MethodExecutionStartedEvent)
        def on_method_execution_started(source, event):
            print("the event is", event)
            print(f"Method '{event.method_name}' started")

my_custom_listener = MyCustomListener()