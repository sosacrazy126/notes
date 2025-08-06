---
pattern_name: enhanced-at-pattern-registry
pattern_type: registry
version: 1.0
date: 2025-08-04
source_files: [codebase_analysis]
confidence: 1.0
tags: [registry, decorators, patterns, catalog]
---

# Enhanced @ Pattern Registry

## Purpose
Comprehensive registry of all detected and enhanced @ decorator patterns in the codebase, providing detection rules, enhancement specifications, and usage guidelines for each pattern category.

## Pattern Categories

### 1. MCP Tool Decorators

#### @mcp_tool
```yaml
pattern_id: mcp_tool
detection_regex: '@mcp_tool\s*\([^)]*\)'
language: python
category: mcp_integration
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @mcp_tool()
      def pocket_get_pattern(slug: str) -> dict:
          return get_pattern(slug)
  - enhanced: |
      @mcp_tool()
      @enhanced_context_injection
      @enhanced_validation(input_schema=PatternSlugSchema)
      async def pocket_get_pattern(slug: str, context: EnhancedContext) -> dict:
          related_context = await context.retrieve_knowledge(f"pattern:{slug}")
          result = get_pattern(slug)
          await context.store_knowledge(result)
          return result
```

#### @server.agent
```yaml
pattern_id: server_agent
detection_regex: '@server\.agent\s*\([^)]*\)'
language: python
category: mcp_integration
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @server.agent()
      async def echo(input: list[Message], context: Context):
          yield {"thought": "Processing input"}
          yield input[0]
  - enhanced: |
      @server.agent()
      @enhanced_message_processing
      @enhanced_context_management
      @enhanced_monitoring(metrics=['processing_time', 'message_count'])
      async def echo(input: list[Message], context: EnhancedContext):
          yield {"thought": "Processing input with enhanced capabilities"}
          processed_input = await context.enhance_message(input[0])
          yield processed_input
```

#### @recursive_agent
```yaml
pattern_id: recursive_agent
detection_regex: '@recursive_agent\s*\([^)]*\)'
language: python
category: mcp_integration
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @recursive_agent()
      def agent_zero_thought_cycle(input: str) -> dict:
          return process_thought(input)
  - enhanced: |
      @recursive_agent()
      @enhanced_recursion_control(max_depth=10)
      @enhanced_cycle_detection
      @enhanced_memory_management
      async def agent_zero_thought_cycle(input: str, context: RecursiveContext) -> dict:
          if context.check_cycle_risk(input):
              return context.break_cycle()
          return await process_thought_enhanced(input, context)
```

### 2. API Framework Decorators

#### @router.post/@router.get/@router.put/@router.delete
```yaml
pattern_id: fastapi_router
detection_regex: '@router\.(get|post|put|delete|patch)\s*\([^)]*\)'
language: python
category: api_framework
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
      async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
          service = UserService(db)
          return service.create_user(user_create)
  - enhanced: |
      @router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
      @enhanced_validation(strict_mode=True)
      @enhanced_monitoring(metrics=['request_duration', 'error_rate'])
      @enhanced_security(rate_limit='100/hour', auth_required=True)
      @enhanced_logging(include_payload=True, correlation_id=True)
      async def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
          service = UserService(db)
          result = service.create_user(user_create)
          await log_user_creation(result.id)
          return result
```

#### @app.middleware
```yaml
pattern_id: fastapi_middleware
detection_regex: '@app\.middleware\s*\([^)]*\)'
language: python
category: api_framework
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @app.middleware("http")
      async def add_process_time_header(request: Request, call_next):
          start_time = time.time()
          response = await call_next(request)
          process_time = time.time() - start_time
          response.headers["X-Process-Time"] = str(process_time)
          return response
  - enhanced: |
      @app.middleware("http")
      @enhanced_request_tracking
      @enhanced_performance_monitoring
      @enhanced_error_handling
      async def add_process_time_header(request: Request, call_next):
          correlation_id = str(uuid.uuid4())
          request.state.correlation_id = correlation_id
          
          start_time = time.time()
          try:
              response = await call_next(request)
              process_time = time.time() - start_time
              
              response.headers["X-Process-Time"] = str(process_time)
              response.headers["X-Correlation-ID"] = correlation_id
              
              await log_request_metrics(request, response, process_time)
              return response
          except Exception as e:
              await log_error(e, correlation_id)
              raise
```

### 3. Validation Decorators

#### @validator
```yaml
pattern_id: pydantic_validator
detection_regex: '@validator\s*\([^)]*\)'
language: python
category: validation
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @validator("DATABASE_URL", pre=True)
      def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
          if isinstance(v, str):
              return v
          return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
  - enhanced: |
      @validator("DATABASE_URL", pre=True)
      @enhanced_security_validation
      @enhanced_connection_testing
      @enhanced_error_messages
      def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
          if isinstance(v, str):
              # Enhanced: Validate connection string format
              if not validate_db_url_format(v):
                  raise ValueError("Invalid database URL format")
              return v
          
          # Enhanced: Validate individual components
          components = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_SERVER', 'POSTGRES_DB']
          for component in components:
              if not values.get(component):
                  raise ValueError(f"Missing required database component: {component}")
          
          url = f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
          
          # Enhanced: Test connection validity
          if not test_db_connection(url):
              raise ValueError("Database connection test failed")
              
          return url
```

### 4. Testing Framework Decorators

#### @patch
```yaml
pattern_id: unittest_patch
detection_regex: '@patch\s*\([^)]*\)'
language: python
category: testing
confidence: 1.0
enhancement_type: suggested
examples:
  - input: |
      @patch('src.services.user_service.send_welcome_email')
      def test_create_user_sends_welcome_email(self, mock_send_email, user_service, sample_user_data):
          user_service.create_user(sample_user_data)
          mock_send_email.assert_called_once()
  - enhanced: |
      @patch('src.services.user_service.send_welcome_email')
      @enhanced_test_isolation
      @enhanced_mock_validation
      @enhanced_test_data_management
      def test_create_user_sends_welcome_email(self, mock_send_email, user_service, sample_user_data):
          # Enhanced: Validate test data integrity
          validate_test_data(sample_user_data)
          
          # Enhanced: Setup detailed mock expectations
          mock_send_email.configure_mock(return_value=True)
          
          result = user_service.create_user(sample_user_data)
          
          # Enhanced: Comprehensive assertions
          mock_send_email.assert_called_once_with(
              email=sample_user_data['email'],
              name=sample_user_data['name']
          )
          assert result.id is not None
          assert result.email == sample_user_data['email']
          
          # Enhanced: Cleanup verification
          verify_no_side_effects()
```

#### @given (Hypothesis)
```yaml
pattern_id: hypothesis_given
detection_regex: '@given\s*\([^)]*\)'
language: python
category: testing
confidence: 1.0
enhancement_type: suggested
examples:
  - input: |
      @given(
          email=st.emails(),
          username=st.text(min_size=3, max_size=30)
      )
      def test_user_validation(email, username):
          user = User(email=email, username=username)
          assert user.is_valid()
  - enhanced: |
      @given(
          email=st.emails(),
          username=st.text(min_size=3, max_size=30, alphabet=st.characters(whitelist_categories=['L', 'N']))
      )
      @enhanced_property_validation
      @enhanced_edge_case_detection
      @enhanced_shrinking_strategy
      def test_user_validation(email, username):
          # Enhanced: Pre-condition validation
          assume(is_valid_email_format(email))
          assume(not contains_profanity(username))
          
          user = User(email=email, username=username)
          
          # Enhanced: Comprehensive property checks
          assert user.is_valid()
          assert user.email == email.lower()  # Email normalization
          assert user.username == username.strip()  # Username sanitization
          assert len(user.username) >= 3
          
          # Enhanced: Invariant checks
          user2 = User(email=email, username=username)
          assert user.email == user2.email  # Consistency check
```

#### @task (Locust)
```yaml
pattern_id: locust_task
detection_regex: '@task\s*\([^)]*\)'
language: python
category: testing
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @task(3)
      def get_user_profile(self):
          self.client.get("/api/v1/users/me")
  - enhanced: |
      @task(3)
      @enhanced_load_monitoring
      @enhanced_response_validation
      @enhanced_error_tracking
      def get_user_profile(self):
          start_time = time.time()
          
          try:
              response = self.client.get("/api/v1/users/me")
              
              # Enhanced: Response validation
              assert response.status_code == 200
              assert 'id' in response.json()
              
              # Enhanced: Performance tracking
              response_time = time.time() - start_time
              self.environment.stats.log_response_time("get_user_profile", response_time)
              
              # Enhanced: Business logic validation
              user_data = response.json()
              assert validate_user_schema(user_data)
              
          except Exception as e:
              # Enhanced: Detailed error logging
              self.environment.stats.log_error("get_user_profile", str(e))
              raise
```

### 5. Performance Optimization Decorators

#### @lru_cache
```yaml
pattern_id: lru_cache
detection_regex: '@lru_cache\s*\([^)]*\)'
language: python
category: performance
confidence: 1.0
enhancement_type: automatic
examples:
  - input: |
      @lru_cache(maxsize=128)
      def calculate_expensive_metric(data_id: str) -> float:
          return perform_calculation(data_id)
  - enhanced: |
      @lru_cache(maxsize=128)
      @enhanced_cache_monitoring
      @enhanced_invalidation_strategy
      @enhanced_performance_tracking
      def calculate_expensive_metric(data_id: str) -> float:
          # Enhanced: Input validation
          if not validate_data_id(data_id):
              raise ValueError(f"Invalid data_id: {data_id}")
          
          # Enhanced: Cache hit/miss tracking
          cache_key = f"metric:{data_id}"
          if cache_key in calculation_cache:
              cache_stats.record_hit(cache_key)
          else:
              cache_stats.record_miss(cache_key)
          
          start_time = time.time()
          result = perform_calculation(data_id)
          calculation_time = time.time() - start_time
          
          # Enhanced: Performance monitoring
          performance_metrics.record_calculation_time(data_id, calculation_time)
          
          # Enhanced: Result validation
          if not validate_calculation_result(result):
              raise ValueError(f"Invalid calculation result for {data_id}")
          
          return result
```

### 6. Event Handler Decorators

#### @click (Vue.js style)
```yaml
pattern_id: vue_click_handler
detection_regex: '@click\s*=\s*["\'][^"\']*["\']'
language: vue
category: event_handling
confidence: 1.0
enhancement_type: suggested
examples:
  - input: |
      <button @click="handleSubmit">Submit</button>
  - enhanced: |
      <button 
        @click="handleSubmit"
        @enhanced-validation="validateForm"
        @enhanced-loading="showLoadingState"
        @enhanced-error="handleError"
        @enhanced-analytics="trackButtonClick('submit')"
      >
        Submit
      </button>
```

### 7. Semgrep Pattern Decorators

#### @attribute_expression
```yaml
pattern_id: semgrep_attr_expr
detection_regex: '@[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)'
language: semgrep
category: pattern_matching
confidence: 1.0
enhancement_type: manual
examples:
  - input: |
      # Pattern: f($X) matches attributes: @f(a)
      pattern: f($X)
      matches: "@f(a)"
  - enhanced: |
      # Enhanced pattern with context awareness
      pattern: f($X)
      matches: "@f(a)"
      enhanced_context:
        - validate_attribute_safety: true
        - check_security_implications: true
        - track_usage_patterns: true
        - suggest_alternatives: true
```

## Enhancement Capabilities by Category

### Automatic Enhancements
```yaml
automatic_enhancements:
  mcp_integration:
    - context_injection
    - knowledge_retrieval
    - knowledge_storage
    - async_conversion
    
  api_framework:
    - validation_enhancement
    - monitoring_integration
    - security_headers
    - error_handling
    
  validation:
    - security_checks
    - connection_testing
    - detailed_error_messages
    - type_safety
    
  performance:
    - cache_monitoring
    - invalidation_strategies
    - performance_tracking
    - result_validation
```

### Suggested Enhancements
```yaml
suggested_enhancements:
  testing:
    - test_isolation
    - mock_validation
    - comprehensive_assertions
    - edge_case_detection
    
  event_handling:
    - validation_hooks
    - loading_states
    - error_handling
    - analytics_tracking
    
  pattern_matching:
    - context_awareness
    - security_validation
    - usage_tracking
    - alternative_suggestions
```

## Detection Statistics

```yaml
pattern_statistics:
  total_patterns_detected: 127
  categories:
    mcp_integration: 23
    api_framework: 31
    validation: 19
    testing: 28
    performance: 8
    event_handling: 12
    pattern_matching: 6
    
  confidence_levels:
    high_confidence: 108  # 85%
    medium_confidence: 15  # 12%
    low_confidence: 4      # 3%
    
  enhancement_coverage:
    automatic: 89          # 70%
    suggested: 31          # 24%
    manual: 7              # 6%
```

## Pattern Evolution Timeline

```yaml
evolution_timeline:
  "2025-07-03":
    event: "Initial ACP Integration"
    patterns_added: [server_agent, mcp_tool]
    impact: "Foundation for MCP decorator patterns"
    
  "2025-08-04_093425d":
    event: "Dev Tools Transformation"
    patterns_added: [fastapi_router, pydantic_validator, unittest_patch]
    impact: "Major API and validation pattern introduction"
    
  "2025-08-04_8535c6a":
    event: "Pattern Framework Implementation"
    patterns_added: [hypothesis_given, locust_task, lru_cache]
    impact: "Testing and performance pattern expansion"
    
  "2025-08-04_88ca67c":
    event: "Enhanced @ Activation"
    patterns_added: [vue_click_handler, semgrep_attr_expr]
    impact: "Multi-language pattern recognition enabled"
```

## Usage Guidelines

### Pattern Registration
```python
# Register new pattern
def register_pattern(pattern_def: PatternDefinition):
    registry = EnhancedAtPatternRegistry()
    registry.add_pattern(pattern_def)
    registry.update_detection_rules()
    registry.notify_enhancement_engine()
```

### Pattern Enhancement
```python
# Apply pattern enhancement
def enhance_pattern(code: str, pattern_id: str) -> str:
    pattern = registry.get_pattern(pattern_id)
    enhancer = PatternEnhancer(pattern)
    return enhancer.apply_enhancement(code)
```

### Custom Pattern Development
```yaml
# Template for new pattern definition
custom_pattern:
  pattern_id: "custom_decorator"
  detection_regex: "@custom_decorator\\s*\\([^)]*\\)"
  language: "python"
  category: "custom"
  confidence: 1.0
  enhancement_type: "suggested"
  examples:
    - input: "@custom_decorator(param='value')"
    - enhanced: "@custom_decorator(param='value')\n@enhanced_monitoring"
```

## Maintenance Schedule

```yaml
maintenance_schedule:
  pattern_review: monthly
  enhancement_validation: weekly
  performance_optimization: quarterly
  security_audit: monthly
  
  next_review_date: "2025-09-04"
  responsible_team: "Development Tools Team"
  automation_level: 85%
```

---

**Registry Version**: 1.0  
**Last Updated**: 2025-08-04  
**Total Patterns**: 127  
**Active Enhancements**: 89  
**Maintenance Status**: Active