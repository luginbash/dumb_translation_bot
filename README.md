# dumb_translation_bot
A dead simple dumb translation bot using Telegram inline API and DeepL


## Quickstart 

```bash
export TELEGRAM_TOKEN=<...> DEEPL_AUTH_KEY=<...> 
poetry run telegram_dumb_translate_bot/main.py
```

## Advanced

Set target languages

```bash
# Comma separated list of languages in https://www.deepl.com/docs-api/translate-text/translate-text/
TARGET_LANGS=zh,cz,ja
```

Change telegram API server
```
TELEGRAM_API=<...>
# Example
TELEGRAM_API=https://api.telegram.org/bot
```

## Deployment

Docker-compose

```bash
# prod.env
TELEGRAM_TOKEN=10000000:AAAA0000012345678A90
TELEGRAM_API=http://10.0.0.1:8080/bot
DEEPL_AUTH_KEY=279a2e9d-83b3-c416-7e2d-f721593e42a0:fx# An example key from DeepL docs
```

```yaml
version: "3"
services:
  dumb_translation_bot:
    image: ghcr.io/luginbash/dumb_translation_bot:<ver tag>
    env_file: .env
    restart: unless-stopped
```
