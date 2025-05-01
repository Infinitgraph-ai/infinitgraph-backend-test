# Technical Test Responses

## _Solution Usage Guide (Steps 1-3)_

### Environment Setup

_Explain how to set up the environment to run your solution. Include any specific requirements or dependencies beyond those in requirements.txt._
1. Python 3.9+ is required
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment variables template:
   ```bash
   cp .env.example .env
   ```



### Running the Application

_Provide detailed instructions on how to run the application, including any environment variables or configuration settings needed._
1. Configure environment variables in `.env` as shown above
   ```
   # Authentication
   JWT_SECRET=your-secure-jwt-secret  # Generate a secure random string
   
   # LLM API Configuration
   OPENAI_API_KEY=your-api-key-here   # API key from OpenRouter/Deepseek/Groq etc
   OPENAI_BASE_URL=provider-base-url  # Example URLs:
                                     # OpenRouter: https://openrouter.ai/api/v1
                                     # Deepseek: https://api.deepseek.com/v1
                                     # Groq: https://api.groq.com/openai/v1
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main.app:app --reload
   ```
   The API will be available at http://localhost:8000

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs 
   - ReDoc: http://localhost:8000/redoc

### Running Tests

_Explain how to run the tests you've implemented and what they cover._

1. Run all tests:
   ```bash
   pytest
   ```

The tests cover:
- Authentication and JWT token validation
- API endpoint functionality

### Docker Setup (if implemented)

_If you implemented Docker containerization, provide instructions on how to build and run the Docker container._

Follow in Docker.md

## Questions (Steps 4-6)

### Step 4: Application Scaling

_Describe how you would scale this application to handle thousands of requests per second. What architecture would you recommend and why?_
To scale the application to handle thousands of requests per second, I recommend:

1. Application Optimization
   - Deploy with Gunicorn using multiple workers for optimal CPU utilization
   - Implement async/await patterns for I/O operations

2. Load Distribution
   - Use Nginx load balancer with multiple application instances
   - Implement intelligent traffic routing (least connections/round-robin)

3. Caching & Performance
   - Redis caching layer for frequent reads (user data, tokens)
   - Move LLM processing to background tasks using Celery
   - Use message queues for reliable task distribution

4. Usage of Multiple LLM providers
   - Use a Fallback LLM provider with a fallback strategy.
   - At Large Scale Api Calls Start hitting the Quota / rate limits.

This provides high availability, efficient resource usage, and handles both quick and long-running operations effectively.

### Step 5: Monitoring Approach

_Explain your approach to monitoring API performance and availability. What key metrics would you track?_

Key monitoring metrics and tools I recommend:

1. Performance Metrics
   - Response times and latency
   - Request throughput
   - Error rates (percentage of 4xx /5xx responses..)
   - Resource usage (CPU, memory)

2. Monitoring Tools
   - Elastic APM/New Relic for application metrics
   - Sentry for error tracking
   - Uptime monitoring with health checks


### Step 6: Security Improvements

_How would you improve the security of this application beyond basic authentication? List three specific measures and explain why they're important._

1. Prompt Hijacking Protection
When accepting user input for processing by an LLM, the input may include crafted instructions designed to override or manipulate the original system prompt. It's essential to implement prompt sanitization or input filtering to prevent malicious behavior and maintain control over the model's responses.

2. Rate Limiting & Usage Quotas
Introduce a per-user tracking mechanism (e.g., token usage or request count) to monitor resource consumption. Enforce rate limiting and quota restrictions to prevent abuse, ensure fair usage, and protect system stability.

3. Brute-Force Attack
Implement safeguards to detect and block IP addresses or accounts exhibiting repeated authentication failures. Introduce temporary lockouts, exponential backoff, or CAPTCHA challenges to deter automated brute-force attempts.


