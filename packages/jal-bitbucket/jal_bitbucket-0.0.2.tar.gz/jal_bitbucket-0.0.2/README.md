# BitBucket
Interact with BitBucket API

---

## Install
    
### Pypi

    pip3 install -U jal_bitbucket

### From Source

    git clone git@github.com:jalgraves/bitbucket.git
    cd bitbucket
    python3 setup.py sdist bdist_wheel
    pip3 install .

### Export Credentials

    export BITBUCKET_USER='<bitbucket_username>
    export BITBUCKET_API_KEY='<bitbucket_api_key>

---

## Usage

    from jal_bitbucket import BitBucket
