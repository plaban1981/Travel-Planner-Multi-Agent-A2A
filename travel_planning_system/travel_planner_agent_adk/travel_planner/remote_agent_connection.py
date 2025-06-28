"""Remote agent connection for A2A communication."""

from a2a.client import A2AClient
from a2a.types import AgentCard


class RemoteAgentConnections:
    """Manages connections to remote agents."""

    def __init__(self, agent_card: AgentCard, agent_url: str):
        """Initialize the remote agent connection."""
        self.agent_card = agent_card
        self.agent_url = agent_url
        self.client = A2AClient(agent_url)

    async def send_message(self, message_request):
        """Send a message to the remote agent."""
        return await self.client.send_message(message_request) 