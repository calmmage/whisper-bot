# Section 1 - improving existing bot

## feature 1.1 - improve logging

- [ ] Delete the 'generating' message from telegram once finished
- [ ] Track time for generation - add to log
- [ ] Report progress and remaining time to telegram
    - [ ] Can I have text-based tqdm?
    - [ ] I can probably send updates every 5 seconds
- [ ] For sequential mode report the text generated so far

## feature 1.2 - add parallel processing

- [ ] Report processing mode in the status message
- [ ] Calculate expected processing time
- [ ] use parallel mode in the bot

## feature 1.3 - add config settings commands

- [ ] s1 add a command to configure parallel mode
- [ ] s1 add parallel mode to config class
- [ ] s4 add automatic command generation for all config fields

# Section 2 - developing new features

## feature 2.1 - gpt summary

- [ ] Generate punctuation with gpt

# Section 3 - common features (for bot base)

## feature 3.1 - gpt utils

- [ ] extract gpt utils to separate file
- [ ] extract gpt utils to a separate lib

# Section 4 - unsorted

## feature 0.2 - gpt fill/extract the info

## feature 0.3 - gpt guess speakers?

## feature 3 - add retries

- On file download
- On openai api
    - Option 1: decorator
    - Option 2: write a custom method

## feature 5 -

## feature 6 - add video support

- [ ] detect and download video from telegram (add handler)
- [ ] extract audio from video
