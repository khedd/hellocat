from listen import Listener
from talk import Talk
from os import system

class Assistant:
    # states of the assistant
    # the assistant starts from the None state and the states that it can go are stated as list
    states = {None: ["hello cat", "open folder", "open app"],
              "hello cat": ["open folder", "open app"],
              "open app": ["firefox", "visual code", "ins ta gram", "duo lingo", "twitter", "git hub", "g mail"],
              "open folder": ["thesis"]
              }

    # replies that will be played by talker
    replies = {"hello cat": "hello", 
               "open app": "which app?",
               "open folder": "which folder?",
               "ins ta gram": "opening instagram",
               "duo lingo": "opening duolingo",
               "twitter": "opening twitter",
               "git hub": "opening github",
               "g mail": "opening gmail",
               "thesis": "opening thesis folder",
               "firefox": "opening firefox."
               }

    # what to run with which command
    commands = { "firefox": "firefox",
                 "thesis": "nautilus /home/khedd/Documents/thesis/",
                 "ins ta gram": "firefox www.instagram.com",
                 "duo lingo": "firefox www.duolingo.com",
                 "git hub": "firefox www.github.com/trending",
                 "g mail": "firefox https://mail.google.com/mail/u/0/",
                 "twitter": "firefox www.twitter.com"
                }
    def __init__(self, *, library_path, keyword_file_paths, model_file_path):
        """
        :param library_path: path of the porcupine shared library
        :param keyword_file_paths: path of the ppn files of porcupine
        :param model_file_path: porcupine model file .pv
        """

        sensitivities = [0.5] * len(keyword_file_paths)
        self.listener = Listener(library_path, model_file_path, keyword_file_paths, sensitivities)
        self.talker = Talk()
        self.state = None

    # infinite loop until keypress
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


if __name__ == '__main__':
    library_path = "/home/khedd/Dev/Fun/Porcupine/lib/linux/x86_64/libpv_porcupine.so"
    keyword_file_paths = glob.glob( "/home/khedd/Dev/python/asst/khedd/keywords/*.ppn")
    model_file_path = "/home/khedd/Dev/Fun/Porcupine/lib/common/porcupine_params.pv"
    asst = Assistant(library_path=library_path, keyword_file_paths=keyword_file_paths,
                    model=model)
    asst.run()

