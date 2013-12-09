###Docker File for creating ckan_base image

## Running

There is no need to clone this reposotory as the kindly/ckan_base is non the docker index.

The following command will install ckan and all dependancies in a container and have it running on port 5000 on the host.

```sudo docker run -name=myckan -i -t -p 5000:80 kindly/ckan_base```

This will drop you into a command line where you can add a user or do any othe admin you want for the server.

Check your browser http://0.0.0.0:5000 to see if it works.

After you quit the terminal you can restart the image by just doing.

```sudo docker start myckan```

This will run the service in the background. To stop it run.

```sudo docker stop myckan```

If you need to use the command line again at any point just run.

```sudo docker attach myckan```

You can have multiple versions just by changing the name 'myckan' and you will also need to change the port.  So run initially.

```sudo docker run -name=mysecondckan -i -t -p 5001:80 kindly/ckan_base```

## What it does.

The image itself kindly/ckan_base just contains all the CKAN dependancies (postgres, solr, apache, nginx etc), but not ckan itself.  This is to make sure this script works across ckan versions.  This docker file is what is run to make this image.  You can make yourself by just running.

```sudo docker build .```

There is a python script in /usr/lib/ckan/startup.py which which gets the latest ckan package and installs it and generates random db and session secrets. This is script has a wrapper startup.sh which is there just to make sure after it is run it falls into a shell.  This is what docker run calls by default.

If you want to run this script with a differnt deb, run the following
specifying the full url of the deb to fetch.

```sudo docker run -name=myckan -i -t -p 80:5000 kindly/ckan_base bash /usr/lib/ckan/startup.sh http://packaging.ckan.org/build/python-ckan_2.1.1-1_amd64.deb```



