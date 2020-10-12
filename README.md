# Text Character Switcher
A Tkinter GUI program written to detect abnormal characters in a text (such as ﬁ, ﬀ), and make changes to them automatically.
Also supports manually adding characters to switches, and word replacements (such as covid to COVID, etc.).

## Main Interface
![Main Interface Image](https://github.com/csjaugustus/textswitcher/blob/master/example_images/maininterface.png)
"Abnormal" characters can be see in the given text.

## White List
![White List Image](https://github.com/csjaugustus/textswitcher/blob/master/example_images/whitelist.png)
The program scans through each character in the text, and marks a character as "abnormal" if it is not part of the white list (which is a regex pattern).

## Unregistered Characters Detected
![Unregistered Characters Detected Image](https://github.com/csjaugustus/textswitcher/blob/master/example_images/whitelistpopup.png)
Whenever a new "abnormal" character is detected, the user will be prompted to either whitelist the character, or tell the program how to make switches for the unregistered characters.

## Switch Success
![Switch Success Image](https://github.com/csjaugustus/textswitcher/blob/master/example_images/switchsuccess.png)
Once all "abnormal" characters are registered, the program goes through the "switch list" and makes all the switches. The user is shown what switches were made, and the result text is copied to clipboard.

## Switch List
![Switch List Image](https://github.com/csjaugustus/textswitcher/blob/master/example_images/switchlist.png)
The user also has the option to manually go through the switch list to add/delete/edit entries. The program not only supports switching single characters, but also word replacements (which work differently, but the user does not have to register the entry differently).
