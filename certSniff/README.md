Below is the formatted GitHub Markdown content for the `certSniff` application, based on the provided information:

---
![certsnifflogo](https://github.com/user-attachments/assets/8f71bab2-2f1a-4748-b293-c396f69f9be6)

# certSniff

CertSniff is a Python-based keyword sniffer, using the Certstream certificate transparency log data stream, that monitors for domain certificate events containing a string of interest.

## Overview

CertSniff connects to a certificate transparency log stream and listens for new certificates. It checks if the domains in these certificates contain specific keywords. If a keyword is found, it logs the domain to a file and prints it to the terminal. It also supports verbose output to print all domains passing through the stream.

## Features

- **Real-time Monitoring**: Listens to real-time certificate transparency log streams.
- **Keyword Matching**: Checks domains against specified keywords.
- **Logging**: Logs matched domains to a file (`log.txt`).
- **Verbose Mode**: Optionally prints all passing domains.
- **Colored Terminal Output**: Uses ANSI color codes for enhanced readability.

## Installation

Clone this repository and install the necessary dependencies:

```bash
git clone https://github.com/elithaxxor/tls_cert_grabber
cd tls_cert_grabber/certSniff
pip install -r requirements.txt
```

## Usage

Run the CertSniff script with Python:

```bash
python3 certSniff.py -f monitor.txt
```

### Command-Line Arguments

- `-f` or `--file`: Specifies a file containing keywords to sniff (default: `monitor.txt`).
- `-v` or `--verbose`: Enables verbose output (prints all domains passing through).

### Example

To monitor live certificate transparency logs that contain any string within a keyword file (`monitor.txt`):

#### `monitor.txt` Example

```
admin
test
dev
```

#### Running the Script

```bash
python3 certSniff.py -f monitor.txt
```

### Output Example

```
╔═╗┌─┐┬─┐┌┬┐╔═╗┌┐┌┬┌─┐┌─┐
║  ├┤ ├┬┘ │ ╚═╗││││├┤ ├┤ 
╚═╝└─┘┴└─ ┴ ╚═╝┘└┘┴└  └  
Certificate Transparency Log Sniffer
-----------------------------------------------------------------------------------------
Using sniff words from [monitor.txt]

[03/03/23 14:16:45]:[aonecnameg.goce.workers.dev]
[03/03/23 14:16:45]:[csbzvbzoompezxyu.southcentralus.atlas-test.cloudapp.azure.com]
[03/03/23 14:16:45]:[admin-test.crystal.io]
[03/03/23 14:16:45]:[dev-chompy.qmo.io]
[03/03/23 14:16:45]:[backuptest.blacklightsupport.co.za]
...
```

## Source Code

The source code for `certSniff.py` can be found in the `certSniff` directory of this repository. You can view it [here](https://github.com/elithaxxor/tls_cert_grabber/blob/main_pi/certSniff/certSniff.py).

---

This document provides an overview of the `certSniff` application, including its features, installation, usage, and an example of how to run the script.
