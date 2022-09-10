# Bensuperpc's website

## _My new website (WIP)_

[![bensuperpc_website](https://github.com/bensuperpc/bensuperpc_website/actions/workflows/base.yml/badge.svg)](https://github.com/bensuperpc/bensuperpc_website/actions/workflows/base.yml)

## About

This is my new website, I'm working on it, it's **not finished yet**.

## Features

- [x] Login system
- [x] Post system (with markdown)
- [x] Share files system
- [ ] Comment system
- [ ] Contact system
- [ ] https and config file

## Screenshots

## Installation

### Requirements

- [Python 3.10](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)
- [Github token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)

### Clone

Clone this repository to your local machine using:

```sh
git clone --recurse-submodules --remote-submodules https://github.com/bensuperpc/bensuperpc_website.git
```

Go to the folder

```sh
cd bensuperpc_website
```

Install the requirements:

```sh
pip install -r requirements.txt
```

Set the environment variables:

```sh
echo "GITHUB_TOKEN=<Your github token>" >> .env
echo "SECRET_KEY=<Your secret key>" >> .env
```

_Note: You can generate a secret key with the following command:_

```sh
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### Run

Now you can run the website with:

```sh
make run
```

And go to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000/](http://localhost:5000/)

## Docker

### Requirements (for docker)

- [Docker](https://www.docker.com/)

### Run with docker

Start the website with:

```sh
make docker-start
```

And go to: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000/](http://localhost:5000/)

Stop the website with:

```sh
make docker-stop
```

Get the logs with:

```sh
make docker-logs
```

## Build with

- [Flask 2.2](https://flask.palletsprojects.com/en/2.2.x/)
- [Bootstrap 5.2](https://getbootstrap.com/)
- [Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)
- [Python 3.10](https://www.python.org/)
- [HTML5](https://html.spec.whatwg.org/multipage/)
- [CSS3](https://www.w3.org/Style/CSS/Overview.en.html)
- [JavaScript](https://www.javascript.com/)
- [jQuery](https://jquery.com/)
- [Font Awesome](https://fontawesome.com/)
- [Google Fonts](https://fonts.google.com/)
- [Gnu Make](https://www.gnu.org/software/make/)
- [Github API](https://docs.github.com/en/rest)
- [Github Actions](https://docs.github.com/en/actions)


## License

[License](License)
