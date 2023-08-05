To create the environment:

1. [Download Anaconda](https://docs.conda.io/en/latest/miniconda.html)
2. Install the environment: `conda env create -f src/environment.yml` 
3. Activate the environment: `source activate yourai`
4. Start the server: `python src/core/cli.py`
    1. use `--port` and `--directory` to specify the port and directory
        
        e.g. `python src/core/cli.py --port 5001 --directory ../`
        
        if not specified, the default port is `5000` and the default directory is the one current working directory
5. To test: `wget localhost:5000`
