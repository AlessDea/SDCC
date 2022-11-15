import pybreaker


class GreetingsListener(pybreaker.CircuitBreakerListener):
    def before_call(self, cb, func, *args, **kwargs):
        print("Calling service...")

    def state_change(self, cb, old_state, new_state):
        print("Breaker changed state from {0} to {1}".format(old_state, new_state))

    def failure(self, cb, exc):
        print("System error occured")

    def success(self, cb):
        print("Called successfully")

class LogListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        msg = "State Change: CB: {0}, New State: {1}".format(cb.name, new_state)
        logging.info(msg)
