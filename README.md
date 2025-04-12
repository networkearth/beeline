# beeline
Make a beeline to the end of your model search

## Installing `beeline`

Simple as:

```
git clone git@github.com:networkearth/beeline.git
cd beeline
pip install .
```

If you haven't already setup your access to AWS see the instructions [below](#setting-up-access-to-aws).

## How to Make a `beeline`

### Step 1. Upload Inputs to S3 (See [Using the AWS Console](#using-the-aws-console)) 

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
    "input_prefix": "example_inputs/",
    "tags": {
        "Name": "Marcel Gietzmann-Sanders",
        "Project": "Testing"
    }
}
```

The `name` is going to be a unique identifier for your job - your results will end up in a directory under that name in the `output_bucket`. 

The `input_bucket` should be where you saved your inputs in S3 and the `input_prefix` should be the folder you uploaded them into. 

Finally the `tags` are there to do cost accounting. You can add whatever you like but `Name` and `Project` are required. 

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

And just like that `beeline` will submit your job and make sure your results (in `outputs`) get written to the `output_bucket` under a folder that matches the `name` of your job (in the config). You can see how your job is doing in the Batch console (See [Using the AWS Console](#using-the-aws-console)) 

So in our example our results would end up in `hive:example/`. (See [Using the AWS Console](#using-the-aws-console)) 

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

## Setting up Access to AWS

### Step 0. Request Access

You can reach out to marcelsanders96@gmail.com and if accepted he'll send you an email to setup a new account.

### Step 1. Setup the AWS CLI

Follow the [link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)!

### Step 2. Install `watercycle`

```bash
git clone git@github.com:networkearth/watercycle.git
cd watercycle
nvm install 22
pip install .
```

### Step 3. Sign Into Your Account

Run `aws configure sso` from the command line. This will ask you a few questions:

- SSO session name: `networkearth`
- SSO start URL: `https://d-9067d0350b.awsapps.com/start/#`
- SSO region: `us-east-1`
- SSO registration scopes: _just hit enter to continue_

This will then redirect to the browser where you can sign in with your username and password. 

Then it'll ask you a couple more questions:

- CLI default client Region: `us-east-1`
- CLI default output format: _just hit enter to continue_
- CLI profile name: `beeline`

After this you'll simply need to:

```bash
export AWS_PROFILE=beeline
watercycle login beeline
```

And you should be good to go! 

Note that if you open a new terminal you'll need to set `export AWS_PROFILE=beeline` again. 

## Using the AWS Console

If you head to `https://d-9067d0350b.awsapps.com/start/#` and then sign in you'll get access to the AWS Console. This is where you can upload things to S3 and monitor your jobs. You'll want to make sure you're set to the North Virgian region (us-east-1) in the upper right hand corner:

![region](images/region.png)

The three things of interest will be Batch (where your jobs live), S3 (where your data lives), and Billing (where you can see how much stuff is costing). Google has much better things to say about making sense of these pages than I do, but feel free to reach out at marcelsanders96@gmail.com. 

