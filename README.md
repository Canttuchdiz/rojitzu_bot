# Rojitzu Bot

Rojitzu Bot is a Discord Bot dedicated to the [Rojitzu Server](https://discord.gg/rojitzu).

## Installation

Get the repository from [github](https://github.com/) to install this bot.
```bash
git clone https://github.com/Canttuchdiz/rojitzu_bot.git
```

Make a .env file as another project file:
```
token = (your token)
```

Build and run the bot by running:
```bash
docker compose up -d --build
```

Every once and awhile run:
```bash
docker system prune -a
```

## Usage

Using ``/create`` and ``/log`` are the commands for controlling the ticketing.

## Notes

In any text channel, the owner must run ``!sync`` the first time you run
your bot.

For any configuration use the ``config.py`` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
