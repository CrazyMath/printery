Printery
========

Local deployment
^^^^^^^^^^^^^^^^

Software dependency:

    Vagrant 2.0.3
    Virtualbox 5.2.10
    nfsd - https://www.vagrantup.com/docs/synced-folders/nfs.html
    git

After all software requirement installed:

    git clone https://github.com/CrazyMath/printery.git
    cd printery
    vagrant up
    vagrant ssh
    source ~/.env/bin/activate
    cd /vagrant/
    python manage.py runserver 0.0.0.0:8000

After that server will be available by url http://127.0.0.1:8000 in your browser


Test data
^^^^^^^^^

Database can be filled with test data with next command:

    python manage.py filldb

It will create 3 users:

Superuser:

    login: admin
    password: test1234

Writer:

    login: writer
    password: test1234

Editor:

    login: editor
    password: test1234

And also it will create 30 new Articles.


Run test
^^^^^^^^

Test can be run with next command:

    python manage.py test --settings=config.settings.test


Project description
^^^^^^^^^^^^^^^^^^^

Superuser(Admin) through admin interface(http://127.0.0.1:8000/admin/articles/article) can create article.

New user can register on site as writer or as editor.

After new article was created it become accessible to writers on page `http://127.0.0.1:8000/articles/` . On this page
writer can assign article to (him/her)self. After article was assigned to writer it disappears from `Articles` page and
became available on page `http://127.0.0.1:8000/articles/user/`.

On page `http://127.0.0.1:8000/articles/user/` writer can see articles which were assigned to him/her. On this page writer
can edit article(add url to article). Also after url was added writer can submit it to review.

Editor on page `http://127.0.0.1:8000/articles/` can see all articles which were submitted for review. Editor can
assign article to (him/her)self. After article was assigned to editor it disappears from `Articles` page and became
available on page `http://127.0.0.1:8000/articles/user/` there editor can review articles and change their status to
`approved`.


Production usage
^^^^^^^^^^^^^^^^

For production usage should be used production requirements which can be found in file `requirements/production.txt`

Server for production should be run with key `--settings=config.settings.production`

Production settings can be found in file `config/settings/production.py`

In file `env.example` can be founded variables wich should be specified for production environment.



