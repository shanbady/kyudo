

# Kyudo
**A research framework for goal driven query interfaces.**

[![Build Status][travis_img]][travis_href] [![Stories in Ready][waffle_img]][waffle_href]

[![Kyudo Targets](docs/img/targets.jpg)][targets.jpg]

## How to Run

In order to run the server locally, follow these steps:

1. Clone the repository into a working directory of your choice
2. Install the dependencies using pip install -r requirements.txt
    Note, it may be helpful to use a virtualenv
3. Set the following environment vars:

        $ export DJANGO_SETTINGS_MODULE=kyudo.settings.development
        $ export SECRET_KEY="super secret pass"
        $ export GOOGLE_OAUTH2_KEY="googlekey"
        $ export GOOGLE_OAUTH2_SECRET="googlesecret"

    Note that this app is enabled with Google OAuth login, you'll need to
    create your own Google credentials with the Google Developers console.

4. Create a database on postgres (on the localhost) called kyudo
    Note, you can set the envvars DB_NAME, DB_USER, DB_PASS etc.
5. Run the database migration:

        $ python kyudo/manage.py migrate

6. Install the Stanford Parser and the Stanford NER tagger (requires Java 1.8). Add the paths to the jars and models in the `kyudo/kyudo/settings/development.py` file (at the end).

7. Run the server:

        $ make runserver

8. You should now be able to open a browser at http://127.0.0.1:8000

## Possible Parsers

- [Sempre](https://github.com/percyliang/sempre)
- DEANNA

A note on Syntactic parsing, this project is an academic project and uses the [Stanford Parser](http://nlp.stanford.edu/software/lex-parser.shtml) and the [Stanford NER tagger](http://nlp.stanford.edu/software/CRF-NER.shtml). The Stanford Parser uses the Penn Treebank tags for its syntactic parsing, which is documented briefly here: [Penn Treebank II Tags](https://gist.github.com/bbengfort/aa6b785aed3d673fce2c).

## About

Kyudo is a knowledge goal casebase management and annotation tool, designed to create a corpus with which to explore Casebased Reasoning and automatic Knowledge Goal solutions in an artificial intelligence setting. To that end, it is set up similarly to a Q&A application like [StackExchange](http://stackexchange.com/) or [Quora](https://www.quora.com/) - but goes further allowing users to annotate topics from [Freebase](http://www.freebase.com/) as well as statistical parses.

### Contributing

Kyudo is open source, but because this is an academic project, we would appreciate it if you would let us know how you intend to use the software (other than simply copying and pasting code so that you can use it in your own projects). If you would like to contribute (especially if you are a student at either the University of Maryland or Wright State), you can do so in the following ways:

1. Add issues or bugs to the bug tracker: [https://github.com/mclumd/kyudo/issues](https://github.com/mclumd/kyudo/issues)
2. Work on a card on the dev board: [https://waffle.io/mclumd/kyudo](https://waffle.io/mclumd/kyudo)
3. Create a pull request in Github: [https://github.com/mclumd/kyudo/pulls](https://github.com/mclumd/kyudo/pulls)

If you are a member of the MCL group, you have direct access to the repository, which is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. A typical workflow is as follows:

1. Select a card from the [dev board](https://waffle.io/mclumd/kyudo) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        ~$ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested) merge your feature into develop.

        ~$ git checkout develop
        ~$ git merge --no-ff feature-myfeature
        ~$ git branch -d feature-myfeature
        ~$ git push origin develop

4. Repeat. Releases will be routinely pushed into master via release branches, then deployed to the server.

### Name Origin

[Kyūdō](http://en.wikipedia.org/wiki/Ky%C5%ABd%C5%8D), the way of the bow, is a Japanese martial art of archery. We started in the Japanese naming scheme because of an external project code named SAMURAI. Since then our applications (Ronin, Kyudo) have followed a Japanese martial naming convention. Kyudo seems particularly important as we have the idea of goal trajectories to solve knowledge goals; much like the flight of an arrow to  hit a target.

### Attribution

The image used in this README, [Kyudo Exam 05][targets.jpg] by [Noomai](https://www.flickr.com/photos/noomai/) is licensed under [CC BY-NC-SA 2.0](https://creativecommons.org/licenses/by-nc-sa/2.0/)


<!-- References -->
[travis_img]: https://travis-ci.org/mclumd/kyudo.svg
[travis_href]: https://travis-ci.org/mclumd/kyudo
[waffle_img]: https://badge.waffle.io/mclumd/kyudo.png?label=ready&title=Ready
[waffle_href]: https://waffle.io/mclumd/kyudo
[targets.jpg]: https://flic.kr/p/4ucxLG
