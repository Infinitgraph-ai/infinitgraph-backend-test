# Infinitgraph.ai Backend Developer Technical Test

## Objective

This technical test aims to assess your skills as a Backend Developer, specifically in the context of building robust APIs using FastAPI, working with LLM integrations, implementing security best practices, and containerizing applications.

The test consists of two parts:
1. Technical implementation: Complete the sections below before your interview.
2. Collaborative discussion: Present your solution and discuss your approach during the interview.

The collaborative phase is designed to give us insight into how we would work together and should be approached as a mutual effort.

## Prerequisites

- Strong Python programming skills
- Experience with FastAPI framework
- Understanding of LLMs and prompt engineering
- Knowledge of API security and authentication
- Familiarity with Docker

## Context

At Infinitgraph.ai, we develop AI-powered text analysis applications. Our clients need to process large volumes of documents while ensuring data security and system reliability. 

For this test, you'll be working on a simplified version of our document processing service. The service provides API endpoints for:
1. Text analysis using LLM models
2. User management 
3. Processing history tracking

You'll need to complete the implementation of this service, focusing on secure and efficient API design.

---

**Important:**

- Fork [this repository](https://github.com/infinitgraph/backend-developer-test/fork), then submit a pull request contributing to the `develop` branch to send your work.
- A `docs/ANSWERS.md` file is provided for:
  - Guiding users in how to use your solution (steps 1-3)
  - Answering questions (steps 4-6)
- Limit your programming work to **steps 1-3** inclusive.

---

## Tasks

1. Set up your development environment using the provided `requirements.txt`. Create a virtual environment with your preferred tool and activate it.

2. Implement the following components in Python:
   - Complete the authentication module (`auth.py`) to secure the API endpoints using JWT
   - Implement the LLM integration in `llm_utils.py` to process text input
   - Enhance error handling across the application

3. Set up unit tests for your components and implement Docker containerization.
   *Choose essential unit tests for your API components without overdoing the number of tests.*

4. Describe how you would scale this application to handle thousands of requests per second. What architecture would you recommend and why?

5. The client needs to monitor API performance and availability. Explain your approach to monitoring and what key metrics you would track.

6. How would you improve the security of this application beyond basic authentication? List three specific measures and explain why they're important.

## Tips and Guidelines

- We estimate this test will take 3-5 hours, depending on your technical familiarity.
- The project has been tested with Python "^3.9,<3.13", so we recommend using a version within this range.
- We don't prefer any specific approach for your work. We're interested in the choices you make, your justification, and your development methodology.
- Your code must be executable.
- Implement appropriate error handling and testing for your solution.
- You may store data locally; a database is not required for this test.

## FAQ

### How do I submit my work?

Your work should be submitted as a pull request to our [repository](https://github.com/infinitgraph/backend-developer-test/). Refer to the official GitHub [documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) for assistance with this process.

### How do I run the tests?

[PyTest](https://docs.pytest.org/en/8.2.x/) is a testing framework for Python that allows you to create unit, integration, and functional tests simply and effectively. PyTest facilitates test writing with clear and concise syntax.

To run the tests, navigate to the project root and execute the command `pytest`. The result should look like:

```bash
=================================================================================== test session starts ===================================================================================
platform darwin -- Python 3.9.19, pytest-8.2.1, pluggy-1.5.0
rootdir: /Users/example/Git/backend-developer-test
plugins: anyio-4.4.0
collected 3 items                                                                                                                                                                         

test/test_models.py ...                                                                                                                                                        [100%]

==================================================================================== 3 passed in 0.12s ====================================================================================
```