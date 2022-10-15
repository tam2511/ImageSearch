# ImageSearch
MVP Project with minimal functionality for visualizing image search pipelines

## What is it for?

ImageSearch was developed as an example of a simple project 
implementation for quick deployment and the ability to visualize 
the work of the model (for example, for your manager or customer). 
This allows to reduce the time of development and coordination of the solution 
in some cases.

## Requirements
- Docker

## Model inference

For example you can use cool library TorchServe ([source](https://github.com/pytorch/serve)).

We added toy example for emblem recognition problem.

This model was trained on private dataset (7k images, 3k classes).
Used architecture: EdgeNext ([paper](https://arxiv.org/abs/2206.10589), [code](https://github.com/mmaaz60/EdgeNeXt)).
Weights (traced) you can download by link: [google drive](https://drive.google.com/uc?export=download&id=1CGz3_QrEFUFSqeJY52tb0j4KiWjxi730).
For training model was used EasyPL library ([source](https://github.com/tam2511/EasyPL)). 

Obviously, you can use other libraries and models, 
as well as write your own solution and wrap it in a container.

## Backend API

When writing the backend, FastAPI ([source](https://fastapi.tiangolo.com)) was used.
There are 2 main post requests in our project:

- `/upload_zip` - takes as input a zip archive with a set of images that will be added to the search index.
Also, the zip archive needs a `data.csv` file that contains relative paths to images and their id (should be int).
Example `data.csv`:
```
image,id
0/00a8d715.jpg,23425
1/00ab6bef.jpg,24414
3/00c9eb52.jpg,23425
...
```
- `/search` - takes as input an image and pagination parameters (shift and limit).
Returns the pagination page for the index search result.

*Please note that this implementation may not be effective for your case,
because stores all data (except images) in memory.*

## Frontend part

...

## Start guide

To quickly start these services you can use our docker compose config from root directory of project:

```
docker compose up
```

And if we combine all steps then get next instruction:

```
docker compose build
docker compose up
```

## Features
- Simple project to deploy.

You can deploy all services with docker-compose.
For easy of testing the service, we have added a toy emblem recognition model.

- Services are weakly dependent on each other's internal implementation.

You can change the main functionality of each service independently.
For example: instead of torchserve you can use your own implementation,
change the behavior of the backend, or change the implementation of the frontend.
