# poseidonctrip

Distributed Crawler Management Framework Based on Scrapy, Scrapyd, Scrapyd-Client, Scrapyd-API, Django and Vue.js.

## Support

poseidonctrip is developed over Python 3.x. Python 2.x will be supported later.

## Usage

Install poseidonctrip by pip:

```bash
pip3 install poseidonctrip
```

After the installation, you need to do these things below to run poseidonctrip server:

If you have installed poseidonctrip successfully, you can use command `poseidonctrip`. If not, check the installation.

First use this command to initialize the workspace:

```bash
poseidonctrip init
```

Now you will get a folder named `poseidonctrip`.

Then cd to this folder, and run this command to initialize the Database:

```bash
cd poseidonctrip
poseidonctrip migrate
```

Next you can runserver by this command:

```bash
poseidonctrip runserver
```

Then you can visit [http://localhost:8000](http://localhost:8000) to enjoy it.

Or you can configure host and port like this:

```
poseidonctrip runserver 0.0.0.0:8888
```

Then it will run with public host and port 8888.

You can create a configurable project and then configure and generate code automatically.Also you can drag your Scrapy Project to `poseidonctrip/projects` folder. Then refresh web, it will appear in the Project Index Page and comes to un-configurable, but you can edit this
project in the web interface.

As for the deploy, you can move to Deploy Page. Firstly you need to build your project and add client in the Client Index Page, then you can deploy the project by clicking button.

After the deployment, you can manage the job in Monitor Page.

