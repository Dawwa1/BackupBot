# PUBLIC VERSION BRANCH

public version of the bot that basically acts as an API for mongodb

## Idea:
- You invite the bot to your server and run `/setup`
    - You input your MongoDB credentials for your own database
- The bot will then use your database to store data instead of my own

- Could add a premium feature where you don't have to input your own database credentials and instead use mine

- Commands:
    - `/setup` - sets up the bot for your server
    - `/backup {channel} {# of messages}` - backs up amt of messages from `{channel}` to database
    - `/restore {channel}` - restores messages from database to `{channel}`
    - `/clear {channel} {# of messages}` - clears amt of messages from `{channel}`
    - `list {server}` - lists all the channels and their servers that have been backed up
    - `/help` - shows help message