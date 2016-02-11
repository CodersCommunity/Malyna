from app.bot_interaction import BotInteraction
from app.irc_handle import IrcHandle
from app.config import Config
import string


def main():
    config = Config()
    handle = IrcHandle(config.return_config())
    interaction = BotInteraction(config.return_config())

    read_buffer = ""
    while True:  # While Connection is Active
        read_buffer = read_buffer + handle.irc_socket.recv(1024)
        temp = string.split(read_buffer, "\n")
        read_buffer = temp.pop()

        interaction.check_timefloodtime()

        for line in temp:
            interaction.check_ping(line)
            return_message = interaction.handle_line(interaction.username,
                                                     interaction.message,
                                                     interaction.parts)
            if interaction.ping:
                handle.send_ping(interaction.ping)
            else:
                handle.send_message(return_message)

if __name__ == "__main__":
    main()
