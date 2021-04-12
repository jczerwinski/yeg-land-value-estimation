# City of Edmonton Land Value Estimation

## Reports
 - [IEEE Formatted Paper](paper.pdf)
 - Google Doc Project Report
   - [Web](https://docs.google.com/document/d/1xmQWSsDa5OCwl9u7ln4yNPeCYkE5dnOUOrxTHfczDYc/edit?usp=sharing)
   - [PDF](project-report.pdf)

## Dependencies

 - Python (v3.8.8 was used, but it might work with other versions)
 - IPython (v7.22.0 was used): `pip install ipython`
 - pipenv (v2020.11.15 was used): `pip install pipenv`

## Usage

Clone this repo:

```sh
git clone https://github.com/jczerwinski/yeg-land-value-estimation
cd yeg-land-value-estimation
```

Install dependencies and load the environment:

```sh
pipenv install
pipenv shell
```

Run the scripts:

```sh
ipython getData.py
ipython model.py
```
