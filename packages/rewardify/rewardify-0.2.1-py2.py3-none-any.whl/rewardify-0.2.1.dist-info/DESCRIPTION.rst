==============
rewardify-base
==============

Base frame reward system


* Free software: BSD license
* Documentation: https://rewardify-base.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.0.0 (2019-06-08)
------------------

* First release on PyPI.

0.1.0 (2019-06-14)
------------------

* Initial version

0.1.1 (2019-06-14)
------------------

* Fixed bug in setup.py, which caused the "backends" package to be excluded

0.2.0 (2019-06-15)
------------------

* Internal changes in the recycle method for rewards
* Added a "user_exists" method to the facade, which will return, whether or not the given user
  name exists in the database or not
* Added "effect" field to Reward class
    * An optional string item "effect" can ba added to the config of any reward. This string should contain
      special syntax, for what effect the reward usage should have on the rewardify system
    * Currently granting the user gold and dust are supported effects
* Added more methods for handling rewards to the facade, which include buying, using and recycling
  rewards

0.2.1 (2019-06-16)
------------------

* Fixed, that the facade method for buying a pack internally called the method for adding a pack, thus not
  actually spending gold on it


