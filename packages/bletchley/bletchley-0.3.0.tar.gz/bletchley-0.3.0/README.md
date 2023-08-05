# About
bletchley is a pure [Python](https://www.python.org/) cryptographic tool suite. It provides historical ciphers. In the future it will also provide cryptographic attacks (cryptanalysis) to use against these ciphers.

If you find an bug or have a feature you'd like to see, please raise an [issue](https://gitlab.com/manny_cyber_wizard/bletchley/issues/new).

You can get in touch with us via this [link](incoming+manny-cyber-wizard-bletchley-10487839-issue-@incoming.gitlab.com).

The latest version of Bletchley is available via our [GitLab repo](https://gitlab.com/manny_cyber_wizard/bletchley), [PyPi](https://pypi.org/project/bletchley/) or [Conda-forge](https://github.com/conda-forge/bletchley-feedstock).


# Ciphers

Supported ciphers can be found on our [wiki](https://gitlab.com/manny_cyber_wizard/bletchley/wikis/home#ciphers).

## Simple Example
Ciphers can be accessed by adding bletchley to your Python path:
~~~~
export PYTHONPATH=$PYTHONPATH:/path/to/bletchley
~~~~
Then importing bletchley into your Python script:
~~~~
from bletchley.ciphers.rot13_cipher import ROT13Cipher
~~~~
And creating an instance of the cipher:
~~~~
my_cipher = ROT13Cipher()
~~~~
From here, you can encrypt and decrypt messages using the cipher:
~~~~
my_message = "Hello World!"
cipher_text = my_cipher.encrypt(my_message)
plain_text = my_cipher.decrypt(cipher_text)
~~~~

## Advanced Example
All ciphers implement the abstract class: Cipher. This means that all ciphers have encrypt and decrypt functions you can use. Note that some more complex ciphers (such as the [VIC Cipher](VIC-Cipher)) may have additional arguments when called. Where possible, these will be included with the cipher.

Taking the VIC cipher as an example, another argument is needed to encrypt/decrypt messages. This is called a 'checkerboard'. We can create our cipher in the same way as we did for the Caeser cipher before:
~~~~
from bletchley.ciphers.vic_cipher import VICCipher
my_cipher = VICCipher()
~~~~
Before we can encrypt/decrypt any message, a checkerboard is needed. We now have two options:
1.  Create our own checkerboard
2.  Let the VIC cipher generate a random checkerboard for us

For now we will choose the easier of the two, and let the VIC cipher generate a checkerboard for us:
~~~~
my_checkerboard = my_cipher.generate_checkerboard()
my_message = "Hello World!"
cipher_text = my_cipher.encrypt(my_message, my_checkerboard)
plain_text = my_cipher.decrypt(cipher_text, my_checkerboard)
~~~~
The checkerboard, in this example, could be exported and saved for future use.

# Cryptanalysis
Supported cryptanalysis tools can be found on our [wiki](https://gitlab.com/manny_cyber_wizard/bletchley/wikis/home#cryptanalysis).

# Contributing
To help Bletchley's continued development, please consider contributing to the project (you can find our contribution guide [here](https://gitlab.com/manny_cyber_wizard/bletchley/blob/master/CONTRIBUTING.md)).