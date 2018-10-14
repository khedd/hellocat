from listen import Listener
from talk import Talk
from os import system

class Assistant:
    states = {None: ["hello cat", "open folder", "open app"],
              "hello cat": ["open folder", "open app"],
              "open app": ["firefox", "visual code", "ins ta gram", "duo lingo", "twitter"],
              "open folder": ["thesis"]
              }
    replies = {"hello cat": "hello", 
               "open app": "which app?",
               "open folder": "which folder?",
               "ins ta gram": "opening instagram",
               "duo lingo": "opening duolingo",
               "twitter": "opening twitter",
               "firefox": "opening firefox."
               }

    commands = { "firefox": "firefox",
                 "thesis": "nautilus /home/khedd/Documents/thesis/",
                 "ins ta gram": "firefox www.instagram.com",
                 "duo lingo": "firefox www.duolingo.com",
                 "twitter": "firefox www.twitter.com"
                }
    def __init__(self):
        self.listener = Listener.create()
        self.talker = Talk()
        self.state = None

    def run(self):
        try:
            while True:
                result = self.listener.listen()

                avail_states = self.states.get(self.state, None)
                if result:
                    print(result)
                    if result in avail_states:
                        self.state = result
                        reply = self.replies.get(result, None)

                        if reply:
                            self.talker.talk(reply)

                        command = self.commands.get(result, None)
                        if command:
                            system(command)
                            system("xdotool getactivewindow getwindowname")
                        
                    if result == "cancel":
                        self.state = None

                avail_states = self.states.get(self.state, None)
                if not avail_states:
                    self.state = None

        except KeyboardInterrupt:
            print('Stopping ...')
        finally:
            pass
            # if porcupine is not None:
            #     porcupine.delete()

            # if audio_stream is not None:
            #     audio_stream.close()

            # if pa is not None:
            #     pa.terminate()

asst = Assistant()
asst.run()