# tickets

<img src="https://discord.com/assets/ff41b628a47ef3141164bfedb04fb220.png" alt="Logo" width="400">

Tickets is a Discord ticket bot that modernizes the way server tickets are handled through use of newly announced Button API endpoints.

![Python Version](https://img.shields.io/badge/python-v3.8.8-brightgreen) ![GitHub repo size](https://img.shields.io/github/repo-size/ayushgun/tickets)

Tickets is highly customizable and modifiable. It is a bot that allows servers to manage tickets that advance user-based cryptocurrency payments. Currently, Bitcoin, Ethereum, and Litecoin are supported as payment methods.

Although there is no official documentation of this bot, each command and config area includes docstrings that explain the purpose and intent of the command. Additionally, a config area has been created at the top of the `main.py` file. 

- [tickets](#tickets)
  - [Quick Start](#installation)
  - [Important Notes](#important)
  - [Support](#support)
  - [Contributions](#contributions)
  - [LICENSE](https://github.com/ayushgun/tickets/blob/main/LICENSE)

# Installation

1. Create a Discord Bot and copy its token, then djust the variables located underneath `# Bot Config`, `# Role Config`, and `# Ticket Config` in **main.py**

2. Adjust the emote IDs for the Payment Methods located under `# Ticket Config` in **main.py**

3. Assuming Python and Pip are pre-installed, run `pip install -r requirements.txt`

4. Run `python main.py` to start the bot

# Important
Please note that the bot will NOT start without adjusting the config correctly. All configs must be properly set up. 

The emote IDs can be found by typing `\{emote}` in Discord and copying the subsequent ID sent. 

Example: Sending "\:python:" returns "<:python:286529073445076992>", where `286529073445076992` is the emote ID.

# Support
Currently, support for this bot is provided on the very basic level. As a student, it is difficult for me to attend to every support request, but I will try my best to make it happen. Please open an issue for support or bug reports.

# Contributions
> We're currently closed to taking any requests, if you make a PR, it'll most likely be denied due to our policies.
