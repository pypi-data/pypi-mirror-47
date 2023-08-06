# tap-annie

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).


## Quick Start

1. This tap is written in python and works perfectly on Python 3.6. Make sure Python 3.6 is installed in your system.

2. Install

    It is highly recommended to use a virtualenv to isolate the process without interaction with other python modules.
    ```bash
    > virtualenv -p python3 venv
    > source venv/bin/activate
    ```
    ```bash
    > pip install singer-python
    > pip install tap-annie
    ```
### Install the tap

  This tap is able to run in conjunction with a specific Singer target by piping the processes. 
       
1. Configure tap-viafoura
 
    Now, let's create a `config_tap_annie.json` in your working directory, following [sample_config.json](sample_config.json). Tap-Auth0 requires seven keys:
     - `ios_account_id` - The account connection id that is integrated with iOS.
     - `android_account_id` - The account connection id that is integrated with Android.
     - `ios_product_id` - The account connection product that is integrated with iOS.
     - `android_product_id` - The account connection product that is integrated with Android.
     - `API_key` - The API Key.
     - `delta_import` - the value of `delta_import` will be `true` or `false`. If `true` it will load only new data. With `false` it will reload all the historical data. 
     - `reload_data` - the value of `reload_new_user` will be `false` or number of days. If you specified the number of days, it will reload the data in a few days ago based on the number of days.

2. Run

  ```bash
› tap-annie -c config_tap_annie.json | target-some-api
```

---

Copyright &copy; 2018 Stitch
