# slack_invoker
Invoke Python functions from Slack

## Installation

```
pip3 install slack_invoker
```

## Using the library

`slack_invoker` currently only supports the creation of Slack bot users via the RTM API.

The [sample_bot](./sample_bot) shows how you can set up a simple bot user which accepts messages
when it is mentioned, parses the messages using an
[`argparse`](https://docs.python.org/3/library/argparse.html) argument parser, passes these
arguments to a Python function, and displays the result in Slack.

The Slack documentation has more information on [how to create a bot user](https://get.slack.help/hc/en-us/articles/115005265703-Create-a-bot-for-your-workspace).

The sample bot requires you to export your `Bot User OAuth Access Token` (provided on
[https://api.slack.com](https://api.slack.com) once you create the bot user) as the
`SLACK_BOT_USER_ACCESS_TOKEN` environment variable.
