# Page analyser

### Hexlet and self written tests
[![Actions Status](https://github.com/Cherund/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Cherund/python-project-83/actions)
[![Self written tests](https://github.com/Cherund/python-project-83/actions/workflows/lint-check.yml/badge.svg)](https://github.com/Cherund/python-project-83/actions/workflows/lint-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/81b72b6b410e262c9524/maintainability)](https://codeclimate.com/github/Cherund/python-project-83/maintainability)

## Description
Page Analyser is a website that analyzes pages for SEO suitability, similar to [PageSpeed Insights](https://pagespeed.web.dev).

## Technologies Used
- Python 3.x
- Flask 3.x
- PostgreSQL
- HTML/Bootstrap for frontend
- Docker for containerization

## Local Setup
**After cloning the repository and setting up PostgreSQL DB**

1. **Install dependencies:**
```
make install
```
2. **Set up environment variables:** Create a `.env` file and define:
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://page_analyser_user:your-password@localhost/page_analyser
```

3. **Build tables in DB:**
```
make build
```
4. **Run server in developer mode:**
```
make dev
```

### [Project on render](https://python-project-83-xs6c.onrender.com)