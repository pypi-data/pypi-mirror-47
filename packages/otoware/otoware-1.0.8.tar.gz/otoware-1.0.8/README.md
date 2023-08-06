# otoware
otoware 手伝い

## install
1. First, install portaudio

  - arch linux
  `sudo pacman -S portaudio tk`
  - ubuntu or devian
  `sudo apt-get install portaudio`

2. Next, install with pip

  `pip install -e .`

3. compile

  `python setup.py sdist`

4. run

  `otowari`

data/origin.wav がdist_origin.wav になります

## TODO
ファイル名と音割れの度合いの変数を外部から与えられるようにする
