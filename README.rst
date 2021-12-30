==========
LTB Server
==========

.. |stage| image:: https://img.shields.io/badge/stage-beta-yellow.png
    :alt: beta
.. |license| image:: https://img.shields.io/badge/licence-LGPL--3-lightgray.png
    :target: https://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |docker| image:: https://img.shields.io/docker/pulls/_/ubuntu
    :target: https://hub.docker.com/_/ubuntu
    :alt: Docker Pulls

|docker| |license| |stage|

TODO: Fertigstellen

README ist noch nicht fertig.

LTB (Lustiges Taschenbuch) Server für die Übersicht und Verwaltung der Existierenden und eigenen Bücher.

Features:

* Übersischt aller existierenden Bücher (ink. Ausgaben/Sonderausgaben)
* Übersicht der Bücher im Besitz
* Unterscheidung zwischen Original und Nachdruck
* Gelesen/Ungelesen Status
* Finden aller fehlenden Bücher
* Automatischer fetch der Daten von der offiziellen Homepage

**Table of contents**

.. contents::
   :local:

Installation
============

Server Image
~~~~~~~~~~~~

Das Server Image kann sowohl aus dem Code gebaut werden, als auch aus dem Docker Hub geladen werden.

Image Herunterladen
--------------------

Über den docker pull Befehl kann das Image einfach geladen werden.

``docker pull user/name:version``

Image bauen
-----------

Zum bauen des Images muss zu aller erst dieses Repository geklont werden.

``git clone XXX``

danach aus dem repository Verzeichnis heraus das image bauen.

``docker build -t name:version .``

Datenbank
~~~~~~~~~
Aktuell wird nur PostgreSQL unterstützt.

Ich empfehle PostgreSQL 13.0 bzw. das postgres:13.0-alpine Image

nginx Server
~~~~~~~~~~~~

Um eine gewisse Sicherheit und Verwaltung der Bilder zu gewährleisten, wird ein angepasster nginx Container benötigt.
Dieser kann sowohl aus dem Code gebaut werden, als auch aus dem Docker Hub geladen werden.

Image Herunterladen
--------------------

Über den docker pull Befehl kann das Image einfach geladen werden.

``docker pull user/name:version``

Image bauen
-----------

Zum bauen des Images muss zu aller erst dieses Repository geklont werden.

``git clone XXX``

danach aus dem repository Verzeichnis heraus das image bauen.

``docker build -t name:version config/nginx/``


Docker Konfiguration
~~~~~~~~~~~~~~~~~~~~
Um Server und Datenbank optimal über Docker zu verwalten empfehle ich docker-compose zu nutzen.

docker-compose Datei
--------------------

.. code-block::

   version: '3'
   services:
     nginx:
       build: ./config/nginx
       ports:
         - "80:80"
       volumes:
         - static_volume:/src/static
         - media_volume:/src/media
       depends_on:
         - web

     web:
       build: .
       volumes:
         - static_volume:/src/static
         - media_volume:/src/media
       env_file:
         - ./.env
       depends_on:
         - db

     db:
       image: postgres:13.0-alpine
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data/
       env_file:
         - ./.env

   volumes:
     postgres_data:
     static_volume:
     media_volume:

nginx
.....

* ``build ./config/nginx`` wenn das Image vorher erstellt werden soll.
* ``image name:version`` wenn ein existierendes (lokales) image verwendet werden soll.
* ``image name:version`` wenn das Image aus dem Docker Hub verwendet werden soll.

Starten des Servers
~~~~~~~~~~~~~~~~~~~

Server Konfiguration
~~~~~~~~~~~~~~~~~~~~

Bedienung
=========

Erstellen eines LTB Types
~~~~~~~~~~~~~~~~~~~~~~~~~

Fech aller aktuellen Bücher eines Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autofech nach neuen Büchern
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buch in bestand aufnehmen
~~~~~~~~~~~~~~~~~~~~~~~~~

Suchen nach Büchern
~~~~~~~~~~~~~~~~~~~

Dummy
~~~~~

#. Dummy
#. Dummy
#. Dummy

API
===

Nach neuen Büchern suchen
~~~~~~~~~~~~~~~~~~~~~~~~~

Issues / Roadmap
======================

Issues
~~~~~~

* Gespeicherte Bilder werden beim Löschen des Buches nicht aus dem Filestore entfernt

Roadmap
~~~~~~~

* Multiuser
* Unterschieldiche "Lagerorte"
* API ausbauen


Changelog
=========

1.0.0
~~~~~~~~~~

* Release

Author
======

* `Christian Heinisch <christian.heinisch@protonmail.com>`_
