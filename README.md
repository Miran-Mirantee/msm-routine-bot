# MapleStoryM routine bot

For people who got better things to do than pressing buttons on your phone for hours every single day.

## Requirement

- Python **3.10+** You can download it from [python.org](https://www.python.org/downloads/)

## Installation

1. Clone the repository:

```
 git clone https://github.com/yourusername/your-project.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

## How to use

1. Add your character image for the program to detect. Do it in this format.

   > ![Screenshot](imgs/characters/charactername.png)

2. Add the details of your characters. How you want the program to play them.

- For cdd and powder alts

```
[
  {
    "imgUrl": "./imgs/characters/charactername.png",
    "doElite": true,
    "eliteLvl": 200
  }
]
```

- For main

```
[
  {
    "imgUrl": "./imgs/characters/charactername.png",
    "gemColor": "yellow"
  }
]
```

3. Once everything is setup, open your MSM pc client on fullscreen. (If you have multiple monitors, put the MSM pc client window in main monitor) Then run the following command.

```
python .\main.py
```

### Note

This is my laziest attempt to make this game less painful to play as possible.
