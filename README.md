# beeline
Make a beeline to the end of your model search

## Installing `beeline`

Simple as:

```
git clone git@github.com:networkearth/beeline.git
cd beeline
pip install .
```

## How to Make a `beeline`

### Step 1. Upload Inputs to S3

This is as simple as creating a folder in S3 and uploading whatever your R script is going to need there. Feel free to create as complex a directory structure as you like - `beeline` will pull it all in at runtime. 

For now let's pretend we've uploaded inputs to the `meadow` bucket in the `example_inputs` folder. 

### Step 2. Write Your Script

Next write up your R script locally. Let's pretend it's called `script.R`. There are only three requirements that `beeline` has:

1. You read your inputs from a `inputs` folder
2. You output whatever you want to save to an `outputs` folder (once again the sub directories can be as complicated as you like)
3. You add a line to the very beginning of your R script that is exactly: `#!/usr/bin/env Rscript`

Besides that you can do whatever you like!

### Step 3. Write a Config

```json
{
    "name": "example",
    "output_bucket": "hive",
    "input_bucket": "meadow",
    "input_prefix": "example_inputs/"
}
```

The `name` is going to be a unique identifier for your job - your results will end up in a directory under that name in the `output_bucket`. 

The `input_bucket` should be where you saved your inputs in S3 and the `input_prefix` should be the folder you uploaded them into. 

Let's pretend we saved this as `config.json`

### Step 4. Choose a Job Type

You can run:

```bash
beeline options
```

And will get a series of options for job types. Pick the one you want. 

We'll pretend we picked `beeline-mgcv-4-4-2-small-basic-basic` which has `mgcv` installed and runs on a small fargate instance. 

### Step 5. Fly!

```bash
beeline fly beeline-mgcv-4-4-2-small-basic-basic script.R config.json
```

And just like that `beeline` will submit your job and make sure your results (in `outputs`) get written to the `output_bucket` under a folder that matches the `name` of your job (in the config). 

So in our example our results would end up in `hive:example/`.

And that's it!

## How to Deploy New Job Types

```bash
bash prep-for-deploy <CONTAINER> <CONFIG> <REQUIREMENTS> <ENTRYPOINT>
```

This will go grab the corresponding files from the appropriate directories in `apps/jobs` and make a new directory in `job_definitions` that pulls together everything [`watercycle`](https://github.com/networkearth/watercycle) needs to deploy the new job type. Then you `cd` into that directory and run:

```
watercycle deploy job
watercycle deploy container
```

