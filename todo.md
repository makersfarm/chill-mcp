# ChillMCP 서버 구현 TODO

## Phase 1: 프로젝트 기본 설정
- [x] 프로젝트 폴더 구조 생성
- [x] requirements.txt 작성 (FastMCP, pytest 등)
- [x] .gitignore 업데이트 (venv, __pycache__ 등)

## Phase 2: 핵심 모듈 구현

### 2.1 설정 및 커맨드라인 파라미터 (필수!)
- [x] config.py: 커맨드라인 파라미터 파싱 구현
  - [x] --boss_alertness (0-100, 기본값 50)
  - [x] --boss_alertness_cooldown (초 단위, 기본값 300)

### 2.2 상태 관리 시스템
- [x] state_manager.py: StateManager 클래스 구현
  - [x] Stress Level (0-100) 관리
  - [x] Boss Alert Level (0-5) 관리
  - [x] 시간 경과에 따른 Stress Level 자동 증가 (1분당 1포인트)
  - [x] Boss Alert Level 자동 감소 (cooldown 주기마다 1포인트)
  - [x] Boss Alert Level 상승 로직 (boss_alertness 확률 적용)

### 2.3 휴식 도구 구현
- [x] tools.py: 기본 휴식 도구
  - [x] take_a_break
  - [x] watch_netflix
  - [x] show_meme

- [x] tools.py: 고급 농땡이 기술
  - [x] bathroom_break
  - [x] coffee_mission
  - [x] urgent_call
  - [x] deep_thinking
  - [x] email_organizing

### 2.4 응답 포맷 유틸리티
- [x] response_formatter.py: 표준 응답 생성 함수
  - [x] Break Summary, Stress Level, Boss Alert Level 포함
  - [x] 정규표현식으로 파싱 가능한 형식

### 2.5 MCP 서버
- [x] server.py: FastMCP 서버 설정
  - [x] 모든 도구 등록
  - [x] stdio transport 설정
  - [x] Boss Alert Level 5일 때 20초 지연 로직

### 2.6 진입점
- [x] main.py: 서버 실행 진입점
  - [x] 커맨드라인 파라미터 처리
  - [x] MCP 서버 시작

## Phase 3: 테스트 코드 작성

### 3.1 단위 테스트
- [x] test_config.py: 커맨드라인 파라미터 테스트
- [x] test_state_manager.py: 상태 관리 로직 테스트
  - [x] Stress Level 증가 테스트
  - [x] Boss Alert Level 상승 테스트
  - [x] Boss Alert Level 감소 테스트
- [x] test_tools.py: 도구 동작 테스트

### 3.2 통합 테스트
- [x] test_integration.py: 전체 시나리오 테스트
  - [x] 커맨드라인 파라미터 인식 테스트 (필수!)
  - [x] 연속 휴식 테스트
  - [x] 스트레스 누적 테스트
  - [x] 지연 테스트 (Boss Alert Level 5)
  - [x] 응답 파싱 테스트
  - [x] Cooldown 테스트

## Phase 4: 문서화 및 검증
- [x] README.md 사용 예시 확인
- [x] Python 3.11에서 동작 확인
- [x] 모든 필수 테스트 통과 확인 (40/40 tests passed)

## 폴더 구조
```
chill-mcp/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── state_manager.py
│   ├── tools.py
│   ├── response_formatter.py
│   └── server.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_state_manager.py
│   ├── test_tools.py
│   └── test_integration.py
├── main.py
├── requirements.txt
├── README.md
└── todo.md
```
