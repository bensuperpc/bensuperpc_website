# Bensuperpc's website

## _My new website (WIP)_

[![bensuperpc_website](https://github.com/bensuperpc/bensuperpc_website/actions/workflows/base.yml/badge.svg)](https://github.com/bensuperpc/bensuperpc_website/actions/workflows/base.yml)

## About

This is my new website, I'm working on it, it's **not finished yet**.

## Features

- [x] Login system (With and Without Google)
- [x] Post system (with markdown)
- [x] Share files system
- [x] Comment system
- [x] Contact system
- [x] https and config file
- [ ] Youtube integration
- [ ] Email integration
- [ ] RSS integration

## Screenshots

## Installation

### Requirements

- [Python 3.10](https://www.python.org/)
- [pip](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)
- [Github token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Google API](https://console.developers.google.com/apis/credentials)

### Clone and config

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
echo "GITHUB_TOKEN=<Your github token>" >> project/.env
echo "SECRET_KEY=<Your secret key>" >> project/.env
```

You can generate a secret key with the following command:

```sh
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

Create Google API credentials:

- Go to [https://console.developers.google.com/apis/credentials](https://console.developers.google.com/apis/credentials)
- Create a new project
- Go to the credentials tab
- Create a new **OAuth client ID**
- Select **Web application**
- Add javascript origins: **<https://127.0.0.1:5000>**
- Add the following URIs: **<https://127.0.0.1:5000/login/google/callback>**
- Download the credentials as a JSON file and copy the content in the following variables:

```sh
echo "GOOGLE_CLIENT_ID=<Your google client id>" >> project/.env
echo "GOOGLE_CLIENT_SECRET=<Your google client secret>" >> project/.env
```

Now should look like this:

```sh
GITHUB_TOKEN=gd56gdf48gf45gf54dgd5sgfds54g5sdfg5dg45g
SECRET_KEY=f6d6fqsd465f46fq6sqd46f46s4df654f5645sf5f5s
GOOGLE_CLIENT_ID=f45ddfs45f4ds5d4f4fd4fds45fd45f45sf45d4fs54df.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=45dfs5d4f5d4sf45dfs5fsd54fds54fs45f
```

_Is not my real tokens :D_

Generate the certificate:

```sh
make certificate
```

### Run

Now you can run the website with:

```sh
make run
```

And go to: [https://127.0.0.1:5000/](https://127.0.0.1:5000/) or [https://localhost:5000/](https://localhost:5000/)

### Run with docker

Start the website with:

```sh
make docker-start
```

And go to: [https://127.0.0.1:5000/](https://127.0.0.1:5000/) or [https://localhost:5000/](https://localhost:5000/)

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
- [Google API](https://developers.google.com/identity/sign-in/web/sign-in)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


## License

[License](License)
