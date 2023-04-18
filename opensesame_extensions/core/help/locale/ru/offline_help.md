# Справка OpenSesame

*Это автономная справочная страница. Если вы подключены к Интернету,
вам доступна онлайн-документация на сайте <http://osdoc.cogsci.nl>.*

## Введение

OpenSesame - это графический конструктор экспериментов для социальных наук. С помощью OpenSesame вы можете легко создавать эксперименты с использованием графического интерфейса. Для сложных задач OpenSesame поддерживает написание сценариев на [Python].

## Начало работы

Лучший способ начать - это выполнить руководство. Руководства и многое другое можно найти онлайн:

- <http://osdoc.cogsci.nl/tutorials/>

## Цитирование

Пожалуйста, используйте следующую ссылку для цитирования OpenSesame в вашей работе:

- Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: Ан open-source графический конструктор экспериментов для социальных наук. *Behavior Research Methods*, *44*(2), 314-324. doi:[10.3758/s13428-011-0168-7](http://dx.doi.org/10.3758/s13428-011-0168-7)

## Интерфейс

Графический интерфейс состоит из следующих компонентов. Вы можете получить
соответствующую им помощь, нажав на значки справки в верхнем правом углу
каждой вкладки.

- *Меню* (в верхней части окна) показывает общие параметры, такие как открытие и сохранение файлов, закрытие программы и отображение этой страницы помощи.
- *Главная панель инструментов* (большие кнопки под меню) предлагает выбор наиболее значимых параметров из меню.
- *Панель инструментов элементов* (крупные кнопки слева от окна) показывает доступные элементы. Чтобы добавить элемент к вашему эксперименту, перетащите его из панели инструментов элементов на область обзора.
- *Область обзора* (Control + \\) показывает древовидный обзор вашего эксперимента.
- В *области вкладок* содержатся вкладки для редактирования элементов. Если вы нажмете на элемент в области обзора, соответствующая вкладка открывается в области вкладок. Справка также отображается в области вкладок.
- [Пул файлов](opensesame://help.pool) (Control + P) показывает файлы, которые сгруппированы с вашим экспериментом.
- [Инспектор переменных](opensesame://help.extension.variable_inspector) (Control + I) показывает все обнаруженные переменные.
- [Окно отладки](opensesame://help.stdout) (Control + D) представляет собой терминал [IPython]. Все, что ваш эксперимент выводит на стандартный вывод (т.е. используя `print()`), показывается здесь.

## Элементы

Элементы являются строительными блоками вашего эксперимента. Десять основных элементов предоставляют базовый функционал для создания эксперимента. Чтобы добавить элементы к вашему эксперименту, перетащите их из панели инструментов элементов в область обзора.

- Элемент [loop](opensesame://help.loop) несколько раз запускает другой элемент. Вы также можете определить независимые переменные в элементе LOOP.
- Элемент [sequence](opensesame://help.sequence) запускает несколько других элементов последовательно.
- Элемент [sketchpad](opensesame://help.sketchpad) отображает визуальные стимулы. Встроенные инструменты рисования позволяют легко создавать дисплеи стимулов.
- Элемент [feedback](opensesame://help.feedback) аналогичен `sketchpad`, но не подготавливается заранее. Благодаря этому элементы FEEDBACK могут быть использованы для предоставления обратной связи участникам.
- Элемент [sampler](opensesame://help.sampler) воспроизводит один звуковой файл.
- Элемент [synth](opensesame://help.synth) генерирует один звук.
- Элемент [keyboard_response](opensesame://help.keyboard_response) собирает ответы с помощью клавиш.
- Элемент [mouse_response](opensesame://help.mouse_response) собирает ответы с помощью щелчка мыши.
- Элемент [logger](opensesame://help.logger) записывает переменные в файл журнала.
- Элемент [inline_script](opensesame://help.inline_script) встраивает код на Python в ваш эксперимент.

Если установлено, дополнительные элементы плагинов предоставляют дополнительный функционал. Плагины отображаются рядом с основными элементами на панели инструментов элементов.

## Запуск вашего эксперимента

Вы можете запустить ваш эксперимент в режиме:

- Полноэкранный (*Control+R* или *Запуск -> Запуск в полноэкранном режиме*)
- Режим окна (*Control+W* или *Запуск -> Запуск в окне*)
- Быстрый запуск (*Control+Shift+W* или *Запуск -> Быстрый запуск*)

В режиме "быстрого запуска" эксперимент начинается немедленно в окне, используя файл журнала `quickrun.csv` и номер испытуемого 999. Это удобно на этапе разработки.

[python]: http://www.python.org/
[ipython]: http://www.ipython.org/