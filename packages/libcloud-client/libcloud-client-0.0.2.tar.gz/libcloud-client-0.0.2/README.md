# LibCloud Python Client

This is an easy-to-use Python client for [libcloud](https://gitlab.com/libcloud/libcloud).
The client library provides a thin wrapper around [boto3](https://github.com/boto/boto3) which
automatically configures the target endpoints to use libcloud for your local cloud
application development.

## Prerequisites

To make use of this library, you need to have [libcloud](https://gitlab.com/libcloud/libcloud)
installed on your local machine. In particular, the `libcloud` command needs to be available.

## Installation

The easiest way to install *LibCloud* is via `pip`:

```
pip install libcloud-client
```

## Usage

This library provides an API that is identical to `boto3`'s. For example, to list the SQS queues
in your local (LibCloud) environment, use the following code:

```
import libcloud_client.session

session = libcloud_client.session.Session()
sqs = session.client('sqs')
assert sqs.list_queues() is not None
```

## Developing

We welcome feedback, bug reports, and pull requests!

Use these commands to get you started and test your code:

```
make install
make test
```

## License

The LibCloud Python Client is released under the MIT License