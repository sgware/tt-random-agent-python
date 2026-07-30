"""
This is an example of a Tandem Tales agent and agent factory in Python. The
agent makes random decisions. The factory continuously creates new agents as
they are needed by the server. Both the agent and factory print messages
during important moments in their lifecycle to demonstrate how to use those
methods.
"""
import random
import time
import tt

class RandomAgent(tt.Client):
    """
    A Tandem Tales agent that makes random choices according to this policy:
    
    - If this is a normal turn, the agent chooses to `PASS` control to its
      partner 30% of the time. If not passing, it chooses a non-`PASS` action
      uniformly at random.
    - If this is a `SUCCEED`/`FAIL` decision, the agent chooses `SUCCEED` 80% of
      the time.
    
    Arguments:
        url (str): The URL of the Tandem Tales server.
        port (int): The network port of the Tandem Tales server.
    """
    
    # ID number that will be assigned to the next agent created.
    next_id = 0
    
    def __init__(self, url='localhost', port=tt.DEFAULT_PORT):
        # The arguments to `tt.Client` are:
        # 1. name: This agent's name. Hard-code this. Use up to 20 letters,
        #    digits, and undersocres.
        # 2. password: This should be left None so the Client will read it from
        #    the environment variables. Do not hard-code the password.
        # 3. world: The name of the world the agent wants to play in. Leave this
        #    None to play any world. Hard-code this if the agent is only
        #    designed to play in one story world.
        # 4. role: The role this client will have, which is either tt.PLAYER or
        #    tt.GM (for game master), or None for either role. Hard-code this if
        #    the agent is only designed to play as one role.
        # 5. partner: The partner this agents wants to play with. Leave this
        #    None to play with any partner. Hard-code this if the agent is only
        #    designed to play with one type of partner.
        # 6. key: The API key used for the external API. This should be left
        #    None so the Client will read it from the environment variables.
        # 7. url: The URL of the Tandem Tales server.
        # 8. port: The network port of the Tandem Tales server.
        super().__init__('random', None, None, None, None, None, url, port)
        self.id = RandomAgent.next_id
        RandomAgent.next_id += 1
    
    def __str__(self):
        return f"Random Agent {self.id}"
    
    def on_connect(self, connect):
        """
        Optional: Runs when the client connects to the server.
        """
        print(f"{self} has connected to the server.")
    
    def on_start(self, world, role, state):
        """
        Optional: Runs when the client starts its session.
        """
        print(f"{self} has started its session as the {role} in world \"{world['name']}\".")
    
    def on_update(self, status):
        """
        Optional: Runs each time the client sees a story world update, whether
        or not it is the client's turn.
        """
        pass
    
    def on_choice(self, status):
        """
        Required: Runs each time the world updates and it is the client's turn.
        """
        choices = status['choices']
        count = len(choices)
        choice = 0;
        # If this is a proposal...
        if count == 2 and choices[0]['type'] == tt.SUCCEED and choices[1]['type'] == tt.FAIL:
            # Choose to succeed 80% of the time.
            if random.randint(1, 10) <= 8:
                choice = 0
            else:
                choice = 1
        # If this is a normal turn...
        else:
            # If pass is the only option, do that.
            if count == 1:
                choice = 0
            # Choose to pass 30% of the time.
            elif random.randint(1, 10) <= 3:
                choice = count - 1
            # Otherwise, choose a random non-pass action.
            else:
                choice = random.randint(0, count - 2)
        print(f"{self} chooses: \"{choices[choice]['description']}\"")
        # Wait a random number of seconds to create the illusion of thinking.
        time.sleep(random.randint(2, 5))
        return choice
    
    def on_end(self, ending):
        """
        Optional: Runs when the story reaches an ending.
        """
        print(f"{self} has reached an ending: \"{ending['description']}\"")
    
    def on_close(self):
        """
        Optional: Runs when the client stops normally by the `close` method or
        because the story ended. Does not run if client crashes.
        """
        print(f"{self} has reached an ending: \"{ending['description']}\"")
    
    def on_stop(self, message):
        """
        Optional: Runs when the session stops.
        """
        if message == None:
            print(f"{self} has stopped.")
        else:
            print(f"{self} has stopped: \"{message}\"")
    
    def on_disconnect(self):
        """
        Optional: Run when the client disconnects from the server.
        """
        print(f"{self} has disconnected.")

class RandomAgentFactory(tt.Factory):
    """
    This factory creates new agents as they are needed by the server. A single
    agent only exists for one story session. When an agent that is waiting for a
    session finds a partner, this factory starts a new agent to take that
    agent's place.
    
    Arguments:
        max (int): The maximum number of clients that may be running at a time
            or 0 for no limit.
    """
    
    def __init__(self, max=0):
        super().__init__(max)
    
    def __str__(self):
        return 'Random Agent Factory'
    
    def on_start(self):
        """
        Optional: Runs when the factory starts.
        """
        print(f"{self} has started.")
    
    def create(self):
        """
        Required: Creates a new client.
        """
        return RandomAgent()
    
    def on_close(self):
        """
        Optional: Runs when the factory is closed or because a client raised an
        exception. Does not run if the factory is interrupted.
        """
        print(f"{self} has been closed.")
    
    def on_stop(self):
        """
        Optional: Runs when the factory has stopped running and all clients
        have finished their sessions and disconnected.
        """
        print(f"{self} has stopped.")

# Start a new factory and run until it is closed or interrupted.
factory = RandomAgentFactory()
factory.run()
