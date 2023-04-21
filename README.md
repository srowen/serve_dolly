To use this example:

- Start a single-node cluster with Databricks Runtime 13.0 ML GPU. Choose, for example, an instance with 1 A10 GPU to start
- Modify the `server.py` file to load the desired model and change other settings as desired; see https://github.com/databrickslabs/dolly#generating-on-other-instances
- Run `runner` and leave it running
- Note the endpoint URL it generates
- For an example of querying the endpoint, attach the `query` notebook to any other cluster, paste the endpoint in the indicated location, and execute
- Endpoint can be accessed anywhere else too, but the request must contain a Databricks PAT in the header as shown in `query`