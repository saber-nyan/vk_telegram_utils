# <p align="center">VK.com, VkOpt & Telegram utilities</p>

## Clone
```bash
git clone https://github.com/saber-nyan/vk_telegram_utils.git
```

## Install
```bash
cd ./vk_telegram_utils/
python3 -m venv ./venv
. ./venv/bin/activate
pip install .
```

## Launch
### VkOpt/Telegram Desktop HTML dump parser
#### Example
```bash
python -m vkopt_telegram_parser -i ~/Documents/VkOpt1.html -i ~/Documents/VkOpt2.html -t ~/Documents/ChatExport_04_03_2020/messages.html -t ~/Documents/ChatExport_04_03_2020/messages2.html -x ./corpus.txt -d 'somevkusername' -m 'Telegram Name'
```
#### Usage
```
usage: python -m vkopt_telegram_parser [-h] [--verbose] [--vkopt-file VKOPT.html] [--vkopt-id username] [--telegram-file TG.html] [--telegram-id name] [--out-json /path/to/dump.json]
                                       [--out-pickle /path/to/dump.pkl] [--out-txt /path/to/dump.txt]

Parses VkOpt and Telegram dialog dumps.

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         show additional debug logs
  --vkopt-file VKOPT.html, -i VKOPT.html
                        choose VkOpt dump files
  --vkopt-id username, -d username
                        select usernames to extract, without @ (VkOpt)
  --telegram-file TG.html, -t TG.html
                        choose Telegram dump files
  --telegram-id name, -m name
                        select names to extract (Telegram; do not confuse with a username!)
  --out-json /path/to/dump.json, -j /path/to/dump.json
                        choose a path to dump results as JSON
  --out-pickle /path/to/dump.pkl, -p /path/to/dump.pkl
                        choose a path to dump results as Pickle
  --out-txt /path/to/dump.txt, -x /path/to/dump.txt
                        choose a path to dump results as plain text

desu~
```

### VK.com API dialogs dumper
#### Example
```bash
python -m vk_dumper -c 50000 -m -d vk_user_domain -x ./corpus.txt phone_number_or_email password
```
#### Usage
```
usage: python -m vk_dumper [-h] [--verbose] [--message-count count] [--vk-id username] [--out-json /path/to/dump.json] [--out-pickle /path/to/dump.pkl] [--out-txt /path/to/dump.txt] [--markov]
                           login password

Utility for dumping VK messages.

positional arguments:
  login                 VK.com phone number/email
  password              VK.com password

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         show additional debug logs
  --message-count count, -c count
                        maximum messages count to extract
  --vk-id username, -d username
                        select usernames to extract, without @
  --out-json /path/to/dump.json, -j /path/to/dump.json
                        choose a path to dump results as JSON
  --out-pickle /path/to/dump.pkl, -p /path/to/dump.pkl
                        choose a path to dump results as Pickle
  --out-txt /path/to/dump.txt, -x /path/to/dump.txt
                        choose a path to dump results as plain text
  --markov, -m          store plaintext with line break after each message for markovify

desu~
```
