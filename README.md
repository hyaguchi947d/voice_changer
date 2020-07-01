# voice changer

作者：矢口裕明(クシナダ機巧株式会社)

本プログラムは Creative Commons 0 で公開します。
作者はいかなる権利も主張しません。

## 使い方

pyaudio,pyworld,sounddeviceを使用しています。

```
$ pip install pyaudio pyworld sounddevice
```

まずサウンドデバイスの設定を行います。

```
$ ./device_query.py
```

で認識されているサウンドデバイスを取得します。
ここで得られた入出力デバイスのインデックスを`voicechanger_gui.py`冒頭の
`input_device_index`,`output_device_index`に設定してください。

```
$ ./voice_changer_gui.py
```

で起動します。
スライダーを動かすと声を変換できます。

## 参考文献

- M. Morise, F. Yokomori, and K. Ozawa, ``WORLD: a vocoder-based high-quality speech synthesis system for real-time applications,'' IEICE transactions on information and systems, vol. E99-D, no. 7, pp. 1877-1884, 2016.
- M. Morise, ``D4C, a band-aperiodicity estimator for high-quality speech synthesis,'' Speech Communication, vol. 84, pp. 57-65, Nov. 2016.
- https://qiita.com/ohtaman/items/84426cee09c2ba4abc22
- https://gist.github.com/tam17aki/8e702542f5e16c0815e7ddcc6e14bbb8
