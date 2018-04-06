# Item Catalog Application

This repository contains my implementation of the catalog application as part of the Udacity Full Stack Nanodegree Program.
This Catalog application is intended to demonstrate the concepts learned during part three of the program, 'The Backend: Databases & Applications'.

The Item Catalog Application is a web application that displays a variety of items, each belonging to a specified category. The web application allows the user to explore the contents of this catalog, including the ability to view an overview of the categories and the newest items, the contents of each category, or a specific item with a more detailed description. The user can log in to the application in order to manipulate the content. This application provides a native token-based authentication for users who will register with the application, providing a username, e-mail address, and password. If the user chooses, she can also log in to the site using her Google account. Once a user is logged in, she can create new entries, edit or delete other entries that belong to her user account. The application also provides a JSON endpoint for the contents of the database, which can be views by visiting the address `http://localhost:8000/catalog.json` in a browser.

Since I was given some freedom to create the catalog application how I would like, I created a music catalog application to categorize some of my favorite bands based on music genre. The content is consists on musical genre and the bands that fit into those categories, one band per category. Each entry for a band conatins a text description of the band, taken from that band's [Wikipedia](https://en.wikipedia.org/wiki/Main_Page) page.

## Environment Setup

Throughout the course of this Nanodegree program, a [vagrant](https://www.vagrantup.com/) virtual machine configuration is required on the host system. This virtual machine is a Linux based VM that provides a PostgreSQL database and support software needed to complete this project. The VM can be downloaded and installed from the [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) website. Udacity provided us with a basic [Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile) for configuration of the virtual machine. The Vagrantfile included in this repository is configured for this project to contain the relevant modules needed fom both Python 2.7.12 and Python 3.5.2, the versions installed on my machine.

Once the vagrant VM is installed, the user will need to navigate to the directory containing the Vagrantfile and use the command `vagrant up` to cause Vagrant to download and install the Linux virtual machine and all dependencies for the environment.
Then the user can log in to the VM using the `vagrant ssh` command. When the user is finished using the VM, she can type `exit` into the terminal to disconnect from the VM and then `vagrant halt` to shutdown.

## Running the code

The user will clone this [GitHub repository](https://github.com/sjcorreia/catalog-project) to their local machine and navigate to the `vagrant` directory. This directory contains the Vagrantfile needed to install and configure the VM for this project. After the vagrant environment has been successfully installed and the user has logged into the VM via ssh, she can navigate to the `/vagrant/catalog/` directory. This directory contains the Python files required to create the initial database, using the command

	python3 models.py

to create the database and the command

    python3 createCatalog.py

to initialize the database with sample data.

To start the webserver, the user must type

    python3 application.py

into the terminal and then visit the URL `http://localhost:8000/catalog` in the browser.

If the user would like to test the functionality, she can use the following information to log in to the application.

    Username: RoboUser
    Password: Udacity1

This log-in information will give the user the ability to test the CRUD operations on the contents of the application.

## Additional Resources

The following links were helpful during the implementation of this project.

* [Flask HTTPAuth Docs](https://flask-httpauth.readthedocs.io/en/latest/)
* [RESTful APIs for Flask](http://blog.luisrei.com/articles/flaskrest.html)
* [Bootstrap Forms](https://getbootstrap.com/docs/4.0/components/forms/)
* [Bootstrap Forms Input](https://www.w3schools.com/bootstrap/bootstrap_forms_inputs.asp)
* [Bootstrap Dropdowns](https://getbootstrap.com/docs/4.0/components/dropdowns/)
* [Universe](https://pixabay.com/en/universe-sky-star-space-all-2742113/) image from Pixabay
* [Milky Way Sky](https://pixabay.com/en/milky-way-starry-sky-night-sky-star-2695569/) image from Pixabay
* [Various Syntax](https://stackoverflow.com/questions/21639275/python-syntaxerror-non-ascii-character-xe2-in-file), [Flask related](https://stackoverflow.com/questions/8552675/form-sending-error-flask), and [httplib2](http://httplib2.readthedocs.io/en/latest/libhttplib2.html) answers from StackOverflow

## Python Code Quality

The source code was run through the command-line tool `pycodestyle` to check that the code conforms to the [PEP8](https://www.python.org/dev/peps/pep-0008/) standards. The source code was also checked using this tool, which did not report any errors.

This tool is run on the command line of the terminal as follows:

	pycodestyle application.py

## Notes

The HTML/CSS used for this project was adapted from the [repository](https://github.com/udacity/ud330) for examples from the Udacity course Full-Stack Foundations. These sources were used as a reference in creating templates for each HMTL element/page.

## License

The contents of this repository are covered under the [MIT License](LICENSE).
