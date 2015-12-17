# How to Run Hermes

Hermes requires at least three arguments in order to run properly. 
* fs_default_ip_addr: IP address of fs.default.name used in HDFS, ie. localhost:9000.
* list_of_files_config: A configuration file that lists all the json paths referenced by configs.
* configs: Users can provide an unlimited amount of configuration files that list what datasets to use and which recommender algorithms and metrics to apply to each dataset.

For more details about list_of_files_config and configs, please read the [Configuration Files Guide](https://github.com/Lab41/hermes/tree/master/docs/configs.md).

With one configuration file:
```bash
$ hermes localhost:9000 ./hermes/configs/list_of_files.ini ./hermes/configs/config1.ini 
```

With more than one configuration files:
```bash
$ hermes localhost:9000 ./hermes/configs/list_of_files.ini ./hermes/configs/config1.ini ./hermes/configs/config2.ini
```

## Options

The hermes binary can take in multiple options:
* --version
* --verbose
* --hdfs_dir

### --version
--version displays the current hermes binary version number. The binary version number is located in hermes/hermes/__init__.py under the variable __version__.

```bash
$ hermes --version
```

### --verbose
--verbose will print out all debug messages to help you debug the code.

```bash
$ hermes --verbose localhost:9000 ./hermes/configs/list_of_files.ini ./hermes/configs/config1.ini
```

### --hdfs_dir
--hdfs_dir requires you to pass in the name of the HDFS directory to store the input data given in the configuration files. The default name is set as "datasets".

```bash
$ hermes --hdfs_dir datasets localhost:9000 ./hermes/configs/list_of_files.ini ./hermes/configs/config1.ini
```



